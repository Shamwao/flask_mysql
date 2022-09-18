from sqlite3 import connect
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.recipe import Recipe
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PW_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []

    @staticmethod
    def validate_input(user):
        is_valid=True
        if len(user['first_name']) < 3:
            flash('Enter a first name', 'register')
            is_valid=False
        if len(user['last_name']) < 3:
            flash('Enter a last name','register')
            is_valid=False
        if len(user['email']) < 1:
            flash('Enter a valid email address','register')
            is_valid =False
        if not EMAIL_REGEX.match(user['email']):
            flash('Enter a valid email','register')
            is_valid=False
        if user['password'] != user['confirm']:
            flash("Passwords don't match",'register')
            is_valid=False
        if len(user['password']) < 8:
            flash('Password must contain at least 8 characters','register')
        if not PW_REGEX.match(user['password']):
            flash('Password must contain at least one capital letter, one number, and one symbol','register')
        return is_valid        

    @classmethod
    def save(cls, data):
        query= "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL('recipes').query_db(query, data)

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('recipes').query_db(query, data)
        return cls(result[0])

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('recipes').query_db(query, data)
        return cls(result[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('recipes').query_db(query, data)
        return cls(result[0])

    @classmethod
    def get_user_recipes(cls):
        query = "SELECT * FROM users LEFT JOIN recipes ON users.id = user_id WHERE users.id = %(id)s;"
        result = connectToMySQL('recipes').query_db(query)
        user = []
        for row in result:
            recipe_data = {
                "id": row['id'],
                "name": row['name'],
                "description": row['description'],
                "instructions": row['instructions'],
                "date_made": row['date_made'],
                "under_30": row['under_30'],
                "created_at": row ['created_at'],
                "updated_at": row['updated_at']
            }
            user.append(Recipe(recipe_data))
        return user