import toml

from utils.schema import ApiConfig, LLMConfig, PexelsConfig, TTIConfig, TTSConfig, VideoConfig


def load_config(config_file: str = "config.toml") -> dict:
    with open(config_file, "r", encoding="utf-8") as f:
        config = toml.load(f)
    return config


_cfg = load_config()
llm = LLMConfig.model_validate(_cfg["llm"])
tts = TTSConfig.model_validate(_cfg["tts"])
tti = TTIConfig.model_validate(_cfg["tti"])
video = VideoConfig.model_validate(_cfg["video"])
api = ApiConfig.model_validate(_cfg["api"])
pexels = PexelsConfig.model_validate(_cfg["pexels"])
