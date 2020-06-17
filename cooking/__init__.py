from flask import Flask
from flask import render_template, request
from cooking.settings import configuration
import os
from cooking.blueprints.admin import admin_bp
from cooking.blueprints.cook import cook_bp
from cooking.blueprints.auth import auth_bp
from cooking.models import Admin, Category, Comment, Post, Link
from cooking.extensions import bootstrap, db, login_manager, csrf, ckeditor, mail, moment, toolbar, migrate

from flask_login import current_user
from flask_sqlalchemy import get_debug_queries
from flask_wtf.csrf import CSRFError

import click
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def make_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('cooking')
    app.config.from_object(configuration[config_name])

    register_blue_prints(app)  # blueprints
    register_commands(app)  # customer shell commands
    register_errors(app)  # error handler function
    register_extensions(app)  # extension init
    register_logging(app)  # log
    register_shell_context(app)  # shell context
    register_template_context(app)  # template context
    register_request_handlers(app)
    return app


def register_blue_prints(app):
    app.register_blueprint(cook_bp)  # front end
    app.register_blueprint(auth_bp, )  # authenticate account
    app.register_blueprint(admin_bp, url_prefix='/admin')  # back end


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    toolbar.init_app(app)
    migrate.init_app(app, db)

def register_logging(app):
    class RequestFormatter(logging.Formatter):

        def format(self, record):
            record.url = request.url
            record.remote_addr = request.remote_addr
            return super(RequestFormatter, self).format(record)

    request_formatter = RequestFormatter(
        '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
        '%(levelname)s in %(module)s: %(message)s'
    )

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler(os.path.join(basedir, 'cooking.log'),
                                       maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    mail_handler = SMTPHandler(
        mailhost=app.config['MAIL_SERVER'],
        fromaddr=app.config['MAIL_USERNAME'],
        toaddrs=['ADMIN_EMAIL'],
        subject='Bluelog Application Error',
        credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']))
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(request_formatter)

    if not app.debug:
        app.logger.addHandler(mail_handler)
        app.logger.addHandler(file_handler)


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, Admin=Admin, Post=Post, Category=Category, Comment=Comment, Link = Link)


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.label).all()
        links = Link.query.order_by(Link.name).all()
        if current_user.is_authenticated:
            unread_comments = Comment.query.filter_by(reviewed=False).count()
        else:
            unread_comments = None
        return dict(
            admin=admin, categories=categories,
            links=links, unread_comments=unread_comments)


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html', description=e.description), 400


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


def register_request_handlers(app):
    @app.after_request
    def query_profiler(response):
        for q in get_debug_queries():
            if q.duration >= app.config['COOKING_SLOW_QUERY_THRESHOLD']:
                app.logger.warning(
                    'Slow query: Duration: %fs\n Context: %s\nQuery: %s\n '
                    % (q.duration, q.context, q.statement)
                )
        return response
