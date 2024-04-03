import os

import pytest
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

from open_the_book.conf import Conf
from open_the_book.otb import OTB


def test_otb_1():
  conf = Conf(
    title='我用闲书成圣人',
    author='出走八万里',
    start_url='https://m.lwxiaoshuo.org/shu/18229/117817287.html',
    get_title=lambda d: d.find_element(By.CSS_SELECTOR, 'h1.headline').text,
    read=lambda d: d.find_element(By.CSS_SELECTOR, 'div.content').text.replace('\n', '<br/>'),
    has_next=lambda d: d.find_element(
      By.CSS_SELECTOR, '#chapter div.pager a:nth-child(3)').get_attribute('href') != 'https://m.lwxiaoshuo.org/info-18229.html',
    next=lambda d: d.find_element(By.CSS_SELECTOR, '#chapter div.pager a:nth-child(3)').click(),
  )

  otb = OTB(conf)
  otb.open()

  book = otb.book
  assert len(book['chapters']) > 0

  output = 'temp/我用闲书成圣人.epub'
  otb.save(output)
  assert os.path.exists(output)
