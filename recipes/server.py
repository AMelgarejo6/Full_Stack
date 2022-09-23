from flask import Flask, render_template, request, redirect, session, flash
from flask_app.controllers import login_reg
from flask_app import app

if __name__ == "__main__":
    app.run(debug=True)