import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(levelname)s - %(message)s')
handler = logging.StreamHandler()

handler.setFormatter(formatter)
logger.addHandler(handler)
