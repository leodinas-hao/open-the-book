from dataclasses import dataclass, field
from typing import Callable
from uuid import uuid4

from selenium.webdriver.chrome.webdriver import WebDriver


@dataclass
class Conf:
  '''configuration class'''

  start_url: str  # url of the first chapter
  title_func: Callable[[WebDriver], str] = field(repr=False)  # retrieve chapter title
  read_func: Callable[[WebDriver], str] = field(repr=False)  # retrieve chapter content
  next_func: Callable[[WebDriver], bool] = field(repr=False)  # navigate to next chapter if there is one, otherwise return false

  implicitly_wait: float = 10.0  # implicitly_wait time of the webdriver
  title: str = 'Unknown'
  author: str = 'Unknown'
  uid: str = field(default_factory=lambda: uuid4().hex)
