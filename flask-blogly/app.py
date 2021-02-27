"""Blogly application."""
from flask import Flask, render_template, request, redirect, session
import time
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
# db.create_all() # this would usually only exist once when creating the databse

#### next step is to make new tags, and handle the tags. THEN adjust newpost page to show all available tags. THEN adjust edit post to reflect the add/drop

@app.route('/')
def home_page():
    user = User.query.all()

    return render_template("list-users.html", user=user)



######## USER ##########

@app.route('/add-user')
def add_user():

    return render_template("add-user.html")

@app.route("/get-user", methods=["POST"])
def get_user():
    firstname = request.form["first-name"]
    lastname = request.form["last-name"]
    url = request.form["img-url"]

    new_user = User(first_name=firstname, last_name=lastname, image_url=url)
    user_id = new_user.id

    db.session.add(new_user)
    db.session.commit()

    return redirect(f'/')

@app.route('/<int:user_id>')
def user_profile(user_id):
    user = User.query.get_or_404(user_id)
    post = Post.query.all()

    return render_template("user-profile.html", user=user, post=post)

@app.route('/edit<int:user_id>')
def edit_user(user_id):
    user = User.query.get(user_id)

    return render_template("edit.html", user=user)

@app.route("/get-user<int:user_id>", methods=["POST"])
def get_user_edit(user_id):
    firstname = request.form["first-name"]
    lastname = request.form["last-name"]
    url = request.form["img-url"]

    user = User.query.filter_by(id=user_id).first()
    user.first_name = firstname
    user.last_name = lastname
    user.image_url = url
    db.session.commit()

    return redirect(f'/{user_id}')

@app.route('/delete<int:user_id>')
def delete_user(user_id):

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/")



######### POSTS #########

@app.route('/new-post<int:user_id>')
def make_post(user_id):
    session.pop('userid-for-post', None)
    session['userid-for-post'] = user_id
    tags = Tag.query.all()

    return render_template("new-post.html", user=user_id, tags=tags)

@app.route('/handle-post', methods=["POST"])
def handle_post():
    post_user = session['userid-for-post']
    post_title = request.form["title"]
    post_content = request.form["content"]
    post_tag = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(post_tag)).all()

    seconds = time.time()
    post = Post(title=post_title, content=post_content, created_at = time.ctime(seconds),user_code=post_user, tags=tags)

    db.session.add(post)
    db.session.commit()

    return redirect('/')

@app.route('/user-post<int:post_id>')
def show_post(post_id):
    user = User.query.all()
    posts = Post.query.all()
    tags = Tag.query.all()

    return render_template("user-post.html", post_id=post_id, posts=posts)

@app.route('/edit-post<int:post_id>')
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    title = post.title
    content = post.content

    return render_template('/edit-post.html', post=post, post_id=post_id, tags=tags)


@app.route("/handle-post<int:post_id>", methods=["POST"])
def handle_post_edit(post_id):
    post_title = request.form["title"]
    post_content = request.form["content"]
    post_tag = request.form["tag"]

    post = Post.query.filter_by(id=post_id).first()
    post.title = post_title
    post.content = post_content

    tag_ids = [int(num) for num in request.form.getlist("tag")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()
    return redirect(f'/user-post{post_id}')

@app.route('/delete-post<int:post_id>')
def delete_post(post_id):
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect('/')


### TAGS ###
@app.route('/new-tag')
def add_tag():
    tags = Tag.query.all()
    return render_template("new-tag.html", tags=tags)

@app.route("/handle-tag", methods=["POST"])
def handle_tag():
    tag = request.form["tag"]
    add_tag = Tag(name=tag)
    db.session.add(add_tag)
    db.session.commit()
    return redirect('/new-tag')