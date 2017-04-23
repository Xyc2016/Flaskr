from datetime import datetime
from flask import Flask, render_template, Blueprint, redirect, url_for,request
from sqlalchemy import func
from os import path
from Flaskr.models import db, Post, Tag, Comment, User, tags
from Flaskr.forms import CommentForm

blog_blueprint = Blueprint('blog',
                           __name__,
                           template_folder=path.join(path.pardir, 'templates', 'blog'),
                           static_folder= path.join(path.pardir,'static'),
                           url_prefix='/blog')


def sidebar_data():
    recent = Post.query.order_by(
        Post.date.desc()
    ).limit(5).all()
    top_tags = db.session.query(
        Tag, func.count(tags.c.post_id).label('total')
    ).join(
        tags
    ).group_by(Tag).order_by('total DESC').limit(5).all()
    return recent, top_tags


@blog_blueprint.route('/')
@blog_blueprint.route('/<int:page>')
def home(page=1):
    posts = Post.query.order_by(
        Post.date.desc()
    ).paginate(page, 10)
    recent, top_tags = sidebar_data()

    return render_template(
        'blog/index.html',
        posts=posts,
        recent=recent,
        top_tags=top_tags
    )


@blog_blueprint.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        print('validate')
        new_comment = Comment()
        new_comment.name = form.name.data
        new_comment.text = form.text.data
        new_comment.post_id = post_id
        new_comment.date = datetime.now()
        db.session.add(new_comment)
        db.session.commit()
    the_post = Post.query.get_or_404(post_id)
    tags = the_post.tags
    comments = the_post.comments.order_by(Comment.date.desc()).all()
    recent, top_tags = sidebar_data()
    return render_template(
        'blog/post.html',
        post=the_post,
        tags=tags,
        comments=comments,
        recent=recent,
        top_tags=top_tags,
        form=form
    )


@blog_blueprint.route('/tag/<string:tag_name>')
def tag(tag_name):
    the_tag = Tag.query.filter_by(title=tag_name).first_or_404()
    posts = the_tag.posts.order_by(Post.date.desc()).all()
    recent, top_tags = sidebar_data()
    print(posts)
    return render_template(
        'blog/tag.html',
        tag=the_tag,
        posts=posts,
        recent=recent,
        top_tags=top_tags
    )


@blog_blueprint.route('/user/<string:username>')
def user(username):
    the_user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.date.desc()).all()
    recent, top_tags = sidebar_data()
    return render_template(
        'user.html',
        user=the_user,
        posts=posts,
        recent=recent,
        top_tags=top_tags
    )
