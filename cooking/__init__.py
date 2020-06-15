from flask import Flask
from flask import render_template
from cooking.settings import configuration
import os
from cooking.blueprints.admin import admin_bp
from cooking.blueprints.cook import cook_bp
from cooking.blueprints.auth import auth_bp
from cooking.extensions import *
import click


def make_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('Cooklog')
    app.config.from_object(configuration[config_name])

    register_blue_prints(app)  # blueprints
    register_commands(app)  # customer shell commands
    register_errors(app)  # error handler function
    register_extensions(app)  # extension init
    register_logging(app)  # log
    register_shell_context(app)  # shell context
    register_template_context(app)  # template context
    return app


def register_blue_prints(app):
    app.register_blueprint(cook_bp)  # front end
    app.register_blueprint(auth_bp, )  # authenticate account
    app.register_blueprint(admin_bp, url_prefix='/admin')  # back end


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)


def register_logging(app):
    pass


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)


def register_template_context(app):
    pass


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/40-0.html'), 400


def register_commands(app):
    @app.cli.command()
    @click.option('--category', default=7, help='No. of Cooking Categories, default is 7.')
    @click.option('--recipe', default=10, help='No. of recipes, default is 10.')
    @click.option('--comment', default=80, help='No of comments, defualt is 80')
    def forge(category, recipe, comment):
        """
        Generate half fake database
        """
        from cooking.fakes import fake_admin, fake_comments, fake_recipes, add_categories
        db.drop_all()
        db.create_all()

        click.echo('Generating the administrator...')
        fake_admin()

        click.echo('Generating %d categories...' % category)
        add_categories(category)

        click.echo('Generating %d recipes...' % recipe)
        fake_recipes(recipe)

        click.echo('Generating %d comments...' % comment)
        fake_comments(comment)

        click.echo('Done')
