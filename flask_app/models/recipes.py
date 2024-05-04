from flask_app.config.mysqlconnection import MySQLConnection
from flask_app.models.users import Users

class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.cook_time = data['cook_time']
        self.date_made = data['date_made']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.users = []

    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM users INNER JOIN recipes ON users.id = recipes.user_id"
        results = MySQLConnection("recipes").query_db(query)
        recipes = []
        for recipe in results:
            data = {
                "recipe_id": recipe['recipes.id'],
                "name": recipe['name'],
                "cook_time": recipe['cook_time'],
                "first_name": recipe['first_name'],
                "last_name": recipe['last_name'],
            }
            recipes.append(data)
        return recipes

    @classmethod
    def recipe_by_id(cls,recipe_id):
        query = """SELECT * FROM recipes
                WHERE id = %(recipe_id)s;
                """
        data = {
            'recipe_id':recipe_id
        }
        results = MySQLConnection("recipes").query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def create_recipe(cls,data):
        query = "INSERT INTO recipes (name, description, instructions, cook_time, date_made, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(cook_time)s, %(date_made)s, %(user_id)s)"
        results = MySQLConnection("recipes").query_db(query,data)
        return results
    
    @classmethod
    def update_recipe(cls,data):
        query = """UPDATE recipes
                SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, cook_time = %(cook_time)s, date_made = %(date_made)s, updated_at = NOW()
                WHERE id = %(id)s"""
        results = MySQLConnection("recipes").query_db(query,data)
        return results
    
    @classmethod
    def delete_recipe(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s"
        results = MySQLConnection("recipes").query_db(query,data)
        return results
    
    @classmethod
    def all_details(cls,data):
        query = "SELECT * FROM users WHERE id =  %(id)s"
        results = MySQLConnection("recipes").query_db(query,data)
        recipe = cls(results[0])
        for user in results:
            data = {
                "id": user['id'],
                "first_name": user['first_name'],
                "last_name": user['last_name'],
                "email": user['email'],
                "password": user['password'],   
                "created_at": user['created_at'],
                "updated_at": user['updated_at'],
            }
            recipe.users.append(Users(data))
            return recipe
        
    @classmethod
    def join_recipes(cls,data):
        query = "SELECT * FROM users RIGHT JOIN recipes on users.id = recipes.user_id WHERE user_id = %(id)s"
        results = MySQLConnection("recipes").query_db(query,data)
        recipe = cls(results[0])
        for user in results:
            data = {
                "id": user['id'],
                "first_name": user['first_name'],
                "last_name": user['last_name'],
                "email": user['email'],
                "password": user['password'],   
                "created_at": user['created_at'],
                "updated_at": user['updated_at'],
            }
            recipe.users.append(Users(data))
            return recipe


    @classmethod
    def get_recipe(cls,data):
        query = "SELECT * FROM recipes LEFT JOIN users ON users.id = recipes.user_id WHERE recipes.id = %(id)s"
        results = MySQLConnection("recipes").query_db(query,data)
        recipe = cls(results[0])
        for user in results:
            data = {
                "id": user['id'],
                "first_name": user['first_name'],
                "last_name": user['last_name'],
                "email": user['email'],
                "password": user['password'],
                "created_at": user['created_at'],
                "updated_at": user['updated_at'],
                "user_id": user['user_id']
            }
            recipe.users.append(Users(data))
            return recipe