from flask import Flask
from dotenv import load_dotenv

load_dotenv()

# Логгер в файл:
import logging
from logging.handlers import RotatingFileHandler
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
logFile = 'robot.log'
my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024,
                                 backupCount=2, encoding=None, delay=0)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(my_handler)
# Консольный логгер:
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(log_formatter)
logger.addHandler(consoleHandler)
# //// Логгер

def create_app(config_name=None):
    if config_name is None:
        config_name = 'default'
    
    app = Flask(__name__)
    
    # Конфигурация
    from .config import config
    logger.info('***CONFIG NAME***' + config_name) 
    app.config.from_object(config[config_name])
    logger.info('***CONFIG***')    
    logger.info(config['default'])
    logger.info('server host:' + app.config['SERVER_HOST'])
    logger.info('server port:' + app.config['SERVER_PORT'])   
    # Регистрация маршрутов
    from .routes import register_routes
    register_routes(app)
    
    return app