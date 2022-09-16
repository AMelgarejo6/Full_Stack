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

    @staticmethod
    def validate(data):
        is_valid = True
        has_special_char =  False

        if data["password"] != data["confirm_password"]:
            flash("passwords must match!")
            is_valid = False

        for letter in data["password"]:
            if letter in ["!","@","#","$","%","^","&","*"]:
                has_special_char = True
            if not has_special_char:
                flash("Needs a special character!")
                is_valid = False

        if len(data['first_name']) <= 1:
            flash("More than one letter please!")
            is_valid = False
        for letter in data["first_name"]:
            if letter in ["!","@","#","$","%","^","&","*","0","1","2","3","4","5","6","7","8","9"]:
                flash("Only letters in name please.")
                is_valid = False

        if len(data['last_name']) <= 1:
            flash("More than one letter please!")
            is_valid = False
        for letter in data["last_name"]:
            if letter in ["!","@","#","$","%","^","&","*","0","1","2","3","4","5","6","7","8","9"]:
                flash("Only letters in name please.")
                is_valid = False

        if len(data['email']) <= 1:
            flash("More than one letter please!")
            is_valid = False
        
        if len(data['password']) <= 7:
            flash("More than eight charaters please!")
            is_valid = False

        return is_valid
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW())"

        user_id = connectToMySQL('loginreg').query_db(query,data)
        return user_id

    @classmethod
    def find_by_email(cls, data):
        query = "SELECT * FROM users WHERE email=%(email)s"

        results = connectToMySQL('loginreg').query_db(query,data)

        if len(results) == 0:
            return False
        one_instance = cls(results[0])
        return one_instance
