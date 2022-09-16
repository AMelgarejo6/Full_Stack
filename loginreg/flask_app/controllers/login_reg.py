from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models.users import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/register", methods=["post"])
def register_user():
    print("trying to register user")
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": request.form["password"],
        "confirm_password": request.form["confirm_password"]
    }

    if not User.validate(data):
        print("not valid")
        return redirect("/")
    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    data["password"] = pw_hash

    user_id = User.save(data)
    session["logged_id"] = user_id
    return redirect("/success")

@app.route("/success")
def success():
    if "logged_id" not in session:
        return redirect("/")
    return render_template("success.html")
    
@app.route("/login", methods=["post"])
def login():
    data = {
        "email": request.form["email"]
    }
    this_user = User.find_by_email(data)

    if not this_user:
        flash("invalid")
        return redirect("/")
    if not bcrypt.check_password_hash(this_user.password, request.form['password']):
        flash("Invalid Email or Password")
        return redirect("/")
    
    session["logged_id"] = this_user.id
    return redirect("/success")

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')

