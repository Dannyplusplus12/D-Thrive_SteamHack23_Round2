from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Post, Current_Post, Article
from . import db

blog = Blueprint('blog', __name__)

@blog.route('/blog', methods=['GET', 'POST'])
@login_required
def blogView():
    posts = Post.query.filter_by(status='public')

    if request.method == 'POST':
    #     type = request.form.get('sort-type')

    #     if type == 'dec':
    #         posts = Post.query.all().sort(key=cmp_to_key(lambda x, y: x.id - y.id))
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

        #mỗi lần preview thì cập nhật lại current_posts[0]
        #em để one-many, tức lưu nhiều current_posts để sau có thể nâng cấp lên kiểu.. lưu nhiều bài chưa hoàn thiện
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

# để xoá một post thì gởi request API với nội dung là id của post muốn xoá
# em đã tạo sẵn một hàm deletePost ở file base.html
# khi bấm xoá post thì gọi hàm deletePost và truyền tham số là id của post
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

# để edit một post thì anh gọi đến hàm này với <int:id> là id của post muốn edit
# một cách dễ là tạo 1 thẻ a với href="{{ url_for('views.edit', id=post['id']) }}
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

    return render_template('blog/view.html', user=current_user, post=post)