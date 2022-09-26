from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Review:
    def __init__(self, data):
        self.id = data["id"]
        self.users_id = data["users_id"]
        self.products_id = data["products_id"]
        self.content = data["content"]
        self.rating = data["rating"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.product = None #opposite of get_all_reviews_product
        self.user = None

    @classmethod
    def save(cls, data):
        query = "INSERT INTO reviews (users_id, products_id, content, rating, created_at, updated_at) VALUES (%(users_id)s, %(products_id)s, %(content)s, %(rating)s, NOW(), NOW())"

        user_id = connectToMySQL('lexoletics').query_db(query,data)
        return user_id

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM reviews WHERE id = %(id)s"
        user_id = connectToMySQL('lexoletics').query_db(query,data)
        return user_id
