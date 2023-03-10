from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
client = MongoClient('mongodb+srv://root:root@cluster0.n0ew8bz.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# route untuk memasukan data ke database
@app.route("/homework", methods=["POST"])
def homework_post():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    doc = {
        'name': name_receive,
        'comment': comment_receive
    }
    db.fanmessages.insert_one(doc)
    return jsonify({'msg': 'data berhasil ditambahkan'})

# route untuk mengambil data
@app.route("/homework", methods=["GET"])
def homework_get():
    message_list = list(db.fanmessages.find({}, {'_id': False}))
    return jsonify({'message': message_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)