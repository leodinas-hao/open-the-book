from typing import Any
import os

from jinja2 import Template


def read(file_path: str) -> str:
  '''read a text file

  :param str file_path: file path prefix with the project root folder
  :return str: text from the file
  '''

  if not os.path.isabs(file_path):
    abs_path = os.path.join(os.path.dirname(__file__), file_path)
  else:
    abs_path = file_path

  with open(abs_path, 'r', encoding='utf-8') as _f:
    return _f.read()


def render(template_file_path: str, data: Any) -> str:
  '''render jinja2 template

  :param str template_file_path: template file path
  :param Any data: data to be rendered
  :return str: output string
  '''

  template = Template(read(template_file_path))
  return template.render(data)
