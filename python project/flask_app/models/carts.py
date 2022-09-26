from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.users import User
from flask_app.models.products import Product
from flask import flash

class Cart:
    def __init__(self, data):
        self.users_id = data["users_id"]
        self.products_id = data["products_id"]
        self.carts = []
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO cart_items (users_id, products_id) VALUES (%(users_id)s, %(products_id)s)"

        user_id = connectToMySQL('lexoletics').query_db(query,data)
        return user_id

    @classmethod
    def get_all_cart_items_for_user(cls, data):
        query = "SELECT * FROM products LEFT JOIN cart_items ON products.id = cart_items.products_id WHERE users_id = %(users_id)s;"
        results = connectToMySQL('lexoletics').query_db(query,data)
        
        cart_products = []
        for row_in_db in results:
            product_data = Product(row_in_db)
            cart_products.append(product_data)
        
        return cart_products