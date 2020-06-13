from flask import Flask
from cooking.settings import configuration
import os
from cooking.blueprints.admin import admin_bp
from cooking.blueprints.cook import cook_bp
from cooking.blueprints.auth import auth_bp
from cooking.extensions import *


def make_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('Cooklog')
    app.config.from_object(configuration[config_name])

    app.register_blueprint(cook_bp)  # front end
    app.register_blueprint(auth_bp, )  # authenticate account
    app.register_blueprint(admin_bp, url_prefix='/admin')  # back end

    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)

    return app

