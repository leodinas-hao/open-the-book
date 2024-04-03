import pytest

from open_the_book.logger import init_logger


@pytest.fixture(scope='session', autouse=True)
def setup():
  # init_logger(verbose=2)
  pass
