from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Post, Current_Post, Article
from . import db

article = Blueprint('article', __name__)

@article.route('/article', methods=['GET', 'POST'])
@login_required
def articleView():
    articles = Article.query.all()
    return render_template('article/article.html', user=current_user, articles=articles)

@article.route('/article/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        if request.form['btn'] == 'create':
            link_to_article = request.form.get('link_to_article')
            img_url = request.form.get('img_url')
            tags = request.form.get('tags')
            title = request.form.get('title')
            new_article = Article(link_to_article=link_to_article, img_url=img_url, tags=tags, title=title)
            db.session.add(new_article)
            db.session.commit()

            return redirect(url_for('article.articleView'))

    return render_template('article/create.html', user=current_user)

@article.route('/article/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id):
    current_article = Article.query.get(id)

    if current_user.role == 'admin':
        pass
    else:
        return redirect(url_for('article.articleView'))


    if request.method == 'POST':
        db.session.delete(current_article)
        db.session.commit()
        return redirect(url_for('article.articleView'))

    return render_template("/article/delete.html", user=current_user, article=current_article)

@article.route('/article/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    current_article = Article.query.get(id)

    if current_user.role == 'admin':
        pass
    else:
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        current_article.link_to_article = request.form.get('link_to_article')
        current_article.img_url = request.form.get('link_to_img_urlarticle')
        current_article.tags = request.form.get('tags')
        current_article.title = request.form.get('title')
        
        db.session.commit()
        return redirect(url_for('article.articleView'))

    return render_template("article/edit.html", user=current_user, article=current_article)