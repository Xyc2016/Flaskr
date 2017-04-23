from flask import Flask, render_template, jsonify, flash, request, Blueprint, redirect, url_for
from config import DevConfig
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class CommentForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[DataRequired()]
    )
    text = TextAreaField(u'Comment', validators=[DataRequired()])


app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'SECRET_KEY'
blog_blueprint = Blueprint('blog', __name__, template_folder='templates/blog', url_prefix='/blog')


class User(db.Model):
    id = db.Column(db.INTEGER(), primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    posts = db.relationship(
        'Post',
        backref='user',
        lazy='dynamic'
    )

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return '<User ' + self.username + '>'


tags = db.Table(
    'post_tags',
    db.Column('post_id', db.INTEGER, db.ForeignKey('post.id')),
    db.Column('tag_id', db.INTEGER, db.ForeignKey('tag.id'))
)


class Post(db.Model):
    id = db.Column(db.INTEGER(), primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text())
    date = db.Column(db.DateTime())
    comments = db.relationship(
        'Comment',
        backref='post',
        lazy='dynamic'
    )
    user_id = db.Column(db.INTEGER(), db.ForeignKey('user.id'))
    tags = db.relationship(
        'Tag',
        secondary=tags,
        backref=db.backref('posts', lazy='dynamic')
    )

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '<Post ' + self.title + '>'


class Comment(db.Model):
    id = db.Column(db.INTEGER(), primary_key=True)
    name = db.Column(db.String(255))
    text = db.Column(db.Text())
    date = db.Column(db.DateTime())
    post_id = db.Column(db.INTEGER(), db.ForeignKey('post.id'))

    def __repr__(self):
        return '<Comment ' + self.text + '>'


class Tag(db.Model):
    id = db.Column(db.INTEGER(), primary_key=True)
    title = db.Column(db.String(255))

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '<Tag ' + self.title + '>'


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


@app.route('/')
def index():
    return redirect(url_for('blog.home'))


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


app.register_blueprint(blog_blueprint)
if __name__ == '__main__':
    app.run()
