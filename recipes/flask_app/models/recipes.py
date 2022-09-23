from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.users import User

class Recipe:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.under = data["under"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.poster = None
        self.users_id = data["users_id"]

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes JOIN users ON recipes.users_id = users.id;"
        results = connectToMySQL('recipes').query_db(query)
        recipes = []

        for row_from_db in results:
            one_recipe = cls(row_from_db)

            poster_data = {
                "id": row_from_db["users.id"],
                "first_name": row_from_db["first_name"],
                "last_name": row_from_db["last_name"],
                "email": row_from_db["email"],
                "password": row_from_db["password"],
                "created_at": row_from_db["users.created_at"],
                "updated_at": row_from_db["users.updated_at"]
            }
            one_recipe.poster = User(poster_data)
            recipes.append(one_recipe)
        
        return recipes
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO recipes (name, under, description, instructions, created_at, updated_at, users_id) VALUES (%(name)s, %(under)s, %(description)s, %(instructions)s, %(created_at)s, NOW(), %(users_id)s)"

        recipe_id = connectToMySQL('recipes').query_db(query, data)
        return recipe_id

    @classmethod
    def get_one_recipe(cls, data):
        query = "SELECT * FROM recipes WHERE recipes.id=%(id)s;"

        results = connectToMySQL('recipes').query_db(query,data)
        one_instance = cls(results[0])
        
        return one_instance

    @classmethod
    def edit_recipe(cls, data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, under=%(under)s, updated_at=NOW() WHERE id=%(id)s;"

        connectToMySQL('recipes').query_db(query, data)
        return

    @classmethod
    def remove(cls, data):
        query = "DELETE FROM recipes WHERE id=%(id)s"
        return connectToMySQL('recipes').query_db(query, data)