from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Post, Current_Post, Article
from . import db

admin = Blueprint('admin', __name__)

@admin.route('/admin/queue', methods=['GET', 'POST'])
@login_required
def queue():

    if current_user.role != 'admin':
        return redirect(url_for('views.home'))

    posts = Post.query.filter_by(status='wait')

    return render_template('admin/queue.html', user=current_user, posts=posts)

@admin.route('/admin/queue/<int:id>/approve', methods=['GET', 'POTS'])
@login_required
def approve(id):

    if current_user.role != 'admin':
        return redirect(url_for('views.home'))

    post = Post.query.get(id)

    post.status = 'public'
    db.session.commit()

    return redirect(url_for('admin.queue'))

@admin.route('/admin/queue/<int:id>/delete', methods=['GET', 'POTS'])
@login_required
def delete(id):

    if current_user.role != 'admin':
        return redirect(url_for('views.home'))

    post = Post.query.get(id)

    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('admin.queue'))