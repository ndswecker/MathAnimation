from flask import Flask

from web import index
from web import animations


def create_app(settings: str = "web.settings"):
    app = Flask(__name__)
    app.config.from_object(settings)
    register_blueprints(app)
    return app


def register_blueprints(app):
    app.register_blueprint(index.router)
    app.register_blueprint(animations.router)
