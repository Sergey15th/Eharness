from app import create_app
from flask import Flask
import os
from flask.signals import request_started
from app.models import CodesTypes

# Логгер в файл:
import logging
from logging.handlers import RotatingFileHandler
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
logFile = 'productview.log'
my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024,
                                 backupCount=2, encoding=None, delay=0)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(my_handler)
# Консольный логгер:
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(log_formatter)
logger.addHandler(consoleHandler)
# //// Логгер

app = create_app()
_app_started = False

def run_on_first_request(sender, **extra):
    global _app_started
    if not _app_started:
        _app_started = True
        logger.info("Первый запрос получен! Выполняю инициализацию...")
        # Ваш код здесь
        indexes = CodesTypes.get_types()
        logger.info(str(CodesTypes.indexes))

# Подключаем сигнал к первому запросу
request_started.connect(run_on_first_request, app)
if __name__ == '__main__':
    app.run(
        host=app.config['SERVER_HOST'],
        port=app.config['SERVER_PORT'],
        debug=app.config['DEBUG']
    )