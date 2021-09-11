from flask import Flask, request
from flask.templating import render_template
import json

app = Flask(__name__)
app.static_folder = 'static'
app.secret_key = '239XRJ2U3R932RXNU32O'

def read_data():
    with open("data.json", 'r') as file:
        data = json.load(file)
    return data

def write_data(entry):
    with open("data.json", 'w') as file:
        json.dump(entry, file)


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/sign_in', methods=['POST'])
def sign_in():
    uname = request.form['username']
    pswd = request.form['password']
    return f'{uname} {pswd}'

@app.route('/sign_up', methods=['POST'])
def sign_up():
    uname = request.form['username']
    pswd = request.form['password1']
    
    if pswd == request.form['password2']:
        data = read_data()

        if uname not in data:
            data[uname] = {'password': pswd, 'notes': []}
            write_data(data)
            return '<a href = "/">Login</a>'
        else:
            return '<h2>Username already taken</h2><a href="/register">Go Back</a>'

    else:
        return '<h2>Password not Matching</h2>'


if __name__ == '__main__':
    app.run(debug=True)