from typing import Optional

import toml

from schemas.config import Config, PromptConfig, PromptSource


def load_config(config_file: str = "config.toml") -> dict:
    with open(config_file, "r", encoding="utf-8") as f:
        config = toml.load(f)
    return config


def get_prompt_config(copywriter_type: Optional[str] = None) -> PromptConfig:
    config_mapping = {
        PromptSource.crosstalk: "./prompts/crosstalk.toml",
        PromptSource.talkshow: "./prompts/talkshow.toml",
        PromptSource.book: "./prompts/book.toml",
    }

    default_config_path = "./prompts/crosstalk.toml"

    config_path = config_mapping.get(copywriter_type, default_config_path)

    try:
        config = load_config(config_path)
    except Exception as e:
        raise RuntimeError(f"Failed to load config from {config_path}: {e}")

    return PromptConfig.model_validate(config)


_cfg = load_config()
config = Config.model_validate(_cfg)
api_config = config.api
