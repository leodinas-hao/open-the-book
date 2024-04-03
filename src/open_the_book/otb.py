import logging
from time import sleep
from zipfile import ZipFile

from selenium import webdriver

from .conf import Conf
from .utils import read, render


class OTB:
  '''open the ebook from internet and save as epub'''

  def __init__(self, conf: Conf):
    '''init'''

    self.logger = logging.getLogger(__name__)
    self.conf = conf
    self.book = {
      'title': conf.title,
      'author': conf.author,
      'uid': conf.uid,
      'chapters': []
    }

  def open(self):
    '''open the book to fetch the contents'''

    # init the driver session
    self.logger.info('init the driver session')
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(self.conf.implicitly_wait)

    # open the first chapter
    driver.get(self.conf.start_url)

    counter = 0
    while True:
      self.logger.info(f'reading chapter {counter} at: {driver.current_url}')

      self.book['chapters'].append({
        'index': counter,
        'name': self.conf.get_title(driver),
        'content': self.conf.read(driver),
      })

      if not self.conf.has_next(driver):
        break

      self.conf.next(driver)  # navigate to next chapter
      sleep(self.conf.throttling)  # throttle
      counter += 1

    driver.quit()  # close the browser

  def save(self, output_path: str):
    '''save the book'''

    self.logger.info(f'saving the book to: {output_path}')

    with ZipFile(output_path, 'w') as epub:
      # write the mimetype & other default files
      epub.writestr('mimetype', read('templates/mimetype'))
      epub.writestr('META-INF/container.xml', read('templates/container.xml'))
      epub.writestr('OEBPS/style.css', self.conf.style_css if self.conf.style_css else read('templates/style.css'))

      epub.writestr('OEBPS/book-toc.html', render('templates/book-toc.html.j2', self.book))
      epub.writestr('OEBPS/toc.ncx', render('templates/toc.ncx.j2', self.book))
      epub.writestr('OEBPS/content.opf', render('templates/content.opf.j2', self.book))
      epub.writestr('OEBPS/cover.html', render('templates/cover.html.j2', self.book))
      for ch in self.book['chapters']:
        epub.writestr(f'OEBPS/{ch["index"]}.html', render('templates/chapter.html.j2', ch))
