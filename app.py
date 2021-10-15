
from flask import Flask,request, jsonify
import sqlite3


from flask.typing import TemplateFilterCallable

app = Flask(__name__)


@app.route('/')
def home():
    return "hello world"

@app.route('/add',methods=['POST'])
def add_todo():
    request_ = request.get_json()
    print("request data",request_)
    id = request_['id']
    title = request_['title']
    description = request_['description']

    conn = sqlite3.connect('todo.db')
    insert_query = """INSERT into TODO(TodoId,Title,Description) VALUES (? ,? ,?)"""
    cursor = conn.cursor()
    cursor.execute(insert_query,(id,title,description))
    conn.commit()
    cursor.close()
    conn.close()
    return "Added successfully" 

@app.route('/delete',methods=['POST'])
def delete_todo():
    request_ = request.get_json()
    print("request data",request_)
    id = request_['id']
    conn = sqlite3.connect('todo.db')
    delete_query = """DELETE FROM TODO where TodoID = ?"""
    cursor = conn.cursor()
    cursor.execute(delete_query,(id,))
    conn.commit()
    cursor.close()
    conn.close()
    return "deleted successfully"
    

@app.route('/update',methods=['POST'])
def update_todo():
    request_ = request.get_json()
    print("request data",request_)
    id = request_['id']
    title = request_['title']
    description = request_['description']
    conn = sqlite3.connect('todo.db')
    delete_query = """UPDATE TODO SET title=?,description=? where TodoID = ?"""
    cursor = conn.cursor()
    cursor.execute(delete_query,(title,description,id))
    conn.commit()
    cursor.close()
    conn.close()
    return "updated successfully"

@app.route('/list', methods=['GET'])
def list_todo():
    conn = sqlite3.connect('todo.db')
    get_query = """SELECT TodoId,Title,Description from TODO"""
    cursor = conn.cursor()
    cursor.execute(get_query)
    records = cursor.fetchall()
    todos = []
    for record in records:
        todo = {}
        todo['id'] = record[0]
        todo['title'] = record[1]
        todo['description'] = record[2]
        todos.append(todo)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'result': todos})
    

if __name__ == '__main__':
    app.run(debug=True)

