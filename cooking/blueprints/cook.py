from flask import Blueprint, render_template

cook_bp = Blueprint('cook', __name__)


@cook_bp.route('/')
def index():
    return render_template('cook/index.html')


@cook_bp.route('/about')
def about():
    return render_template('cook/about.html')


@cook_bp.route('/category/<int:category_id>')
def show_category(category_id):
    return render_template('cook/category.html')


@cook_bp.route('/post/<int:post_id>',methods=['GET','POST'])
def show_post(post_id):
    return render_template('cook/post.html')
