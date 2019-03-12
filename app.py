from flask import Flask
from os import urandom

app = Flask(__name__)
app.secret_key = str(urandom(24))
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

@app.route('/')
def start():
    return 'Hello World!'
