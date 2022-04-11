from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import certifi

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.x85pm.mongodb.net/Cluster0?retryWrites=true&w=majority',tlsCAFile=certifi.where())
db = client.dbnetnote

@app.route('/')
def home():
   return render_template('home.html')










if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)




