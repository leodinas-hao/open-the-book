import pytest

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

from open_the_book.conf import Conf
from open_the_book.otb import OTB


def test_otb_1():
  conf = Conf(
    start_url='https://m.lwxiaoshuo.org/shu/18229/144093149.html',
    get_title=lambda d: d.find_element(By.CSS_SELECTOR, 'h1.headline').text,
    read=lambda d: d.find_element(By.CSS_SELECTOR, 'div.content').text,
    has_next=lambda d: d.find_element(
      By.CSS_SELECTOR, '#chapter div.pager a:nth-child(3)').get_attribute('href') != 'https://m.lwxiaoshuo.org/info-18229.html',
    next=lambda d: d.find_element(By.CSS_SELECTOR, '#chapter div.pager a:nth-child(3)').click(),
  )

  otb = OTB(conf)
  otb.open()

  book = otb.book
  assert len(book['chapters']) == 2
