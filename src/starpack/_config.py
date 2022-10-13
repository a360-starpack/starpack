from pathlib import Path
import typer
from pydantic import BaseSettings, root_validator
from typing import Optional

# Configuration for the app name
APP_NAME = "starpack"
APP_DIR = Path(typer.get_app_dir(APP_NAME))
ENV_FILE = APP_DIR / "starpack.config"
BASE_DIR = Path(__file__).resolve().parent

# Generate the configuration folder and file if it doesn't exist
APP_DIR.mkdir(exist_ok=True, parents=True)
ENV_FILE.touch()


class Settings(BaseSettings):
    engine_port: int = 1976
    engine_image: str = "starpack/starpack-engine:latest"
    app_name: str = APP_NAME
    app_dir: Path = APP_DIR
    plugins_dir: Optional[Path] = None

    @root_validator
    def ensure_plugins_dir(cls, values):
        if not values["plugins_dir"]:
            values["plugins_dir"] = values["app_dir"] / "plugins"
        values["plugins_dir"].mkdir(exist_ok=True, parents=True)

        return values

    class Config:
        env_file = str(ENV_FILE)
        env_file_encoding = "utf-8"


settings = Settings()
