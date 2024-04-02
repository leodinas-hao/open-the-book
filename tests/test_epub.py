from zipfile import ZipFile

import pytest

container_xml = '''<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
'''


@pytest.mark.parametrize('output', [
  'temp/simpe_epub.epub'
])
def test_simple_epub(output):
  # https://www.manuel-strehl.de/simple_epub_ebooks_with_python
  with zipfile.ZipFile(output, 'w') as epub:
    # The first file must be named "mimetype"
    epub.writestr("mimetype", "application/epub+zip")
