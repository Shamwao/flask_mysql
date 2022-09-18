from flask import Flask
from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.user import User


@app.route('/create_recipe')
def r_create_recipe():
    data = {"id" : session['user_id']}
    return render_template('create.html', user=User.get_one(data))

@app.route('/create-recipe', methods = ['POST'])
def f_create_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/create_recipe')
    Recipe.save(request.form)
    return redirect('/all_recipes')

@app.route('/all_recipes')
def all_recipes():
    recipes = Recipe.get_all_recipes()
    data = {"id": session['user_id']}
    return render_template('all_recipes.html', recipes = recipes, user = User.get_one(data))

@app.route('/show_recipe/<int:id>')
def r_show_recipe(id):
    data = {"id":id}
    return render_template('show_recipe.html', recipe=Recipe.get_one(data))

@app.route('/edit_recipe/<int:id>')
def r_edit_recipe(id):
    data = {"id":id}
    return render_template('edit.html', recipe=Recipe.get_one(data))

@app.route('/update_recipe/<int:recipe_id>', methods =['POST'])
def f_update(recipe_id):
    if not Recipe.validate_recipe(request.form):
        return redirect(f"/edit_recipe/{recipe_id}")
    Recipe.update(request.form)
    return redirect('/all_recipes')

@app.route('/delete/<int:id>')
def delete(id):
    data = {"id" : id}
    Recipe.delete(data)
    return redirect('/all_recipes')