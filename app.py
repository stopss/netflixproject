from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

import certifi
import json
from bson import ObjectId
from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.gqkk6.mongodb.net/Cluster0?retryWrites=true&w=majority',tlsCAFile=certifi.where())
db = client.dbnetnote


# pull하고 변경
@app.route('/main')
def main():
   return render_template('main.html')

# DB에 저장된 유저 기록 요청
@app.route("/netnote/main", methods=["GET"])
def movie_get():
    movie_list = list(db.movies.find({},{'_id':False}))
    # movie_list = list(db.movies.find())

    return jsonify({'movies': movie_list})


# URL DB에 저장
@app.route('/netnote/geturl', methods=['POST'])
def url_post():
   url = request.form['url']

   doc = {
      'url': url,
      # 'idd': x,
      # "img": "https://images.justwatch.com/poster/19316749/s276/war-of-the-worlds.webp", "title": "우주전쟁",
      # "director": "Steven Spielberg", "date": "2021.10.11", "together": "친구1,친구2",
      # "memo": "레이 페리어는 이혼한 항만 근로자로 아무런 희망 없이 매일을 살아간다. 그러던 어느 주말, 그의 전 부인은 아들 로비와 어린 딸 레이첼과 주말을 보내라고 레이에게 맡긴다. 그리곤 얼마 안 있어 강력한 번개가 내리친다. 잠시 후, ",
      # "star": 4
   }
   db.movies.insert_one(doc)

   return jsonify({'msg': 'url 주소 저장!'})






if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)




