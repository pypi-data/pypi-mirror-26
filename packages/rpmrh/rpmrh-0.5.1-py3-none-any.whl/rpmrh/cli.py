"""Command Line Interface for the package"""

import logging
from collections import defaultdict, OrderedDict
from contextlib import ExitStack
from functools import reduce, wraps
from itertools import chain, repeat
from operator import itemgetter, attrgetter
from pathlib import Path
from typing import Callable, Iterator

import attr
import click
import toml
from attr.validators import instance_of
from ruamel import yaml

from . import RESOURCE_ID, configuration, util
from .service.abc import Repository, Builder, BuildFailure


@attr.s(slots=True, frozen=True)
class Parameters:
    """Global run parameters (CLI options, etc.)"""

    #: Source group name
    source = attr.ib(validator=instance_of(str))
    #: Destination group name
    destination = attr.ib(validator=instance_of(str))
    #: EL major version
    el = attr.ib(validator=instance_of(int))

    #: Configured and indexed service instances
    service = attr.ib(validator=instance_of(configuration.InstanceRegistry))

    @service.default
    def load_user_and_bundled_services(_self):
        """Loads all available user and bundled service configuration files."""

        streams = chain(
            util.open_resource_files(
                root_dir='conf.d',
                extension='.service.toml',
            ),
            util.open_config_files(
                extension='.service.toml',
            ),
        )

        with ExitStack() as opened:
            streams = map(opened.enter_context, streams)
            contents = map(toml.load, streams)

            return configuration.InstanceRegistry.from_merged(*contents)


# Command decorators
def processor(func: Callable):
    """Process a sequence of (SCL collection, its package iterator) pairs. """

    @wraps(func)
    def wrapper(*args, **kwargs):
        def bound(stream: Iterator):  # bind args, kwargs, wait for the stream
            return func(stream, *args, **kwargs)
        return bound
    return wrapper


def generator(func: Callable):
    """Add package iterators to a sequence of SCL names.

    Any existing package iterators are discarded.
    """

    @wraps(func)
    @processor
    def wrapper(stream, *args, **kwargs):
        # Discard the existing package iterators
        stream = map(itemgetter(0), stream)
        return func(stream, *args, **kwargs)
    return wrapper


# Logging setup
logger = logging.getLogger(RESOURCE_ID)
util.logging.basic_config(logger)


# Commands
@click.group(chain=True)
@util.logging.quiet_option(logger)
@click.option(
    '--from', '-f', 'source',
    help='Name of a source group (tag, target, ...).'
)
@click.option(
    '--to', '-t', 'destination',
    help='Name of a destination group (tag, target, ...).'
)
@click.option(
    '--el', '-e', type=click.IntRange(6), default=7,
    help='Major EL version.',
)
@click.option(
    '--collection', '-c', 'collection_seq', multiple=True,
    help='Name of the SCL to work with (can be used multiple times).'
)
@click.pass_context
def main(context, collection_seq, **config_options):
    """RPM Rebuild Helper – an automation tool for mass RPM rebuilding,
    with focus on Software Collections.
    """

    # Store configuration
    context.obj = Parameters(**config_options)


@main.resultcallback()
@click.pass_context
def run_chain(context, processor_seq, collection_seq, **_config_options):
    """Run a sequence of collections through a processor sequence.

    Keyword arguments:
        processor_seq: The callables to apply to the collection sequence.
        collection_seq: The sequence of SCL names to be processed.
    """

    # TODO: Start with latest packages from each collection
    collection_seq = zip(collection_seq, repeat(None))

    # Apply the processors
    pipeline = reduce(
        lambda data, proc: proc(data),
        processor_seq,
        collection_seq
    )

    # Output the results in YAML format
    stdout = click.get_text_stream('stdout', encoding='utf-8')
    for collection, packages in pipeline:
        packages = sorted(packages)

        if not packages:
            continue

        yaml.dump(
            {collection: [str(pkg) for pkg in packages]},
            stream=stdout,
            default_flow_style=False,
        )


@main.command()
@generator
@click.pass_obj
def diff(params, collection_stream):
    """List all packages from source tag missing in destination tag."""

    for collection in collection_stream:
        def latest_builds(group):
            """Fetch latest builds from a group."""

            tag = params.service.unalias(
                'tag', group,
                el=params.el,
                collection=collection
            )
            repo = params.service.index['tag_prefixes'].find(
                tag, type=Repository
            )

            yield from repo.latest_builds(tag)

        # Packages present in destination
        present = {
            build.name: build
            for build in latest_builds(params.destination)
            if build.name.startswith(collection)
        }

        def obsolete(package):
            return (
                package.name in present
                and present[package.name] >= package
            )

        missing = (
            pkg for pkg in latest_builds(params.source)
            if pkg.name.startswith(collection)
            and not obsolete(pkg)
        )

        yield collection, missing


@main.command()
@click.option(
    '--output-dir', '-d', metavar='DIR',
    type=click.Path(file_okay=False, writable=True),
    default='.',
    help='Target directory for downloaded packages [default: "."].'
)
@processor
@click.pass_obj
def download(params, collection_stream, output_dir):
    """Download packages into specified directory."""

    log = logger.getChild('download')
    output_dir = Path(output_dir).resolve()

    for collection, packages in collection_stream:
        tag = params.service.unalias(
            'tag', params.source, el=params.el, collection=collection,
        )
        repo = params.service.index['tag_prefixes'].find(tag, type=Repository)
        collection_dir = output_dir / collection

        collection_dir.mkdir(exist_ok=True)

        def logged_download(package):
            log.info('Fetching {}'.format(package))
            return repo.download(package, collection_dir)

        paths = map(logged_download, packages)

        yield collection, paths


@main.command()
@click.option(
    '--failed', '-f', 'fail_file',
    type=click.File(mode='w', encoding='utf-8', lazy=True),
    help='Path to store build failures to [default: stderr].',
)
@processor
@click.pass_obj
def build(params, collection_stream, fail_file):
    """Attempt to build packages in target."""

    failed = defaultdict(set)

    for collection, packages in collection_stream:
        target = params.service.unalias(
            'target', params.destination, el=params.el, collection=collection,
        )
        builder = params.service.index['target_prefixes'].find(
            target, type=Builder,
        )

        def build_and_filter_failures(packages):
            with builder:
                for pkg in packages:
                    try:
                        yield builder.build(target, pkg)
                    except BuildFailure as failure:
                        failed[collection].add(failure)

        yield collection, build_and_filter_failures(packages)

    if not failed:
        raise StopIteration()

    # Convert the stored exceptions to readable representation
    readable_failures = {
        scl: OrderedDict(
            (f.package.nevra, f.reason)
            for f in sorted(fails, key=attrgetter('package'))
        ) for scl, fails in failed.items()
    }

    if fail_file is None:
        fail_file = click.get_text_stream('stderr', encoding='utf-8')

    yaml.dump(readable_failures, stream=fail_file, default_flow_style=False)
