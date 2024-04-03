from logging import config

DEFAULT_LOGGER_CONFIG = {
  'version': 1,
  'root': {
    'level': 'DEBUG',
    'handlers': ['console']
  },
  'handlers': {
    'console': {
      'formatter': 'print',
      'class': 'logging.StreamHandler',
      'level': 'WARNING',
    },
  },
  'formatters': {
    'print': {
      'format': '%(asctime)s : %(levelname)s - %(name)s : %(message)s',
      'datefmt': '%Y-%m-%dT%H:%M:%S%z',
    },
  },
  'loggers': {
    # overwrite the logging level for urllib3 library, which is a dependency of requests
    # to avoid propagated logs from it
    'urllib3': {
      'level': 'WARNING',
      'propagate': False,
    },
  },
  # https://docs.python.org/3/howto/logging.html#configuring-logging
  'disable_existing_loggers': False,
}


VERBOSE_MAP = [
  'WARNING',  # 0
  'INFO',     # 1
  'DEBUG',    # 2
]


def init_logger(verbose: int = 0):
  '''configures logger

  :param verbose (int, optional): verbosity level of console logger; default to 0; see `VERBOSE_MAP`
  '''

  # update console logging level
  DEFAULT_LOGGER_CONFIG['handlers']['console']['level'] = VERBOSE_MAP[verbose if verbose < 3 else 2]

  # set logger
  config.dictConfig(DEFAULT_LOGGER_CONFIG)
