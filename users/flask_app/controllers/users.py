from flask_app import app
from flask import Flask, render_template, redirect, request, session, flash
from flask_app.models.user import Users
@app.route('/backhome')
def backhome():
    return redirect('/')

@app.route('/')
def mainpage():
    users = Users.get_all()
    print(users)
    return render_template('mainpage.html', users = users)

@app.route('/newuser', methods=["post"])
def new_user():
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"]
    }
    Users.save(data)
    return redirect('/')

@app.route('/form')
def new_form():
    return render_template('create.html')

@app.route('/singleuser/<int:id>') #take in an id
def single_user_page(id):
    data = {
        "id": id
    }

    single_user = Users.get_one(data)
    return render_template("singleuser.html", single_user = single_user)

@app.route('/delete/<int:id>')
def delete_user(id):
    data = {
        "id": id
    }
    Users.delete(data)
    return redirect('/')

@app.route('/change/<int:id>')
def change_info(id):
    data = {
        "id": id
    }
    single_user = Users.get_one(data)
    return render_template("change.html", single_user = single_user)

@app.route('/editted/<int:id>', methods=["post"])
def editted(id):
    data = {
        "id": id,
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"]
    }
    Users.edit(data)
    return redirect('/')