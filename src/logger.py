import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('logs.log')
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


def log_message(message):
    logging.info(message)


def log_error(message):
    logging.error(message)
