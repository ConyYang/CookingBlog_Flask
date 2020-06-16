from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField,\
    ValidationError, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, Email, URL, Optional
from cooking.models import Category


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class RecipeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired, Length(1, 60)])
    category = SelectField('Category', coerce=int, default=1)
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.label) for category in Category.query.order_by(Category.name).all()]


class CategoryForm(FlaskForm):
    label = StringField('Label', validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField()

    def validate_label(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('Label already in use')


class CommentForm(FlaskForm):
    author = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 254)])
    site = StringField('Site', validators=[Optional(), URL(), Length(0, 255)])
    # optional, can be empty, length can be zero
    body = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField()


class AdminCommentForm(FlaskForm):
    author = HiddenField()
    email = HiddenField()
    site = HiddenField()
