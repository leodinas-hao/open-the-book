from dataclasses import dataclass, field
from typing import Callable
from uuid import uuid4

from selenium.webdriver import Chrome


@dataclass
class Conf:
  '''configuration class'''

  start_url: str  # url of the first chapter
  get_title: Callable[[Chrome], str] = field(repr=False)  # retrieve chapter title
  read: Callable[[Chrome], str] = field(repr=False)  # retrieve chapter content
  has_next: Callable[[Chrome], bool] = field(repr=False)  # check if there is next chapter
  next: Callable[[Chrome], None] = field(repr=False)  # navigate to next chapter

  implicitly_wait: float = 10.0  # implicitly_wait time of the webdriver
  title: str = 'Unknown'
  author: str = 'Unknown'
  uid: str = field(default_factory=lambda: uuid4().hex)
