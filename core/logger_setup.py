import sys

from loguru import logger

from config import *


logger.remove()

# Вывод в консоль
logger.add(
    sys.stdout,
    level="DEBUG",
    format="<cyan>{time:DD-MM-YYYY - HH:mm:ss}</cyan> | <blue>{level}</blue> | <level>{message}</level>",
    enqueue=True)

# Вывод в файл
logger.add('outputs/logs.log',
           level='TRACE',
           mode=f'{Config.LOGS_MODE}',
           rotation=f'{Config.LOGS_TIME} day',
           retention=5,
           format="<cyan>{time:DD-MM-YYYY - HH:mm:ss}</cyan> | <blue>{level}</blue> | {name}:{function} - <level>{message}</level>",
           enqueue=True
           )

log = logger
