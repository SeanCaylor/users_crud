from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL
app = Flask(__name__)

@app.route('/')
def home():
    return redirect('/users')

@app.route('/users')
def index_group():
    mysql = connectToMySQL('users_cr')
    users = mysql.query_db('SELECT id, CONCAT_WS(" ", first_name, last_name) as "name", email FROM users;')
    print(users)
    return render_template('index.html', all_users = users)

@app.route('/users/<int:id>')
def index_single(id = 0):
    mysql = connectToMySQL('users_cr')
    query = 'SELECT id, CONCAT_WS(" ", first_name, last_name) as "name", email, created_at, updated_at FROM users WHERE id = %(id)s'
    data = {
        'id' : id
    }
    user = mysql.query_db(query, data)
    print(user)
    return render_template('displayuser.html', user = user)

@app.route('/users/delete/<int:id>')
def delete_user(id = 0):
    mysql = connectToMySQL('users_cr')
    query = 'DELETE FROM users WHERE id = %(id)s'
    data = {
        'id' : id
    }
    user = mysql.query_db(query, data)
    print(user)
    return redirect('/')

@app.route('/users/new')
def new_user_form():
    return render_template('newuser.html')

@app.route('/users/update/<int:id>')
def user_update(id = 0):
    mysql = connectToMySQL('users_cr')
    query = 'SELECT * FROM users WHERE id = %(id)s'
    data = {
        'id' : id
    }
    user = mysql.query_db(query, data)
    print(user)
    return render_template('updateuser.html', user = user)

@app.route('/create_user', methods=['POST'])
def create_user():
    mysql = connectToMySQL('users_cr')

    query = "INSERT INTO users (first_name, last_name, email) VALUE (%(fn)s, %(ln)s, %(eml)s)"
    data = {
        'fn' : request.form['first_name'],
        'ln' : request.form['last_name'],
        'eml' : request.form['email']
    }
    print('succeed')
    new_friend_id = mysql.query_db(query, data)
    print(new_friend_id)
    return redirect(f'/users/{new_friend_id}')

@app.route('/update_user/<int:id>', methods=['POST'])
def update_user(id):
    mysql = connectToMySQL('users_cr')

    query = "UPDATE users SET first_name = %(fn)s, last_name = %(ln)s, email = %(eml)s WHERE id = %(id)s"

    data = {
        'fn' : request.form['first_name'],
        'ln' : request.form['last_name'],
        'eml' : request.form['email'],
        'id' : id
    }
    print('succeed')
    updated_id = mysql.query_db(query, data)
    return redirect('/users/' + str(data['id']))

if __name__ == "__main__":
    app.run(debug = True)