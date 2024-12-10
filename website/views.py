# Views related to out core app like home page, profile etc

import os
import google.generativeai as genai
from flask import Blueprint, current_app, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Post, User, Comment, Like
from werkzeug.utils import secure_filename
from . import db

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
@login_required
def home():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)


@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get('text')
        image = request.files.get('image')

        if not text:
            flash('Post cannot be empty', category='error')
        else:
            formatted_text = format_blog_post(text)
            image_url = None
            if image:
                filename = secure_filename(image.filename)
                image_path = os.path.join(current_app.root_path, 'static', 'images', filename)
                image.save(image_path)
                image_url = f"\static\images\{filename}"

            post = Post(text=formatted_text, author=current_user.id, image_url=image_url)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.home'))
        
    return render_template('create_post.html', user=current_user)

def format_blog_post(content):
    paragraphs = content.strip().split('\n\n')
    formatted_paragraphs = []
    
    for para in paragraphs:
        para_with_breaks = para.replace("\n", "<br>")
        formatted_paragraphs.append('<p>' + para_with_breaks + '</p>')
        
    return ''.join(formatted_paragraphs)


@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist.", category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted.', category='success')

    return redirect(url_for('views.home'))


@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))

    posts = user.posts
    return render_template("posts.html", user=current_user, posts=posts, username=username)

'''
views.config['MAIL_SERVER'] = 'smtp.gmail.com'
views.config['MAIL_PORT'] = 587
views.config['MAIL_USE_TLS'] = True
views.config['MAIL_USE_SSL'] = False
views.config['MAIL_USERNAME'] = 'your_email@example.com'
views.config['MAIL_PASSWORD'] = 'your_password'
views.config['MAIL_DEFAULT_SENDER'] = 'your_email@example.com'

def send_email():
    msg = Message(subject, recipients=[recipient])
    msg.body = body
    mail.send(msg)
'''

@views.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(
                text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
            # send_email()
        else:
            flash('Post does not exist.', category='error')

    return redirect(url_for('views.home'))


@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('views.home'))


@views.route("/like-post/<post_id>", methods=['POST'])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(author=current_user.id, post_id=post_id).first()

    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    return jsonify({"likes": len(post.likes), "liked": current_user.id in map(lambda x: x.author, post.likes)})


@views.route("/likes/<int:author>")
@login_required
def view_likes(author):
    user = User.query.get(author)

    if not user:
        flash('No user found.', category='error')
        return redirect(url_for('views.home'))

    user_likes = Like.query.filter_by(author=user.id).all()
    post_ids = [like.post_id for like in user_likes]
    liked_posts = Post.query.filter(Post.id.in_(post_ids)).all()

    return render_template('user_likes.html', user=current_user, posts=liked_posts, username=user.username)



@views.route("/summarise/<post_id>", methods=['POST'])
@login_required
def summarise_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    
    if not post:
        return jsonify({'error': 'Post does not exist.'}), 400

    post_text = request.form.get('post_text')

    try:
        genai.configure(api_key='AIzaSyBIAXz7OnLXZFf-NkapidwG1OwzUQIXNGg')
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"Summarize the following text in about 30% of words present:\n\n{post_text}"

        response = model.generate_content(prompt)
        summary = response.text

        return jsonify({'summary': summary})

    except Exception as e:
        return jsonify({'error': f'An error occurred while summarizing: {str(e)}'}), 500


@views.route('/recommend')
@login_required
def recommended():
    posts = get_user_recommended_posts(current_user.id)
    return render_template('recommendations.html', user=current_user, posts=posts, username=current_user.username)

def get_user_recommended_posts(user_id, limit=5):
    liked_posts_subquery = (
        Like.query
        .filter(Like.author == user_id)
        .with_entities(Like.post_id)
    )

    recommended_posts = (
        Post.query
        .filter(Post.author.in_(
            Post.query.filter(Post.id.in_(liked_posts_subquery)).with_entities(Post.author)
        ))
        .filter(Post.id.notin_(liked_posts_subquery))
        .limit(limit)
        .all()
    )

    return recommended_posts