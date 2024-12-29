from utils.config import load_config

config = load_config()


class Settings:
    DATABASE_URL = config["api"]["database_url"]
    APP_PORT = config["api"]["app_port"]
    MAX_CONCURRENT_TASKS = config["api"]["max_concurrent_tasks"]
    TASK_TIMEOUT_SECONDS = config["api"]["task_timeout_seconds"]


settings = Settings()
