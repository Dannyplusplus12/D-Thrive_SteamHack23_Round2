from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Post, Current_Post, Comment
from . import db

blog = Blueprint('blog', __name__)

@blog.route('/blog', methods=['GET', 'POST'])
@login_required
def blogView():
    posts = Post.query.filter_by(status='public')
    if request.method == 'POST':

        if request.form['btn'] == 'search':
            text = request.form.get('search-for')
            posts = Post.query.filter(Post.tags.contains(text))

    return render_template('blog/blog.html', user=current_user, posts=posts)

@blog.route('/blog/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        tags = request.form.get('tags')

        try:
            db.session.delete(current_user.current_posts[0])
        except:
            pass

        current_post = Current_Post(title=title, content=content, tags=tags, user_id=current_user.id, author=current_user.user_name)
        db.session.add(current_post)
        db.session.commit()

        return redirect(url_for('blog.preview'))

    try:
        current_post = current_user.current_posts[0]
    except:
        current_post = Current_Post(title="", content="", tags="")

    return render_template('blog/create.html', user=current_user, post=current_post)

@blog.route('/blog/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id):
    post = Post.query.get(id)

    if current_user.role == 'admin' or post.user_id == current_user.id:
        pass
    else:
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('blog.blogView'))

    return render_template("blog/delete.html", user=current_user, post=post)

@blog.route('/blog/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get(id)

    if current_user.role == 'admin' or post.user_id == current_user.id:
        pass
    else:
        return redirect(url_for('views.home'))

    status = (post.status == 'public') 

    if request.method == 'POST':
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        post.tags = request.form.get('tags')

        status = 'public' if request.form.get('check-status') == 'on' else 'private'
        post.status = status
        
        db.session.commit()
        return redirect(url_for('blog.blogView'))

    return render_template("blog/edit.html", user=current_user, post=post, status=status)
    
@blog.route('/blog/preview', methods=['GET', 'POST'])
@login_required
def preview():
    post = current_user.current_posts[0]

    if request.method == 'POST':
        if request.form['btn'] == 'post':
            new_post = Post(title=post.title, content=post.content, tags=post.tags, user_id=current_user.id, author=current_user.user_name, status="wait")
            db.session.add(new_post)
            db.session.commit()

            return redirect(url_for('blog.blogView'))

    return render_template('blog/preview.html', user=current_user, post=post)

@blog.route('/blog/<int:id>/view', methods=['GET', 'POST'])
@login_required
def view(id):
    post = Post.query.get(id)
    if request.method == 'POST':
        if request.form['btn'] == 'comment':
            new_comment = Comment(content=request.form['comment-content'], user_id=current_user.id, post_id=id)
            db.session.add(new_comment)
            db.session.commit()

    list = []
    for comment in post.comments:
        list.append({'user_name': User.query.get(comment.user_id).user_name, 'content': comment.content, 'id': comment.id})

    return render_template('blog/view.html', user=current_user, post=post, comment_list=list)

@blog.route('/blog/<int:id>/<int:post_id>/delete-comment', methods=['GET', 'POST'])
@login_required
def deleteComment(id, post_id):
    comment = Comment.query.get(id)

    if current_user.role == 'admin' or comment.user_id == current_user.id:
        pass
    else:
        return redirect(url_for('views.home'))
    
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('blog.view', id=post_id))