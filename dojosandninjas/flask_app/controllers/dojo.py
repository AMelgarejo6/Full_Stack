from flask_app import app
from flask import Flask, render_template, redirect, request, session, flash
from flask_app.models.dojos import Dojos
from flask_app.models.ninjas import Ninjas
@app.route('/backhome')
def backhome():
    return redirect('/')

@app.route('/')
def mainpage():
    dojos = Dojos.get_all()
    print(dojos)
    return render_template('mainpage.html', dojos=dojos)

@app.route('/newdojo', methods=["post"])
def new_user():
    data = {
        "name": request.form["name"],
    }
    Dojos.save(data)
    return redirect('/')

@app.route('/singledojo/<int:id>') #take in an id
def single_dojo_page(id):
    data = {
        "id": id
    }
    one_dojo = Dojos.get_one(data)
    all_ninjas = Ninjas.get_all_ninjas(data)
    return render_template("singledojo.html", all_ninjas = all_ninjas, one_dojo = one_dojo)

@app.route('/delete/<int:id>')
def delete_user(id):
    data = {
        "id": id
    }
    Dojos.delete(data)
    return redirect('/')

@app.route('/createnewninja')
def new_ninja():
    all_dojos = Dojos.get_all()
    return render_template('newninja.html', all_dojos=all_dojos)

@app.route('/newninja', methods=["post"])
def new_ninja_info():
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "age": request.form["age"],
        "dojo_id": request.form["dojos_id"]
    }
    Ninjas.save(data)
    return redirect('/')
