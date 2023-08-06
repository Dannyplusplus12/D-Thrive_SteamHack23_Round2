from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Post, Current_Post, Article
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('home.html', user=current_user)

@views.route('/my-blog', methods=['GET', 'POST'])
@login_required
def myBlog():
    posts = Post.query.filter_by(user_id=current_user.id)

    if request.method == 'POST':
        if request.form['btn'] == 'search':
            text = request.form.get('search-for')
            posts = Post.query.filter(Post.tags.contains(text))

    return render_template('my-blog.html', user=current_user, posts=posts)

@views.route('/about', methods=['GET', 'POST'])
@login_required
def about():

    return render_template('about.html', user=current_user)

@views.route('/contact', methods=['GET', 'POST'])
@login_required
def contact():

    return redirect(url_for('views.home'))