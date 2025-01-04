import logging
import sys

logger = logging.getLogger('pandora')
logger.setLevel(logging.INFO)

logger_formatter = logging.Formatter(logging.BASIC_FORMAT)

logger_handler = logging.StreamHandler(sys.stdout)
logger_handler.setFormatter(logger_formatter)

logger.addHandler(logger_handler)
