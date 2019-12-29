#!/usr/bin/env python3
import json

import flask
import psycopg2
from flask import jsonify, Response
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from qovery_client.qovery import Qovery

# --- START INIT ---

app = flask.Flask(__name__)

# this file is not used while deployed on Qovery
configuration_file_path = '../.qovery/local_configuration.json'
# the database name comes from .qovery.yml file
database_name = 'my-postgresql-3498225'

# get database configuration from Qovery
qovery = Qovery(configuration_file_path=configuration_file_path)
db_conf = qovery.get_database_by_name(database_name)

# Setup PostgreSQL
conn = psycopg2.connect(host=db_conf.host, user=db_conf.username, database='postgres', password=db_conf.password, port=db_conf.port)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

cursor = conn.cursor()

queries = [
    """
CREATE TABLE IF NOT EXISTS todo (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT NOW(),
    title TEXT NOT NULL,
    description TEXT
)
    """
]

for query in queries:
    cursor.execute(query)


# --- END INIT ---

class Todo(object):
    def __init__(self, row_tuple=None, json_dict=None):

        self.id = None
        self.created_at = None
        self.title = None
        self.description = None

        if row_tuple:
            self.id = row_tuple[0]
            self.created_at = row_tuple[1]
            self.title = row_tuple[2]
            self.description = row_tuple[3]

        if json_dict:
            if 'title' in json_dict:
                self.title = json_dict['title']

            if 'description' in json_dict:
                self.description = json_dict['description']

    @property
    def to_json_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'title': self.title,
            'description': self.description
        }

    @property
    def error_message(self):
        if not self.title:
            return 'title field is mandatory'

        return None


@app.route('/', methods=['GET'])
def index():
    branch_name = qovery.branch_name
    if not branch_name:
        branch_name = 'unknown'

    return "<h1>Welcome :)</h1><p>The current branch is <b>" + branch_name + "</b></p><p>Source code available " \
                                                                             "<a href='https://github.com/evoxmusic/flask-todo'>here</a></p>" \
                                                                             "<p>API resources available:</p>" \
                                                                             "<ul><li>GET /api/todo -> to list todo</li>" \
                                                                             "<li>GET /api/todo/:id -> to show todo by id</li>" \
                                                                             "<li>POST /api/todo -> to add todo</li>" \
                                                                             "<li>DELETE /api/todo/:id -> to delete todo by id</li></ul>"


@app.route('/api/todo', methods=['GET'])
def list_todo():
    results = []

    cursor.execute('SELECT * FROM todo')

    for row in cursor.fetchall():
        results.append(Todo(row_tuple=row).to_json_dict)

    return jsonify({'results': results})


@app.route('/api/todo', methods=['POST'])
def add_todo():
    json_dict = flask.request.get_json()
    todo = Todo(json_dict=json_dict)

    if todo.error_message:
        return Response(json.dumps({'error_message': todo.error_message}), status=400)

    cursor.execute('INSERT INTO todo (title, description) VALUES (%s, %s) RETURNING id, created_at, title, description',
                   (todo.title, todo.description,))

    resp = cursor.fetchone()

    return Response(json.dumps(Todo(row_tuple=resp).to_json_dict), status=201)


@app.route('/api/todo/<id>', methods=['GET'])
def get_todo(id):
    cursor.execute('SELECT * FROM todo WHERE id = %s LIMIT 1', (id,))

    resp = cursor.fetchone()
    if not resp:
        return jsonify()

    return jsonify(Todo(row_tuple=resp).to_json_dict)


@app.route('/api/todo/<id>', methods=['DELETE'])
def delete_todo(id):
    cursor.execute('DELETE FROM todo WHERE id = %s', (id,))
    return '', 204


if __name__ == '__main__':
    print('Server is ready!')
    app.run(host='0.0.0.0', port=5000)
