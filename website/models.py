from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.String)
    tags = db.Column(db.String)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.String(150))
    status = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments  = db.relationship('Comment')

class Current_Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.String)
    tags = db.Column(db.String)
    author = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(30))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(30))
    user_name = db.Column(db.String(150))
    posts = db.relationship('Post')
    current_posts = db.relationship('Current_Post')
    comments  = db.relationship('Comment')

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tags = db.Column(db.String)
    link_to_article = db.Column(db.String)
    img_url = db.Column(db.String)
    date = db.Column(db.DateTime(timezone=True), default=func.now())

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))