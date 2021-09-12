from flask import Flask, request
from flask.globals import session
from flask.templating import render_template
import json
import os

app = Flask(__name__)
app.static_folder = 'static'
app.secret_key = '239XRJ2U3R932RXNU32O'

BASE_DIR = 'notes'

### functions to read & write to json file
def read_data():
    with open("data.json", 'r') as file:
        data = json.load(file)
    return data

def write_data(entry):
    with open("data.json", 'w') as file:
        json.dump(entry, file)


### flask routes

# login page
@app.route('/')
def main():
    return render_template('index.html')

# registration page
@app.route('/register')
def register():
    return render_template('register.html')

# login function
@app.route('/home', methods=['POST'])
def home():
    uname = request.form['username']
    pswd = request.form['password']
    user_data = read_data()[uname]

    if user_data['password'] == pswd:
        session['user'] = uname
        return render_template('home.html', user_notes = user_data['notes'], user = uname)
    else:
        return "<h2>Invalid Credentials</h2>"

# registration function
@app.route('/sign_up', methods=['POST'])
def sign_up():
    uname = request.form['username']
    pswd = request.form['password1']
    
    if pswd == request.form['password2']:
        data = read_data()

        if uname not in data:
            os.mkdir(os.path.join(BASE_DIR, uname))
            data[uname] = {'password': pswd, 'notes': []}
            write_data(data)
            return '<a href = "/">Login</a>'
        else:
            return '<h2>Username already taken</h2><a href="/register">Go Back</a>'

    else:
        return '<h2>Password not Matching</h2>'

@app.route('/new')
def new():
    return render_template('new.html')


if __name__ == '__main__':
    app.run(debug=True)