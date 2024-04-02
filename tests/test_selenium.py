import pytest

from selenium import webdriver


@pytest.mark.parametrize('url', [
  'https://www.google.com/'
])
def test_open_url(url):
  # ensure using headless mode
  # https://www.selenium.dev/blog/2023/headless-is-going-away/
  options = webdriver.ChromeOptions()
  options.add_argument("--headless=new")
  driver = webdriver.Chrome(options=options)
  driver.get(url)
  assert 'Google' in driver.title
  driver.quit()
