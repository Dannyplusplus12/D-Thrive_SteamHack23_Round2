from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, Current_Post
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # if request.method == 'POST':
    #     note = request.form.get('note')

    #     if len(note) < 1:
    #         flash('Note can\'t be empty!', category='error')
    #     else:
    #         new_note = Note(data=note, user_id=current_user.id)
    #         db.session.add(new_note)
    #         db.session.commit()
    #         flash('Note Added!', category='success')
    return render_template('home.html', user=current_user)

# @views.route('/delete-note', methods=['POST'])
# def delete_note():
#     data = json.loads(request.data)
#     noteId = data['noteId']
#     note = Note.query.get(noteId)
#     if note:
#         if note.user_id == current_user.id:
#             db.session.delete(note)
#             db.session.commit()
#     return json.dumps({})

@views.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        #mỗi lần preview thì cập nhật lại current_posts[0]
        #em để one-many, tức lưu nhiều current_posts để sau có thể nâng cấp lên kiểu.. lưu nhiều bài chưa hoàn thiện
        try:
            db.session.delete(current_user.current_posts[0])
        except:
            pass
        current_post = Current_Post(title=title, content=content, user_id=current_user.id)
        db.session.add(current_post)
        db.session.commit()

        return redirect(url_for('views.preview'))

    try:
        current_post = current_user.current_posts[0]
        title = current_post.title
        content = current_post.content
    except:
        title = ""
        content = ""
    return render_template('create.html', user=current_user, title=title, content=content)


@views.route('/preview', methods=['GET', 'POST'])
def preview():
    current_post = current_user.current_posts[0]
    title = current_post.title
    content = current_post.content

    return  render_template('preview.html', user=current_user, title=title, content=content)