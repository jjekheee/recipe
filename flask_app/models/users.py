from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Users:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def add_account(cls,data):
        query = """INSERT INTO users (first_name,last_name,email,password)
        VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);"""
        results = MySQLConnection("recipes").query_db(query,data)
        return results
    
    @staticmethod
    def validate_register(data):
        is_valid = True

        if len(data['first_name']) < 3:
            flash("First Name must be atleast 3 characters long!!","reg_err")
            is_valid = False
        if len(data['last_name']) < 3:
            flash("Last Name must be atleast 3 characters long","reg_err")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid Email Address!","reg_err")
            is_valid = False
        if len(data['password']) < 6:
            flash('Password must be 7 characters.',"reg_err")
            is_valid = False
        elif len(data['password']) < 1:
            flash('Password must be longer.',"reg_err")
            is_valid = False
        if len(data['cpassword']) < 1:
            flash('Please confirm your password.',"reg_err")
            is_valid = False
        elif data['password'] != data['cpassword']:
            flash('Password did not match.',"reg_err")
            is_valid = False
        return is_valid
        
    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if len(data['name']) < 1:
            flash('Name must not be blank', 'recipe_err')
            is_valid = False
        if len(data['description']) < 1:
            flash('Description must not be blank', 'recipe_err')
            is_valid = False
        if len(data['instructions']) < 1:
            flash('Instructions must not be blank', 'recipe_err')
            is_valid = False
        if len(data['date_made']) < 1:
            flash('Date cooked/Made must not be blank', 'recipe_err')
            is_valid = False
        if len(data['cook_time']) < 1:
            flash('Is it under 30 minutes?', 'recipe_err')
            is_valid = False
        return is_valid

    @classmethod
    def login_user(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = MySQLConnection("recipes").query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_users_by_id(cls,data):
        query = "SELECT * FROM users where id = %(id)s"
        results = MySQLConnection("recipes").query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    

    @classmethod
    def all_details(cls,data):
        query = "SELECT * FROM users WHERE id =  %(id)s"
        results = MySQLConnection("recipes").query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])