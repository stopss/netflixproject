from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import hashlib
import certifi
from pymongo import MongoClient

client = MongoClient('',tlsCAFile=certifi.where())
db = client.dbnetnote


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')


@app.route("/login", methods=["POST"])
def sign_up():
    # 로그인
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()                             # 비밀번호 암호화를 위한 해쉬값을 만들어 줌.
    result = db.users.find_one({'id': id_receive,
                                'pw': pw_hash})                                                  # 아이디와 패스워드가 매칭되는지 판단을 해줌. 매칭되는 사람이 있다면! 로그인에 성공 한것. 매칭이 안되면 회원가입을 해야함.

    if result is not None:                                                                       # result가 있다면!
        payload = {
            'id2': id_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)                           # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')                               # jwt 토큰을 발행. 놀이공원 자유입장권과 같은 것. 어떤 사람이 언제까지 입장이 유효하다를 적시해줌.
                                                                                                 # 토큰이 제대로 발행되었는지 확인하려면, 오른쪽 마우스 검사 누르고, 개발자 콘솔을 열면 Application탭을 눌러서 cookies가 나와 있음.
        return jsonify({'result': 'success', 'token': token})
                                                                                                 # 찾지 못하면,
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
