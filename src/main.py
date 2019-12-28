import flask

app = flask.Flask(__name__)

if __name__ == '__main__':
    print('Server is ready!')
    app.run(host='0.0.0.0', port=5000)
