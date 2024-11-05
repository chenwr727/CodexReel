import toml


def load_config(tasks_file: str = "config.toml"):
    with open(tasks_file, "r", encoding="utf-8") as f:
        config = toml.load(f)
    return config
