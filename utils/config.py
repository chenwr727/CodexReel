import toml

from schemas.config import Config, SubtitleConfig


def load_config(config_file: str = "config.toml") -> dict:
    with open(config_file, "r", encoding="utf-8") as f:
        config = toml.load(f)
    return config


_cfg = load_config()
config = Config.model_validate(_cfg)
config.video.subtitle = SubtitleConfig.model_validate(_cfg["subtitle"])
api_config = config.api
