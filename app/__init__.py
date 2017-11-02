from flask import Flask
from flask_bootstrap import Bootstrap
from flask_bootstrap import __version__ as FLASK_BOOTSTRAP_VERSION
from flask_sqlalchemy import SQLAlchemy
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from config import config


bootstrap = Bootstrap()
nav = Nav()
db = SQLAlchemy()


def create_app(config_name):
    """Create an application instance."""
    app = Flask(__name__)

    # apply configuration
    app.config.from_object(config[config_name])

    # initialize extensions
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    nav.init_app(app)
    db.init_app(app)

    # register blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api_v1 import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    # register navigation bar
    nav.register_element('mynavbar', Navbar(
        View('Valve Inspector', '.index')
    ))

    return app
