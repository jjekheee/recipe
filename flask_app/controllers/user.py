from flask import render_template,redirect,session,request,flash
from flask_app import app
from flask_app.models.users import Users
from flask_app.models.recipes import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/register', methods = ['POST'])
def register():

    if Users.validate_register(request.form):
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        flash("Registration Successful","reg_success")
    
        data = {
            'first_name':request.form['first_name'],
            'last_name':request.form['last_name'],
            'email':request.form['email'],
            'password': pw_hash
        }
        session['user_id'] = Users.add_account(data)
    return redirect('/')

@app.route('/login_user', methods = ['POST'])
def login():
    data = {'email':request.form['email']}
    user_in_db = Users.login_user(data)
    if user_in_db:
        if bcrypt.check_password_hash(user_in_db.password, request.form['password']):
            session['user_id'] = user_in_db.id
            session['first_name'] = user_in_db.first_name
        return redirect('/recipes')
    flash("invalid email/password",'log_err')
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')



