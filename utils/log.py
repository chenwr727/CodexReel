from loguru import logger

log_file = "./logs/agent_{time:YYYY-MM-DD}.log"

logger.add(
    sink=log_file,
    rotation="00:00",
    retention="7 days",
    level="INFO",
)
