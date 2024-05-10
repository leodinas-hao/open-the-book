import logging
from time import sleep
import os
import shutil
from zipfile import ZipFile

from selenium import webdriver

from .conf import Conf
from .utils import prefix_path, read, render, write


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

  def open(self, save_to: str, *, index: int = 0):
    '''fetch the contents of the book and save to the specified path

    :param str save_to: path to save the book; supports `*.epub` or `*.txt` format
    :param int index: index of the first chapter, default 0
    '''

    # prepare saving
    if save_to.endswith('.txt'):
      save_path = save_to
    elif save_to.endswith('.epub'):
      # create a temporary directory for epub files
      save_dir = self.init_epub(save_to)
      save_path = os.path.join(save_dir, 'OEBPS')
      toc_path = os.path.join(save_path, 'book-toc.txt')
    else:
      raise ValueError(f'unknown format: {save_to}')

    # init the driver session
    self.logger.info('init the driver session')
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(self.conf.implicitly_wait)

    # open the first chapter
    driver.get(self.conf.start_url)

    counter = index
    while True:
      self.logger.info(f'reading chapter {counter} at: {driver.current_url}')

      content = self.conf.read(driver)
      chapter = self.conf.get_title(driver)

      if save_to.endswith('.txt'):
        # write to a txt file
        write(save_path, f'{chapter}\n\n{content}\n\n', mode='a')
      else:
        # write to the temporary directory
        # update the temporary toc: add new chapter to a new line
        write(toc_path, f'{counter}|{chapter}\n', mode='a')
        # write the chapter content
        write(os.path.join(save_path, f'{counter}.html'),
              render(prefix_path('templates/chapter.html.j2'), {'index': counter, 'name': chapter, 'content': content}),
              mode='w')

      if not self.conf.has_next(driver):
        # no more chapters
        # if saving epub, finish building of toc, and zip all contents
        self.save_epub(save_dir, toc_path)
        break

      self.conf.next(driver)  # navigate to next chapter
      sleep(self.conf.throttling)  # throttle
      counter += 1

    driver.quit()  # close the browser

  def init_epub(self, save_to: str) -> str:
    '''init epub temporary directory structure

    :param str save_to: file path
    :returns str: path to the temporary directory
    '''

    # create a temporary directory first, then save all chapters into it
    save_dir = os.path.dirname(save_to)
    save_dir = os.path.join(save_dir, os.path.basename(save_to).rstrip('.epub'))
    os.makedirs(save_dir, exist_ok=True)

    # create the epub directory structure
    write(os.path.join(save_dir, 'mimetype'), read(prefix_path('templates/mimetype')), mode='w')
    os.makedirs(os.path.join(save_dir, 'META-INF'), exist_ok=True)
    write(os.path.join(save_dir, 'META-INF/container.xml'), read(prefix_path('templates/container.xml')), mode='w')
    save_content_dir = os.path.join(save_dir, 'OEBPS')
    os.makedirs(save_content_dir, exist_ok=True)
    write(os.path.join(save_content_dir, 'cover.html'), render(prefix_path('templates/cover.html.j2'), self.book), mode='w')
    write(os.path.join(save_content_dir, 'style.css'), self.conf.style_css if self.conf.style_css else read(prefix_path('templates/style.css')), mode='w')

    return save_dir

  def save_epub(self, save_dir: str, toc: str):
    '''save the epub from the temporary directory

    :param str save_dir: the directory path containing the epub files
    :param str toc: toc file path
    '''

    save_path = save_dir + '.epub'
    # read the toc file to build toc files: OEBPS/book-toc.html, OEBPS/toc.ncx, OEBPS/content.opf
    toc_ls = read(toc).splitlines()
    self.book['chapters'] = [{'index': l.split('|', 1)[0], 'name': l.split('|', 1)[1]} for l in toc_ls if l]
    write(os.path.join(save_dir, 'OEBPS/book-toc.html'), render(prefix_path('templates/book-toc.html.j2'), self.book), mode='w')
    write(os.path.join(save_dir, 'OEBPS/toc.ncx'), render(prefix_path('templates/toc.ncx.j2'), self.book), mode='w')
    write(os.path.join(save_dir, 'OEBPS/content.opf'), render(prefix_path('templates/content.opf.j2'), self.book), mode='w')

    # zip all contents
    with ZipFile(save_path, 'w') as epub:
      for root, _, files in os.walk(save_dir):
        for file in files:
          epub.write(os.path.join(root, file), arcname=os.path.join(root.replace(save_dir, ''), file))

    # delete the temporary directory
    # shutil.rmtree(save_dir)
