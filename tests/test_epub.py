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
    epub.write('src/open_the_book/templates/mimetype', arcname='mimetype')
    epub.write('src/open_the_book/templates/container.xml', arcname='META-INF/container.xml')
    epub.write('src/open_the_book/templates/style.css', arcname='OEBPS/style.css')

    epub.writestr('OEBPS/book-toc.html', utils.render('src/open_the_book/templates/book-toc.html.j2', book))
    epub.writestr('OEBPS/toc.ncx', utils.render('src/open_the_book/templates/toc.ncx.j2', book))
    epub.writestr('OEBPS/content.opf', utils.render('src/open_the_book/templates/content.opf.j2', book))
    epub.writestr('OEBPS/cover.html', utils.render('src/open_the_book/templates/cover.html.j2', book))
    for ch in book['chapters']:
      epub.writestr(f'OEBPS/{ch["index"]}.html', utils.render('src/open_the_book/templates/chapter.html.j2', ch))
