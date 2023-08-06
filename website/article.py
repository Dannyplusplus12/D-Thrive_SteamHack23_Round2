from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Post, Current_Post, Article
from . import db

article = Blueprint('article', __name__)

@article.route('/article', methods=['GET', 'POST'])
@login_required
def articleView():
    articles = Article.query.all()
    list = []
    n = len(articles)
    for i in range(0, n, 2):
        pair = {'article1': [], 'article2': []}
        if i+1 < n:
            pair['article1'] = [articles[i].link_to_article, articles[i].img_url,articles[i].tags,articles[i].date,articles[i].title,articles[i].id]
            pair['article2'] = [articles[i+1].link_to_article, articles[i+1].img_url,articles[i+1].tags,articles[i+1].date,articles[i+1].title,articles[i+1].id]
            list.append(pair)
        else:
            list.append({'article1': [articles[i].link_to_article, articles[i].img_url,articles[i].tags,articles[i].date,articles[i].title,articles[i].id]})
    return render_template('article/article.html', user=current_user, list=list)

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

    db.session.delete(current_article)
    db.session.commit()
    return redirect(url_for('article.articleView'))

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