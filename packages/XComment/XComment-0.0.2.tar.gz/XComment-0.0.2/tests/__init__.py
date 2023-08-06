from os import listdir
from re import sub
from os.path import dirname, realpath, join, basename
from zipfile import ZipFile
from typing import Tuple

from XComment.comments_remover import Language


def get_input_and_output_source_file_paths(language: Language) -> Tuple[str, str]:  # noqa
    tests_dir_path = dirname(realpath(__file__))
    sources_dir_path = join(tests_dir_path, 'sources')
    language_sources_dir_path = join(sources_dir_path, language.name)
    input_source_file_prefix = 'input'
    output_source_file_prefix = 'output'
    input_file_path = output_file_path = None
    for file_name in listdir(language_sources_dir_path):
        if file_name.find('.zip') >= 0:
            continue
        if file_name.startswith(input_source_file_prefix):
            input_file_path = join(language_sources_dir_path, file_name)
        if file_name.startswith(output_source_file_prefix):
            output_file_path = join(language_sources_dir_path, file_name)
        if input_file_path and output_file_path:
            return input_file_path, output_file_path


def strip_spaces_and_linebreaks(s: str) -> str:
    return ''.join(s.split())


def prepare_zipped_sources(path):
    zippath = sub(r"(\.[a-z]*)$", ".zip", path)
    zf = ZipFile(zippath, mode='w')
    try:
        zf.write(path, basename(path))
    finally:
        zf.close()
    return zippath
