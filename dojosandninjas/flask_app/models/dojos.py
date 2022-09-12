from flask_app.config.mysqlconnection import connectToMySQL

class Dojos:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod

    def get_all(cls):
        query = "SELECT * FROM dojos;"
        
        results = connectToMySQL('dojos_and_ninjas').query_db(query) #we will call on the connectToMySQL command everytime we want to execute a query
        users = []

        for result in results:
            one_instance = cls(result)
            users.append(one_instance)
        return users
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO dojos (name, created_at, updated_at) VALUES (%(name)s, NOW(), NOW())"
        return connectToMySQL('dojos_and_ninjas').query_db(query, data)

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM dojos WHERE id=%(id)s;"
        results = connectToMySQL('dojos_and_ninjas').query_db(query, data)

        print(results)
        users = []
        for result in results:
            users.append(cls(result))
        return users

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM dojos WHERE id=%(id)s;"
        return connectToMySQL('dojos_and_ninjas').query_db(query, data)
