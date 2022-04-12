from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import requests
import certifi

from bs4 import BeautifulSoup

from bson.objectid import ObjectId
from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.x85pm.mongodb.net/Cluster0?retryWrites=true&w=majority',tlsCAFile=certifi.where())
db = client.dbnetnote

@app.route('/')
def home():
   return render_template('home.html')

@app.route("/netnote/write", methods=["GET"])
def write_get():
   print("get")
   # get_url = "https://www.netflix.com/kr/title/81251379"
   # get_url = "https://www.netflix.com/title/81251379"
   get_url = "https://www.justwatch.com/kr/%EC%98%81%ED%99%94/riteul-poreseuteu"
   objId = db.movies.find_one({'url': get_url})['_id']
   print(objId)

   headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
   data = requests.get(get_url, headers=headers)

   soup = BeautifulSoup(data.text, 'html.parser')

   title = soup.select_one('#base > div.jw-info-box > div > div.jw-info-box__container-content > div:nth-child(2) > div.title-block__container > div.title-block > div > h1').text
   director = soup.select_one('#base > div.jw-info-box > div > div.jw-info-box__container-sidebar > div > aside > div.hidden-sm.visible-md.visible-lg.title-sidebar__desktop > div.title-info > div:nth-child(5) > div.detail-infos__value > span > a').text
   image = soup.select_one('meta[property="og:image"]')['content']

   db.movies.update_one({'_id': objId}, {'$set':{'title':title, 'director':director, 'image':image}})

   doc = {
      'objId': objId,
      'title': title,
      'director': director,
      'image': image
   }

   return render_template('write.html', data=doc)
   # return jsonify({'movies':doc})


@app.route("/netnote/write", methods=["POST"])
def write_post():
   print("기록 저장하기")
   objId_receive = request.form['objId']
   date_receive = request.form['date']
   together_receive = request.form['together']
   memo_receive = request.form['memo']
   star_receive = request.form['star']
   print(objId_receive, date_receive, together_receive, memo_receive, star_receive)


   doc = {
      'date': date_receive,
      'together': together_receive,
      'memo': memo_receive,
      'star': star_receive
   }
   db.movies.update_one({'_id': ObjectId(objId_receive)}, {'$set':doc})

   return render_template('home.html')


@app.route("/netnote/view", methods=["GET"])
def view_get():
   print("view")
   objId_receive = "6254557f6626d6d50173d193"

   doc = db.movies.find_one({'_id': ObjectId(objId_receive)})

   return render_template('view.html', data=doc)











if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)




