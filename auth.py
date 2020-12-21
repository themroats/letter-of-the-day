from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, LoginManager
from initdb import Users, sess

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return render_template("login.html")


@auth.route("/login", methods=["POST"])
def login_post():
    username = request.form.get("username")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = sess.query(Users).filter_by(username=username).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password):
        flash("Please check your login details and try again.")

        # if user doesn't exist or password is wrong, reload the page
        return redirect(url_for("auth.login"))

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for("main.index"))


@auth.route("/signup")
def signup():
    return render_template("signup.html")


@auth.route("/signup", methods=["POST"])
def signup_post():

    username = request.form.get("username")
    password = request.form.get("password")

    # if this returns a user, then the email already exists in database
    user = sess.query(Users).filter_by(username=username).first()

    # if a user is found, we want to redirect back to signup page so user can try again
    if user:
        flash("Username already exists")
        return redirect(url_for("auth.signup"))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = Users(
        username=username, password=generate_password_hash(password, method="sha256")
    )

    # add the new user to the database
    sess.add(new_user)
    sess.commit()

    return redirect(url_for("auth.login"))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
