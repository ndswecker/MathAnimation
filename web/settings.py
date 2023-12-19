import os
import pathlib

SECRET_KEY = os.environ["SECRET_KEY"]

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent
SCENES_DIR = ROOT_DIR / "scenes"
WEB_DIR = ROOT_DIR / "web"
STATIC_DIR = WEB_DIR / "static"
MEDIA_DIR = STATIC_DIR / "media"
DEFAULT_VIDEO_DIR = MEDIA_DIR / "default"
DYNAMIC_VIDEO_DIR = MEDIA_DIR / "dynamic"
