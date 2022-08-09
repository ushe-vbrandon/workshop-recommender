import logging

from pydantic import BaseSettings

class Settings(BaseSettings):
    DEBUG: bool = True
    LOGLEVEL: str = 'INFO'
    LOGFILE: str = 'systemdat.log'

    DATADIR: str = 'data'
   
config = Settings()

def log_setup(loglevel, logfile):
    if loglevel == 'DEBUG':
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(
        format='[%(asctime)s] %(levelname)s | %(name)s: %(message)s',
        filename=logfile,
        level=level)


log_setup(config.LOGLEVEL, config.LOGFILE)
logger = logging.getLogger(__name__)
logger.info(f"Configured logging loglevel {config.LOGLEVEL}")
