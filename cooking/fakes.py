# create fake stats
from faker import Faker

from cooking.models import *
from cooking.extensions import db
from django.db import IntegrityError

import random

faker = Faker()


def fake_admin():
    admin_cony = Admin(
        username='Cony Admin',
        blog_title='Cooking Blog',
        blog_sub_title='This is my first Cooking Blog !',
        name='Yu Cony',
        about='A COOKING programmer'
    )
    db.session.add(admin_cony)
    db.session.commit()


category_list = ['Cantonese', 'Dessert', 'French',
                 'Japanese', 'Si Chuan', 'Thailand',
                 'Western']


def add_categories(count=7):
    for i in range(count):
        category = Category(label=category_list[i])
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


titles_list = [
    'Xiao Long Bao',
    'Tiramisu',
    'Baked Snail',
    'Beef Ramen',
    'Twice Cooked Spicy Pork Slices',
    'Curried crab',
    'Tomato Pasta',

    'Char siew',
    'Rice Cake',
    'Tomato Pasta',
    'Su Shi',
    'Hot Garlic Source Eggplant',
    'Grilled Steamed Lobster',
    'Onion Steak',

    'Scrambled egg with shrimps',
    'Ice Cream',
    'Potato Salad',
    'Dumplings'
]


def fake_recipes(count=12):
    for i in range(count):
        post = Post(
            title=titles_list[i],
            content=faker.text(),
            category=Category.query.get(i % len(category_list)+1),
            timestamp=faker.date_time_this_year()
        )
        db.session.add(post)
    db.session.commit()


def fake_comments(count=500):
    # Reviewed comments
    for i in range(count):
        comment = Comment(
            author=faker.name(),
            email=faker.email(),
            site=faker.url(),
            content=faker.sentence(),
            timestamp=faker.date_time_this_year(),
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

    # Not reviewed Comments
    notReviewed_comments = int(count * 0.1)
    for i in range(notReviewed_comments):
        comment = Comment(
            author=faker.name(),
            email=faker.email(),
            site=faker.url(),
            content=faker.sentence(),
            timestamp=faker.date_time_this_year(),
            reviewed=False,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

    # Admin Comments
    admin_comments = int(count * 0.05)
    for i in range(admin_comments):
        comment = Comment(
            author='Cony Yang',
            email='ConyYang@cooking.com',
            site='cooking.com',
            content=faker.sentence(),
            timestamp=faker.date_time_this_year(),
            from_admin=True,
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

    db.session.commit()

    # Reply
    for i in range(int(count * 0.15)):
        comment = Comment(
            author=faker.name(),
            email=faker.email(),
            site=faker.url(),
            content=faker.sentence(),
            timestamp=faker.date_time_this_year(),
            reviewed=True,
            replied=Comment.query.get(random.randint(1, Comment.query.count())),
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()


def fake_links():
    Github = Link(name='Github', url='https://github.com/ConyYang')
    linkedin = Link(name='LinkedIn', url='https://www.linkedin.com/in/yubeicony')
    db.session.add_all([Github, linkedin])
    db.session.commit()
