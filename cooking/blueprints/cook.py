from flask import Blueprint, render_template, current_app, abort, make_response
from cooking.models import Post
from cooking.utils import redirect_back
cook_bp = Blueprint('cook', __name__)


@cook_bp.route('/')
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('cook/index.html', posts=posts)


@cook_bp.route('/about')
def about():
    return render_template('cook/about.html')


@cook_bp.route('/category/<int:category_id>')
def show_category(category_id):
    return render_template('cook/category.html')


@cook_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    return render_template('cook/post.html')


@cook_bp.route('/change-theme/<theme_name>')
def change_theme(theme_name):
    if theme_name not in current_app.config['COOKING_THEMES'].keys():
        abort(404)

    response = make_response(redirect_back())
    response.set_cookie('theme', theme_name, max_age=30 * 24 * 60 * 60)
    return response
