from flask import Flask, redirect, url_for
from Flaskr.controllers.blog import blog_blueprint
from Flaskr.config import DevConfig
from Flaskr.models import db

app = Flask(__name__)
app.config.from_object(DevConfig)
db.init_app(app)


@app.route('/')
def index():
    return redirect(url_for('blog.home'))


app.register_blueprint(blog_blueprint)
if __name__ == '__main__':
    app.run()
