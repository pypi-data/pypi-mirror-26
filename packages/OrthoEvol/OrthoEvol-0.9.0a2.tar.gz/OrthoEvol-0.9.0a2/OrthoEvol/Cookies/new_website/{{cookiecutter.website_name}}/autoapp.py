"""Create an application instance."""
from flask.helpers import get_debug_flag

from {{cookiecutter.website_name}}.app import create_app
from {{cookiecutter.website_name}}.settings import DevConfig, ProdConfig

CONFIG = DevConfig if get_debug_flag() else ProdConfig

app = create_app(CONFIG)
