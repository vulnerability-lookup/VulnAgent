import os
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    try:
        import tomli as tomllib
    except ModuleNotFoundError:
        tomllib = None

DEFAULTS = {
    "xmpp": {
        "server": "localhost",
    },
    "agents": {
        "llm": {
            "name": "tool_assistant",
            "password": "password",
        },
        "chat": {
            "name": "chat_agent",
            "password": "password",
        },
        "vlai": {
            "name": "vlai_assistant",
            "password": "password",
        },
        "coordinator": {
            "name": "coordinator",
            "password": "password",
        },
    },
    "llm": {
        "provider": "qwen2.5:7b",
        "base_url": "http://localhost:11434/v1",
        "temperature": 0.7,
    },
}


def _deep_merge(base, override):
    """Recursively merge override into base."""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def _find_config_file():
    env_path = os.environ.get("VULNAGENT_CONFIG")
    if env_path:
        path = Path(env_path)
        if path.is_file():
            return path

    xdg_config = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    config_path = xdg_config / "vulnagent" / "config.toml"
    if config_path.is_file():
        return config_path

    return None


def _load_config():
    if tomllib is None:
        return DEFAULTS

    config_file = _find_config_file()
    if config_file is None:
        return DEFAULTS

    with open(config_file, "rb") as f:
        user_config = tomllib.load(f)

    return _deep_merge(DEFAULTS, user_config)


_config = None


def get_config():
    global _config
    if _config is None:
        _config = _load_config()
    return _config
