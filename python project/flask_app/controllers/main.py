from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask_bcrypt import Bcrypt
from flask_app.models.users import User
from flask_app.models.products import Product
from flask_app.models.reviews import Review
from flask_app.models.carts import Cart
bcrypt = Bcrypt(app)

@app.route("/")
def landing_page():
    return render_template("main.html")

@app.route("/shop")
def shopping_page():
    all_products = Product.get_all_products()
    return render_template("browsing_page.html", all_products = all_products)

@app.route("/register")
def register():
    return render_template("loginreg.html")

@app.route("/submit/register", methods=["post"])
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
        return redirect("/register")
    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    data["password"] = pw_hash

    user_id = User.save(data)
    session["logged_id"] = user_id

    return redirect("/shop")

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
    return redirect("/shop")

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')

@app.route("/singleproduct/<int:id>")
def single_product_with_reviews(id):
    data = {
        "id": id
    }
    single_product = Product.get_all_reviews_for_product(data)
    return render_template("singleproduct.html", single_product = single_product)

@app.route("/add/review/<int:id>")
def add_review(id):
    data = {
        "id": id
    }
    single_product = Product.get_single_product(data)
    return render_template("addreview.html", single_product = single_product)

@app.route("/submit/review/<int:id>", methods=["post"])
def submit_review(id):
    data = {
        "users_id": session["logged_id"],
        "products_id":id,
        "content": request.form["content"],
        "rating": request.form["rating"]
    }
    Review.save(data)
    return redirect("/singleproduct/" + str(data["products_id"]))

@app.route("/addcart/<int:id>")
def add_to_cart(id):
    data = {
        "products_id": id,
        "users_id": session["logged_id"]
    }
    Cart.save(data)
    user_data = {
        "users_id": session["logged_id"]
    }
    all_items = Cart.get_all_cart_items_for_user(user_data)
    print(all_items)
    return render_template("mycart.html", all_items = all_items)

@app.route("/delete/review/<int:id>/<int:product_id>")
def delete_review(id, product_id):
    data = {
        "id": id
    }
    product_data = {
        "products_id": product_id
    }
    Review.delete(data)
    return redirect("/singleproduct/" + str(product_data["products_id"]))

@app.route("/mycart/<int:id>")
def mycart(id):
    data = {
        "users_id": id
    }
    all_items = Cart.get_all_cart_items_for_user(data)
    return render_template("mycart.html", all_items = all_items)

#{% if user.is_admin == 1 %} CHECK IF ADMIN IN JINJA