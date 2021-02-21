"""Blogly application."""
from flask import Flask, render_template, request, redirect, session
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


@app.route('/')
def home_page():
    user = User.query.all()
    return render_template("list-users.html", user=user)


@app.route('/add-user')
def add_user():
    return render_template("add-user.html")


@app.route("/get-user", methods=["POST"])
def get_user():
    firstname = request.form["first-name"]
    lastname = request.form["last-name"]
    url = request.form["img-url"]

    new_user = User(first_name=firstname, last_name=lastname, image_url=url)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/')


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


@app.route('/<int:user_id>')
def user_details(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("user-details.html", user=user)


@app.route('/edit<int:user_id>')
def edit_user(user_id):
    user = User.query.get(user_id)
    return render_template("edit.html", user=user)


@app.route('/delete<int:user_id>')
def delete_user(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect('/')