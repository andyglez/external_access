from flask import Flask
from os import urandom
from settings import database as db

app = Flask(__name__)
app.secret_key = str(urandom(24))
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

@app.route('/')
def start():
    cursor = db.get_connection.cursor()
    cursor.execute("select * from Users")
    result = ''
    for i in cursor.fetchall():
        result += str(i) + '\n'
    return result
