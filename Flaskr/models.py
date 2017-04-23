from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

tags = db.Table(
    'post_tags',
    db.Column('post_id', db.INTEGER, db.ForeignKey('post.id')),
    db.Column('tag_id', db.INTEGER, db.ForeignKey('tag.id'))
)


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
