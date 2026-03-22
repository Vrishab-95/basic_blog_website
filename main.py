from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

import hashlib
from urllib.parse import urlencode
# Import your forms from the forms.py
from forms import CreatePostForm,RegisterForm,LoginForm,CommentForm

import os
from dotenv import load_dotenv

'''
Make sure the required packages are installed: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
'''

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
ckeditor = CKEditor(app)
Bootstrap5(app)


# TODO: Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI',"sqlite:///posts.db")
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLES

# TODO: Create a User table for all your registered users.
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    name: Mapped[str] = mapped_column(String(250), nullable=False)

    posts: Mapped[list["BlogPost"]] = relationship(
        "BlogPost", back_populates="author"
    )

    comments:Mapped[list["Comments"]] = relationship("Comments", back_populates="author")

    def avatar(self, size):
        # print(self.email)
        # default = "https://www.example.com/default.jpg"
        email_encoded = self.email.lower().encode('utf-8')
        email_hash = hashlib.sha256(email_encoded).hexdigest()
        query_params = urlencode({'d': "identicon", 's': str(size)})

        return f"https://www.gravatar.com/avatar/{email_hash}?{query_params}"

        # return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'


class BlogPost(db.Model):
    __tablename__ = "blog_posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    # author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    author: Mapped["User"] = relationship(
        "User", back_populates="posts"
    )

    comments:Mapped[list["Comments"]] = relationship("Comments", back_populates="parent_post")
    # id: Mapped["User"] = relationship(back_populates="author_id")

class Comments(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String(450), nullable=False)

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author:Mapped["User"] = relationship("User",back_populates="comments")

    post_id:Mapped[int] = mapped_column(ForeignKey("blog_posts.id"))
    parent_post:Mapped["BlogPost"] = relationship("BlogPost", back_populates="comments")

with app.app_context():
    db.create_all()


def admin_only(function):
    @wraps(function)
    def decorator_function(*args, **kwargs):
        print(current_user.is_authenticated)
        print(current_user.id)

        if current_user.id!=1:
            return abort(403)

        return function(*args, **kwargs)

    return decorator_function




# TODO: Use Werkzeug to hash the user's password when creating a new user.
@app.route('/register',methods=['GET', 'POST'])
def register():
    form=RegisterForm()
    if request.method == 'GET':
        return render_template("register.html",form=form)

    email=request.form['email']
    password=request.form['password']
    name=request.form['name']
    all_emails=db.session.execute(db.select(User.email)).scalars().all()

    if email in all_emails:
        flash("Email already registered")
        return redirect(url_for('login'))


    db.session.add(User(email=email,password=generate_password_hash(password,salt_length=8,method='pbkdf2:sha256:600000'),name=name))
    db.session.commit()

    login_user(db.session.query(User).filter_by(email=email).first())

    return redirect(url_for('get_all_posts'))


# TODO: Retrieve a user from the database based on their email. 
@app.route('/login',methods=["GET","POST"])
def login():
    form=LoginForm()
    if request.method == 'GET':
        return render_template("login.html",form=form)

    email=request.form['email']
    password=request.form['password']

    user=db.session.execute(db.select(User).where(User.email==email)).scalar()

    if user:
        if check_password_hash(user.password, password):

            login_user(user)
            return redirect(url_for('get_all_posts'))

        flash("Invalid password. Try again!")

    flash("Invalid Email. Try again!")

    return render_template("login.html",form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route('/')
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts)


# TODO: Allow logged-in users to comment on posts
@app.route("/post/<int:post_id>",methods=["GET","POST"])
def show_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)

    form=CommentForm()

    if request.method=="GET":
        return render_template("post.html", post=requested_post,form=form)

    if not current_user.is_authenticated:
        flash("Please login to comment on posts")
        return redirect(url_for("login"))

    comment_body=request.form["comment"]

    db.session.add(Comments(text=comment_body,author_id=current_user.id,post_id=post_id))
    db.session.commit()

    return redirect(url_for("show_post",post=requested_post,form=form,post_id=post_id))


# TODO: Use a decorator so only an admin user can create a new post
@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


# TODO: Use a decorator so only an admin user can edit a post
@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True)


# TODO: Use a decorator so only an admin user can delete a post
@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=False)
