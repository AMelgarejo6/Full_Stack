from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.users import User
from flask_app.models.recipes import Recipe

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
    return redirect("/")

@app.route("/success")
def success():
    if "logged_id" not in session:
        return redirect("/")
    
    data = {
        "id": session["logged_id"]
    }
    this_user = User.find_one_by_id(data)
    all_recipes = Recipe.get_all()
    return render_template("recipes.html", this_user = this_user, all_recipes = all_recipes)
    
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



@app.route("/createrecipe")
def create_recipe():
    return render_template("createrecipe.html")

@app.route("/submitrecipe", methods=["post"])
def submit_recipe():
    print("trying to create recipe")
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "created_at": request.form["created_at"],
        "under": request.form["under"],
        "users_id": session["logged_id"]
    }
    Recipe.save(data)
    return redirect("/success")

@app.route("/edit/<int:id>")
def edit_page(id):
    data = {
        "id": id
    }
    one_recipe = Recipe.get_one_recipe(data)
    return render_template("edit_page.html", one_recipe = one_recipe)

@app.route("/submitedit", methods=["post"])
def submit_edit():
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "under": request.form["under"],
        "id": request.form["id"] #LOOK AT HIDDEN INPUT ON HTML EDIT FORM
    }
    Recipe.edit_recipe(data)

    return redirect("/success")

@app.route("/remove/<int:id>")
def remove_recipe(id):
    data = {
        "id": id
    }
    Recipe.remove(data)
    return redirect("/success")

@app.route("/viewrecipe/<int:id>")
def view_recipe(id):
    data = {
        "id": id
    }
    my_recipe = Recipe.get_one_recipe(data)
    userid = {
        "id": my_recipe.users_id
    }
    operator = {
        "id": session["logged_id"]
    }
    this_user = User.find_one_by_id(operator)
    posted_by_this_user = User.find_one_by_id(userid)
    return render_template("view_recipe.html", my_recipe = my_recipe, this_user = this_user, posted_by_this_user = posted_by_this_user)

