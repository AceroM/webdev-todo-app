from flask import Flask, render_template, request, session, redirect, url_for
import json
import requests
import os

app = Flask(__name__)
app.secret_key = '6969'

s = requests.Session()
cookies = {}

authLink = 'https://hunter-todo-api.herokuapp.com/auth'

@app.route('/')
def home():
    if session.get('user', None):
        return redirect('/todos')
    else:
        return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user', None):
        return redirect('/todos')
    if request.method == 'POST':
        print(request)
        username = request.form['username']
        data = '{"username":"' + username + '"}'
        response = s.post(
            'https://hunter-todo-api.herokuapp.com/auth', data=data)
        print(response.content)
        print(response.status_code)
        if response.status_code == 200:
            session['user'] = username
            return redirect('/todos')
        else:
            return render_template('login.html', error="incorrect login information")
    else:
        return render_template('login.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        content = request.form['content']
        todo_data = {'content': content}
        todo_data = json.dumps(todo_data)
        res = s.post('https://hunter-todo-api.herokuapp.com/todo-item', data=todo_data)
        print(res.status_code)
        print(res.content)
        if res.status_code != 201:
            return render_template('create.html', error="ERROR OCCURED")
        else:
            return redirect('/todos')
    else:
        return render_template('create.html')


@app.route('/logoff', methods=["GET"])
def logoff():
    if session.get('user', None):
        session['user'] = 0
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('user', None):
        return redirect('/todos')
    if request.method=="POST":
        user = request.form['name']
        user_data = {'username': user}
        user_data = json.dumps(user_data)
        res = s.post('https://hunter-todo-api.herokuapp.com/user', data=user_data)
        print(res.status_code)
        print(res.content)
        if res.status_code != 201:
            return render_template('register', error="ERROR OCCURED")
        else:
            return render_template('home.html', message="Thanks for registering, please login")
    else:
        return render_template('register.html')

# todoList = []

@app.route('/todos', methods=["GET"])
def menu():
    if session.get('user', None):
        todos = s.get('https://hunter-todo-api.herokuapp.com/todo-item')
        todos = json.loads(todos.content)
        return render_template('index.html', todos=todos, user=session.get('user'))
    else:
        return redirect('/')

@app.route('/todos/notcomplete/<int:number>', methods=["GET"])
def notcomplete(number):
    s.put('https://hunter-todo-api.herokuapp.com/todo-item/' + str(number), data='{"completed":false}')
    todos = s.get('https://hunter-todo-api.herokuapp.com/todo-item')
    todos = json.loads(todos.content)
    return render_template('index.html', status="Marked incomplete", todos=todos)

@app.route('/todos/complete/<int:number>', methods=["GET"])
def complete(number):
    s.put('https://hunter-todo-api.herokuapp.com/todo-item/' + str(number), data='{"completed":true}')
    todos = s.get('https://hunter-todo-api.herokuapp.com/todo-item')
    todos = json.loads(todos.content)
    return render_template('index.html', status="Marked complete", todos=todos)

@app.route('/todos/delete/<int:number>', methods=["GET"])
def delete(number):
    s.delete('https://hunter-todo-api.herokuapp.com/todo-item/' + str(number))
    todos = s.get('https://hunter-todo-api.herokuapp.com/todo-item')
    todos = json.loads(todos.content)
    return render_template('index.html', status="Deleted item", todos=todos)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, threaded=True)
