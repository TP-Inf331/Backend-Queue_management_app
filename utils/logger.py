from loguru import logger
logger.add("logs/app_{time}.log", rotation="10 MB", retention="7 days", level="INFO")
