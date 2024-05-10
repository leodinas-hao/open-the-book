import os
from zipfile import ZipFile

import pytest
from jinja2 import Template

from open_the_book import utils


@pytest.mark.parametrize('output, book', [
  ('temp/simple_epub.epub', {
    'title': 'test',
    'author': 'author1',
    'uid': '1234567890',
    'chapters': [
      {'index': 0, 'name': 'c0', 'content': 'chapter 0 content'},
      {'index': 1, 'name': 'c1', 'content': 'chapter 1 content'},
    ]
  }),
])
def test_simple_epub(output, book):
  # https://www.manuel-strehl.de/simple_epub_ebooks_with_python
  with ZipFile(output, 'w') as epub:
    # The first file must be named "mimetype"
    # epub.writestr("mimetype", "application/epub+zip")
    epub.writestr('mimetype', utils.read(utils.prefix_path('templates/mimetype')))
    epub.writestr('META-INF/container.xml', utils.read(utils.prefix_path('templates/container.xml')))
    epub.writestr('OEBPS/style.css', utils.read(utils.prefix_path('templates/style.css')))

    epub.writestr('OEBPS/book-toc.html', utils.render(utils.prefix_path('templates/book-toc.html.j2'), book))
    epub.writestr('OEBPS/toc.ncx', utils.render(utils.prefix_path('templates/toc.ncx.j2'), book))
    epub.writestr('OEBPS/content.opf', utils.render(utils.prefix_path('templates/content.opf.j2'), book))
    epub.writestr('OEBPS/cover.html', utils.render(utils.prefix_path('templates/cover.html.j2'), book))
    for ch in book['chapters']:
      epub.writestr(f'OEBPS/{ch["index"]}.html', utils.render(utils.prefix_path('templates/chapter.html.j2'), ch))

  assert os.path.exists(output)

  # delete the file
  os.remove(output)
