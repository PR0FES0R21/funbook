from flask import Flask, render_template, request, jsonify, escape
from pymongo import MongoClient

import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DB_HOST = os.environ.get("MONGODB_URL")
DB_NAME = os.environ.get("DB_NAME")


client = MongoClient(DB_HOST)
db = client[DB_NAME]
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# route untuk memasukan data ke database
@app.route("/homework", methods=["POST"])
def homework_post():
    name_give = request.form["name_give"]
    commen_give = request.form["comment_give"]
    
    doc = {
        'name': escape(name_give),
        'comment': escape(commen_give)
    }
    
    db.fanmessages.insert_one(doc)
    return jsonify({'msg': 'data berhasil ditambahkan'})
    
# route untuk mengambil data
@app.route("/homework", methods=["GET"])
def homework_get():
    message_list = list(db.fanmessages.find({}, {'_id': False}))
    return jsonify({'message': message_list})

@app.route('/delete_all', methods=['GET'])
def delete_all():
    db.fanmessages.delete_many({})
    return jsonify({'msg': 'Semua data dihapus!'})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)