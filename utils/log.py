from loguru import logger


logger.add(
    "./logs/agent_{time:YYYY-MM-DD}.log",
    rotation="00:00",
    retention="7 days",
    level="INFO",
    format="{time} - {level} - {message}",
)
