from flask import Flask
import mysql.connector
import time

app = Flask(__name__)

mydb = mysql.connector.connect(
    user="root",
    password="root",
    host="mysql-development",
    port="3306",
    database="testapp"
)

if __name__ == "__main__":
    app.run()
