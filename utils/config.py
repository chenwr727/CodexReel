import toml

from schemas.config import Config


def load_config(config_file: str = "config.toml") -> dict:
    with open(config_file, "r", encoding="utf-8") as f:
        config = toml.load(f)
    return config


_cfg = load_config()
config = Config.model_validate(_cfg)
api_config = config.api
