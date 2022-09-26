from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.reviews import Review
from flask_app.models.users import User

class Product:
    def __init__(self, data):
        self.id = data["id"]
        self.category = data["category"]
        self.description = data["description"]
        self.image = data["image"]
        self.price = data["price"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.reviews = []

    @classmethod
    def save(cls, data):
        query = "INSERT INTO products (category, description, image, price, created_at, updated_at) VALUES (%(category)s, %(description)s, %(image)s, %(price)s, NOW(), NOW())"

        user_id = connectToMySQL('lexoletics').query_db(query,data)
        return user_id

    @classmethod
    def get_all_reviews_for_product(cls, data):
        query = "SELECT * FROM products LEFT JOIN reviews ON products.id = reviews.products_id LEFT JOIN users ON reviews.users_id = users.id WHERE products.id = %(id)s;"

        
        results = connectToMySQL('lexoletics').query_db(query,data)
        
        one_product = cls(results[0])
        print(results[0])
        print("here is the result!")

        all_reviews = []
        for row_in_db in results:
            review_data = {
                "id": row_in_db["reviews.id"],
                "users_id": row_in_db["users_id"],
                "products_id": row_in_db["products_id"],
                "content": row_in_db["content"],
                "rating": row_in_db["rating"],
                "created_at": row_in_db["reviews.created_at"],
                "updated_at": row_in_db["reviews.updated_at"],
            }
            one_review = Review(review_data)

            user_data = {
                "id": row_in_db["users.id"],
                "first_name": row_in_db["first_name"],
                "last_name": row_in_db["last_name"],
                "email": row_in_db["email"],
                "password": row_in_db["password"],
                "is_admin": row_in_db["is_admin"],
                "created_at": row_in_db["users.created_at"],
                "updated_at": row_in_db["users.updated_at"],
            }
            one_review.user = User(user_data)

            all_reviews.append(one_review)
        one_product.reviews = all_reviews
        
        return one_product
        
    @classmethod
    def get_all_products(cls):
        query = "SELECT * FROM products"
        results = connectToMySQL('lexoletics').query_db(query)

        products = []

        for row_from_db in results:
            one_product = cls(row_from_db)
            products.append(one_product)

        return products

    @classmethod
    def get_single_product(cls, data):
        query = "SELECT * FROM products WHERE id = %(id)s"
        result = connectToMySQL('lexoletics').query_db(query, data)

        one_instance = cls(result[0])
        return one_instance