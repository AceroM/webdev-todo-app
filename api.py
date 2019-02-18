import json
import requests

s = requests.Session()

cookies = {}
data = {'username': 'migool'}
todo_data = {'content': 'Do homework'}
completed = '{"completed":true}'
data = json.dumps(data)
todo_data = json.dumps(todo_data)

response = s.post(
    'https://hunter-todo-api.herokuapp.com/auth', cookies=cookies, data=data)

# add = s.post('https://hunter-todo-api.herokuapp.com/todo-item', data=todo_data)
# print(add.content)

# deleted = s.delete('https://hunter-todo-api.herokuapp.com/todo-item/110')
# print(deleted.content)

res = s.put(
    'https://hunter-todo-api.herokuapp.com/todo-item/111', data=completed)
print(res.content)

todos = s.get('https://hunter-todo-api.herokuapp.com/todo-item')
todos = json.loads(todos.content)

print(todos)