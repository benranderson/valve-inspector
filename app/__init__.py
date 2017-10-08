from flask import Flask
from flask_bootstrap import Bootstrap
from flask_bootstrap import __version__ as FLASK_BOOTSTRAP_VERSION
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from config import config


bootstrap = Bootstrap()
nav = Nav()
db = SQLAlchemy()
ma = Marshmallow()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    nav.init_app(app)
    db.init_app(app)
    ma.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api')

    nav.register_element('mynavbar', Navbar(
        View('Valve Inspector', '.index')
    ))

    return app
