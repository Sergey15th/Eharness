from flask import Flask
from dotenv import load_dotenv
import logging
logger = logging.getLogger(__name__)

load_dotenv()

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
    logger.info('server port:' + str(app.config['SERVER_PORT']))   
    # Регистрация маршрутов
    from .routes import register_routes
    register_routes(app)
    
    return app