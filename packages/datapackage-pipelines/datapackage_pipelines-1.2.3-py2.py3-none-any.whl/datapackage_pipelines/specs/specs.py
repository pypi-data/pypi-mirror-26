import os

import yaml
from datapackage_pipelines.status import status

from .resolver import resolve_executor
from .errors import SpecError
from .schemas.validator import validate_pipeline
from .parsers import BasicPipelineParser, SourceSpecPipelineParser
from .parsers.base_parser import PipelineSpec
from .hashers import HashCalculator, DependencyMissingException

SPEC_PARSERS = [
    BasicPipelineParser(),
    SourceSpecPipelineParser()
]


def resolve_processors(spec):
    abspath = os.path.abspath(spec.path)
    for step in spec.pipeline_details['pipeline']:
        if 'executor' not in step:
            step['executor'] = resolve_executor(step,
                                                abspath,
                                                spec.errors)


def process_schedules(spec):
    if spec.schedule is None:
        schedule = spec.pipeline_details.get('schedule', {})
        if 'crontab' in schedule:
            schedule = schedule['crontab'].split()
            spec.schedule = schedule


def calculate_dirty(spec):
    pipeline_status = status.get_status(spec.pipeline_id) or {}
    dirty = pipeline_status.get('cache_hash', '') != spec.cache_hash
    dirty = dirty or pipeline_status.get('state') != 'SUCCEEDED'
    dirty = dirty and len(spec.errors) == 0

    spec.dirty = dirty


def find_specs(root_dir='.'):
    for dirpath, _, filenames in os.walk(root_dir):
        if dirpath.startswith('./.'):
            continue
        for filename in filenames:
            for parser in SPEC_PARSERS:
                if parser.check_filename(filename):
                    fullpath = os.path.join(dirpath, filename)
                    with open(fullpath, encoding='utf8') as spec_file:
                        contents = spec_file.read()
                        try:
                            spec = yaml.load(contents)
                            yield from parser.to_pipeline(spec, fullpath)
                        except yaml.YAMLError as e:
                            error = SpecError('Invalid Spec File %s' % fullpath, str(e))
                            yield PipelineSpec(path=dirpath, errors=[error])


def pipelines():

    specs = find_specs()
    hasher = HashCalculator()
    while specs is not None:
        deferred = []
        found = False

        for spec in specs:
            error_num = len(spec.errors)
            if (spec.pipeline_details is not None and
                    validate_pipeline(spec.pipeline_details, spec.errors)):

                resolve_processors(spec)
                process_schedules(spec)

                try:
                    hasher.calculate_hash(spec)
                    found = True
                except DependencyMissingException as e:
                    deferred.append((e.spec, e.missing))
                    continue

                calculate_dirty(spec)

            if not error_num and len(spec.errors):
                status.register(spec.pipeline_id,
                                spec.cache_hash,
                                spec.pipeline_details,
                                spec.source_details,
                                spec.errors)

            yield spec

        if found and len(deferred) > 0:
            specs = iter((x[0] for x in deferred))
        else:
            for spec, missing in deferred:
                spec.errors.append(
                    SpecError('Missing dependency',
                              'Failed to find a dependency: {}'.format(missing))
                )
                yield spec
            specs = None


def register_all_pipelines():
    for spec in pipelines():
        status.register(spec.pipeline_id,
                        spec.cache_hash,
                        pipeline=spec.pipeline_details,
                        source=spec.source_details,
                        errors=spec.errors)
