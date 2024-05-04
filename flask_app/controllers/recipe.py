from flask import render_template,redirect,session,request,flash
from flask_app.models.recipes import Recipe
from flask_app.models.users import Users
from flask_app import app


@app.route('/recipes')
def recipes():
    id = session['user_id']
    first_name = session['first_name']
    recipes = Recipe.get_all_recipes()
    return render_template('recipes.html', recipes = recipes)

@app.route('/recipes/new')
def new_recipes():
    return render_template('addrecipe.html')

@app.route('/add_recipes', methods = ['POST'])
def add_recipes():
    data = {
            'name':request.form['name'],
            'description':request.form['description'],
            'instructions':request.form['instructions'],
            'date_made':request.form['date_made'],
            'cook_time':request.form['cook_time']
        }
    if not Users.validate_recipe(data):
        return redirect('/recipes/new')
    Recipe.create_recipe(request.form)
    return redirect('/recipes')

@app.route('/recipes/<id>')
def show_recipe(id):
    data = { 
        "id": id
    }
    recipe = Recipe.get_recipe(data)
    return render_template('details.html', recipe = recipe)

@app.route('/recipes/edit/<recipe_id>')
def recipe_page(recipe_id):
    recipe_id = Recipe.recipe_by_id(recipe_id)
    return render_template('editrecipe.html', recipe = recipe_id)

@app.route('/edit_recipe', methods = ['POST'])
def edit_recipe():
    Recipe.update_recipe(request.form)
    return redirect('/recipes')

@app.route('/recipes/delete/<id>')
def delete_recipe(id):
    data = {
        "id":id
    }
    Recipe.delete_recipe(data)
    return redirect('/recipes')