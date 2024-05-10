from typing import Any
import os

from jinja2 import Template


def prefix_path(file_path: str) -> str:
  '''prefix the file path with the project root folder

  :param str file_path: file path
  :return str: prefixed file path
  '''

  return os.path.join(os.path.dirname(__file__), file_path)


def read(file_path: str) -> str:
  '''read a text file

  :param str file_path: file path prefix with the project root folder
  :return str: text from the file
  '''

  with open(file_path, 'r', encoding='utf-8') as _f:
    return _f.read()


def render(template_file_path: str, data: Any) -> str:
  '''render jinja2 template

  :param str template_file_path: template file path
  :param Any data: data to be rendered
  :return str: output string
  '''

  template = Template(read(template_file_path))
  return template.render(data)


def write(file_path: str, contents: str, *, mode='a', encoding='utf-8'):
  '''write text to a file

  :param str file_path: file path
  :param str contents: text to be written
  :param str mode: file open mode, 'w' to overwrite; or 'a' to append
  :param str encoding: file encoding
  '''

  with open(file_path, mode=mode, encoding=encoding) as _f:
    _f.write(contents)
