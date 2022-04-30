
from flask import Flask, jsonify, abort, request, make_response
from flaskext.mysql import MySQL

app = Flask(__name__)

# Configure mysql database
app.config['MYSQL_DATABASE_HOST'] = 'database'
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'devenes123'
app.config['MYSQL_DATABASE_DB'] = 'todo_db'
app.config['MYSQL_DATABASE_PORT'] = 3306
mysql = MySQL()
mysql.init_app(app)
connection = mysql.connect()
connection.autocommit(True)
cursor = connection.cursor()


def init_todo_db():
    drop_table = 'DROP TABLE IF EXISTS todo_db.todos;'
    todos_table = """
    CREATE TABLE todo_db.todos(
    task_id INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(100) NOT NULL,
    description VARCHAR(200),
    is_done BOOLEAN NOT NULL DEFAULT 0,
    PRIMARY KEY (task_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """
    data = """
    INSERT INTO todo_db.todos (title, description, is_done)
    VALUES
        ("Project 2", "Work on project 2 with teammates", 1 ),
        ("Kubernetes Documentation", "Study and learn how to read Kubernetes docs", 0),
        ("Work on CC Phonebook", "Solve python coding challenge about phonebook app", 0);
        ("Try to learn Docker", "Study and learn how to use Docker", 0);
        ("Learn to use Git", "Study and learn how to use Git", 1);
        ("Learn to use Gitlab", "Study and learn how to use Gitlab", 1);
        ("Learn to use Jenkins", "Study and learn how to use Jenkins", 1);
        ("Learn to use Jenkinsfile", "Study and learn how to use Jenkinsfile", 1);
        ("Work on Golang", "Study and learn how to use Golang", 1);
    """
    cursor.execute(drop_table)
    cursor.execute(todos_table)
    cursor.execute(data)


def get_all_tasks():
    query = """
    SELECT * FROM todos;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    tasks = [{'task_id': row[0], 'title':row[1], 'description':row[2],
              'is_done': bool(row[3])} for row in result]
    return tasks


def find_task(id):
    query = f"""
    SELECT * FROM todos WHERE task_id={id};
    """
    cursor.execute(query)
    row = cursor.fetchone()
    task = None
    if row is not None:
        task = {'task_id': row[0], 'title': row[1],
                'description': row[2], 'is_done': bool(row[3])}
    return task


def insert_task(title, description):
    insert = f"""
    INSERT INTO todos (title, description)
    VALUES ('{title}', '{description}');
    """
    cursor.execute(insert)

    query = f"""
    SELECT * FROM todos WHERE task_id={cursor.lastrowid};
    """
    cursor.execute(query)
    row = cursor.fetchone()
    return {'task_id': row[0], 'title': row[1], 'description': row[2], 'is_done': bool(row[3])}


def change_task(task):
    update = f"""
    UPDATE todos
    SET title='{task['title']}', description = '{task['description']}', is_done = {task['is_done']}
    WHERE task_id= {task['task_id']};
    """
    cursor.execute(update)

    query = f"""
    SELECT * FROM todos WHERE task_id={task['task_id']};
    """
    cursor.execute(query)
    row = cursor.fetchone()
    return {'task_id': row[0], 'title': row[1], 'description': row[2], 'is_done': bool(row[3])}


def remove_task(task):
    delete = f"""
    DELETE FROM todos
    WHERE task_id= {task['task_id']};
    """
    cursor.execute(delete)

    query = f"""
    SELECT * FROM todos WHERE task_id={task['task_id']};
    """
    cursor.execute(query)
    row = cursor.fetchone()
    return True if row is None else False


@app.route('/')
def home():
    return "Welcome to Enes Turan's To-Do API Service"


@app.route('/todos', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': get_all_tasks()})


@app.route('/todos/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = find_task(task_id)
    if task == None:
        abort(404)
    return jsonify({'task found': task})


@app.route('/todos', methods=['POST'])
def add_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    return jsonify({'newly added task': insert_task(request.json['title'], request.json.get('description', ''))}), 201


@app.route('/todos/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = find_task(task_id)
    if task == None:
        abort(404)
    if not request.json:
        abort(400)
    task['title'] = request.json.get('title', task['title'])
    task['description'] = request.json.get('description', task['description'])
    task['is_done'] = int(request.json.get('is_done', int(task['is_done'])))
    return jsonify({'updated task': change_task(task)})


@app.route('/todos/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = find_task(task_id)
    if task == None:
        abort(404)
    return jsonify({'result': remove_task(task)})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


if __name__ == '__main__':
    init_todo_db()
    # app.run(debug=False)
    app.run(host='0.0.0.0', port=80)
