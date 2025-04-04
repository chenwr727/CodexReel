from typing import Optional

import toml

from schemas.config import Config, PromptConfig, PromptSource


def load_config(config_file: str = "config.toml") -> dict:
    with open(config_file, "r", encoding="utf-8") as f:
        config = toml.load(f)
    return config


def get_prompt_config(prompt_source: Optional[str] = None) -> PromptConfig:
    config_mapping = {k.value: f"./prompts/{k.value}.toml" for k in PromptSource}
    default_config_path = "./prompts/podcast.toml"
    config_path = config_mapping.get(prompt_source, default_config_path)

    try:
        config = load_config(config_path)
    except Exception as e:
        raise RuntimeError(f"Failed to load config from {config_path}: {e}")

    return PromptConfig.model_validate(config)


_cfg = load_config()
config = Config.model_validate(_cfg)
api_config = config.api
