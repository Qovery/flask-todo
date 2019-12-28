import flask
import psycopg2
from flask import jsonify
from qovery_client.qovery import Qovery

app = flask.Flask(__name__)

db_conf = Qovery().get_database_by_name('my-postgresql-3498225')  # name come from .qovery.yml file
db = psycopg2.connect(host=db_conf.host, database='todo_db', user=db_conf.username, password=db_conf.password, port=db_conf.port)


@app.route('/api/todo', methods=['GET'])
def list_todo():
    return jsonify({'results': []})


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
