import logging

from selenium import webdriver

from .conf import Conf


class OTB:
  '''open-the-book'''

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
      counter += 1

    driver.quit()  # close the browser

  def save(self, output_path):
    '''save the book'''

    raise NotImplementedError()
