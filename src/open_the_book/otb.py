import logging

from selenium import webdriver

from .conf import Conf


class OTB:
  '''open-the-book'''

  def __init__(self, conf: Conf):
    '''init'''

    self.conf = conf
    self.logger = logging.getLogger(__name__)

    # init the driver session
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    self.driver = webdriver.Chrome(options=options)
    self.driver.implicitly_wait(conf.implicitly_wait)

    self.book = {
      'title': conf.title,
      'author': conf.author,
      'uid': conf.uid,
      'chapters': []
    }

  def open(self):
    '''open the book to fetch the contents'''

    self.driver.get(self.conf.start_url)

    counter = 0
    while True:
      self.logger.info(f'reading chapter {counter} at: {self.driver.current_url}')

      self.book['chapters'].append({
        'index': counter,
        'name': self.conf.title_func(self.driver),
        'content': self.conf.read_func(self.driver),
      })

      if not self.conf.next_func(self.driver):
        break

      counter += 1

  def save(self, output_path):
    '''save the book'''

    raise NotImplementedError()
