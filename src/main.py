#!/usr/bin/env python3

import flask
import psycopg2
from flask import jsonify
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from qovery_client.qovery import Qovery

# --- START INIT ---

app = flask.Flask(__name__)

# this file is not used while deployed on Qovery
configuration_file_path = '../.qovery/local_configuration.json'
# the database name comes from .qovery.yml file
database_name = 'my-postgresql-3498225'

# get database configuration from Qovery
db_conf = Qovery(configuration_file_path=configuration_file_path).get_database_by_name(database_name)

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
    def __init__(self, row):
        self.id = row[0]
        self.created_at = row[1]
        self.title = row[2]
        self.description = row[3]

    @property
    def to_json_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'title': self.title,
            'description': self.description
        }


@app.route('/api/todo', methods=['GET'])
def list_todo():
    results = []

    cursor.execute('SELECT * FROM todo')

    for row in cursor.fetchall():
        results.append(Todo(row).to_json_dict)

    return jsonify({'results': results})


@app.route('/api/todo', methods=['POST'])
def add_todo():
    return jsonify({})


@app.route('/api/todo/<id>', methods=['GET'])
def get_todo(id):
    return jsonify({})


@app.route('/api/todo/<id>', methods=['DELETE'])
def delete_todo(id):
    return jsonify({'result': 'ok'})


@app.route('/api/todo/<id>', methods=['PUT'])
def update_todo(id):
    return jsonify({})


if __name__ == '__main__':
    print('Server is ready!')
    app.run(host='0.0.0.0', port=5000)
