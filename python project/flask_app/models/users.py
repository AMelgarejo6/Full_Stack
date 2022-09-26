from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.is_admin = 0

    @staticmethod
    def validate(data):
        is_valid = True

        if data["password"] != data["confirm_password"]:
            flash("passwords must match!")
            is_valid = False

        special_char_counter = 0
        for letter in data["password"]:
            if letter in ["!","@","#","$","%","^","&","*"]:
                special_char_counter += 1
        if special_char_counter < 1:
            flash("Needs a special character!")
            is_valid = False

        if len(data['first_name']) < 1:
            flash("More than one letter please!")
            is_valid = False
        if len(data['last_name']) < 1:
            flash("More than one letter please!")
            is_valid = False
        if len(data['email']) < 1:
            flash("More than one letter please!")
            is_valid = False
        if len(data['password']) < 7:
            flash("More than eight charater please!")
            is_valid = False

        return is_valid
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, is_admin, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, 0 , NOW(), NOW())"

        user_id = connectToMySQL('lexoletics').query_db(query,data)
        return user_id

    @classmethod
    def find_by_email(cls, data):
        query = "SELECT * FROM users WHERE email=%(email)s"

        results = connectToMySQL('lexoletics').query_db(query,data)

        if len(results) == 0:
            return False
        one_instance = cls(results[0])
        return one_instance

    @classmethod
    def find_one_by_id(cls, data):
        query = "SELECT * FROM users WHERE id=%(id)s"

        results = connectToMySQL('lexoletics').query_db(query, data)

        if len(results) == 0: #checking if there is no matches
            return False
        
        one_instance = cls(results[0]) #if it didnt return nothing, then it will only return one
        return one_instance