from zipfile import ZipFile

import pytest


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
