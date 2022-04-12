from flask import Flask, render_template, request, redirect, url_for, jsonify
app = Flask(__name__)

# jwt 연결
import jwt                                                                            #파이썬 인터프리터에서 jwt 추가해주세요!
# 시간 날짜 형태 사용
from datetime import datetime, timedelta
# 비밀번호 암호화
import hashlib
# 비밀키 설정
SECRET_KEY = 'NetNote'
from bson.objectid import ObjectId                                                    #db에서 object id값 가져올 때 사용.
import certifi
from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.juhth.mongodb.net/cluster0?retryWrites=true&w=majority',tlsCAFile=certifi.where())
db = client.dbnetnote


@app.route('/')
def home():
    return render_template('home.html')

#로그인 시간이 만료되면 홈으로 이동.
@app.route('/')
def login_over():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return render_template('home.html')
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))


@app.route('/login')
def login_template():
    return render_template('login.html')


@app.route("/login", methods=["POST"])
def login():
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

@app.route('/sign_up')
def sign_up_template():
    return render_template('sign_up.html')

@app.route("/sign_up/save", methods=["POST"])
def sign_up():
    id_receive = request.form['id_give']                                                              # id 받고
    pw_receive = request.form['pw_give']                                                              # pw 받고
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()                                  # 해쉬 함수를 걸어준다
    doc = {
        "id": id_receive,                                                                             # 아이디
        "pw": pw_hash,                                                                                # 비밀번호
        "profile_name": id_receive                                                                    # 프로필 이름 기본값은 아이디
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route("/sign_up/sign_up_check", methods=["POST"])
def sign_up_check():
    # 아이디 중복 확인
    id_receive = request.form['id_give']
    exists = bool(db.users.find_one({"id": id_receive}))
    return jsonify({'result': 'success', 'exists': exists})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

