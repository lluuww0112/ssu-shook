from flask import Blueprint, jsonify, request
from model import sql_runner_Club, sql_runner_User
from model import sql_runner


Login_BP = Blueprint('Login', __name__)


@Login_BP.route('/regist', methods=["POST"])
def regist():
    user = request.json

    message = "성공적으로 가입이 완료되었습니다"
    status = 1
    # ID중복 검사
    if not sql_runner_User.regist(user):
        message = "이미 존재하는 유저입니다."
        status = 0
    return jsonify({
        "message" : message,
        "status" : status
    })


@Login_BP.route('/', methods=['POST'])
def login():    
    ID_PSW = request.json

    flag = 1
    message = "환영합니다"
    # ID및 비밀번호 확인
    if not sql_runner_User.login(ID_PSW['ID'], ID_PSW['password']):
        flag = 0
        message = "아이디 또는 비밀번호가 일치하지 않습니다."
        
    return jsonify({
        "message" : message,
        "status" : flag
    })      
