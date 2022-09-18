from sqlite3 import connect
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None

    @classmethod
    def save(cls, data):
        query= "INSERT INTO recipes (name, description, instructions, date_made, under_30, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under_30)s, %(user_id)s);"
        return connectToMySQL('recipes').query_db(query, data)

    @classmethod
    def get_all_recipes(cls):
        query= "SELECT * FROM recipes;"
        result = connectToMySQL('recipes').query_db(query)
        recipes = []
        for r in result:
            recipes.append(cls(r))
        return recipes
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        result = connectToMySQL('recipes').query_db(query, data)
        return cls(result[0])

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL('recipes').query_db(query, data)
        
    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s, under_30 = %(under_30)s WHERE id = %(id)s;"
        return connectToMySQL('recipes').query_db(query, data)

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            flash('Field cannot be blank')
            is_valid = False 
        if len(recipe['description']) < 3:
            flash('Field cannot be blank')
            is_valid = False 
        if len(recipe['instructions']) < 3:
            flash('Field cannot be blank')
            is_valid = False 
        if len(recipe['date_made']) <= 0: 
            flash('When was the recipe made?')
            is_valid = False 
        if "under_30" not in recipe:
            flash ('Does your recipe take less than 30 minutes?')
            is_valid = False
        return is_valid
