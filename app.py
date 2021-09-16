from flask import Flask, request
from flask.globals import session
from flask.templating import render_template
import json
import os
from tool import skip_line

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

# home page
@app.route('/home')
def home():
    if 'user' in session:
        user = session['user']
        return render_template('home.html', user_notes =  read_data()[user]['notes'], user = user)
    else:
        return render_template('405.html')

# new page
@app.route('/new')
def new():
    if 'user' in session:
        return render_template('new.html')
    else:
        return render_template('405.html')

# login function
@app.route('/sign_in', methods=['POST'])
def sign_in():
    uname = request.form['username']
    pswd = request.form['password']

    try:
        user_data = read_data()[uname]
        if user_data['password'] == pswd:
            session['user'] = uname
            return '''<script>window.location='/home'</script>'''
        else:
            return '''<script>alert("Invalid Credentials");window.location='../'</script>'''
    except:
        return '''<script>alert("User Not Found");window.location='../'</script>'''

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
            return '''<script>alert("Registered");window.location='../'</script>'''
        else:
            return '''<script>alert("Username already taken");window.location='/register'</script>'''

    else:
        return '''<script>alert("Password not Matching");window.location='/register'</script>'''

# logout function
@app.route('/logout')
def logout():
    if 'user' in session:
        session.clear()
        return '''<script>window.location='../';</script>'''
    else:
        return render_template('405.html')

# save function
@app.route('/save', methods=['POST'])
def save():
    if 'user' in session:
        name = request.form['name'].strip()
        content = request.form['content']

        data = read_data()
        if name not in data[session['user']]['notes']:
            with open(f"{BASE_DIR}/{session['user']}/{name}.txt", 'w') as note:
                note.write(content)
            data[session['user']]['notes'].append(name)
            write_data(data)
            return '''<script>alert("Note Saved");window.location='/home'</script>'''
        else:
            return '''<script>alert("Name Exists");window.location='/new';</script>'''
    else:
        return render_template('405.html')

# view note function
@app.route('/view_note')
def view_note():
    if 'user' in session:
        note = request.args.get('note')
        path = f'notes/{session["user"]}/{note}.txt'
        with open(path, 'r') as file:
            lines = skip_line(file.readlines())
        print(lines)
        return render_template('note.html', user=session['user'], note=note, lines=lines)

    else:
        return render_template('405.html')

# delete note function
@app.route('/delete_note')
def delete_note():
    if 'user' in session:
        note = request.args.get('note')
        path = f'notes/{session["user"]}/{note}.txt'
        os.remove(path)

        data = read_data()
        data[session['user']]['notes'].remove(note)
        write_data(data)

        return '''<script>alert('Note Deleted');window.location='/home'</script>'''
    else:
        return render_template('405.html')


# go back functions

@app.route('/back')
def back():
    return '''<script>window.location='../'</script>'''

@app.route('/prev')
def prev():
    if 'user' in session:
        return '''<script>window.location='/home'</script>'''
    else:
        return back()

# 404 error handler
@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")

if __name__ == '__main__':
    app.run(debug=True)