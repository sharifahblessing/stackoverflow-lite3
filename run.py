from flask import Flask, redirect
from flask_restful import Resource, Api
from app.database import Database
from app import app

db = Database()

@app.route('/',methods=['GET'])
def index():
    return redirect("https://stackoverflowlite6.docs.apiary.io/#",code=302)
if __name__ == '__main__':
    db.create_db_tables()
    app.run(port=5000,debug=True)