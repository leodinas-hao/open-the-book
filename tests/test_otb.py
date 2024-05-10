import os
import re

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

  output = 'temp/我用闲书成圣人.epub'
  OTB(conf).open(output)

  assert os.path.exists(output)


def test_otb_2_txt():
  next_link_selector = '#novelbody > div.nr_function > div:nth-child(6) > ul > li:nth-child(4) > a'
  conf = Conf(
    title='道诡异仙',
    author='狐尾的笔',
    start_url='https://m.jcdf99.com/html/33909/23421777.html',
    get_title=lambda d: d.find_element(By.CSS_SELECTOR, '#novelbody > div.nr_function > h1').text.replace('道诡异仙', '').strip(),
    read=lambda d: re.sub(re.compile(r'^\s+', re.MULTILINE), '', d.find_element(By.CSS_SELECTOR,
                          '#novelcontent').text.replace('\n\n', '\n').strip().strip('最新网址：').strip()),
    has_next=lambda d: d.find_element(
      By.CSS_SELECTOR, next_link_selector).get_attribute('href') != 'https://m.jcdf99.com/html/33909/23422827.html',
    next=lambda d: d.find_element(By.CSS_SELECTOR, next_link_selector).click(),
  )

  output = 'temp/道诡异仙.txt'
  OTB(conf).open(output)

  assert os.path.exists(output)


def test_otb_3_epub():
  next_link_selector = '#novelbody > div.nr_function > div:nth-child(6) > ul > li:nth-child(4) > a'
  conf = Conf(
    title='道诡异仙',
    author='狐尾的笔',
    # start_url='https://m.jcdf99.com/html/33909/23421777.html',
    start_url='https://m.jcdf99.com/html/33909/23422656.html',
    get_title=lambda d: d.find_element(By.CSS_SELECTOR, '#novelbody > div.nr_function > h1').text.replace('道诡异仙', '').strip(),
    read=lambda d: d.find_element(By.CSS_SELECTOR, '#novelcontent').text.replace('\n\n', '<br/>').strip().strip('最新网址：').strip(),
    has_next=lambda d: d.current_url != 'https://m.jcdf99.com/html/33909/23422826.html',
    next=lambda d: d.find_element(By.CSS_SELECTOR, next_link_selector).click(),
  )

  output = 'temp/道诡异仙.epub'
  OTB(conf).open(output, index=1747)

  assert os.path.exists(output)
