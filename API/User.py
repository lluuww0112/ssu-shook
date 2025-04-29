from flask import Blueprint, jsonify, request
from model import sql_runner_Club, sql_runner_User
from model import sql_runner


User_BP = Blueprint('User', __name__)


# 회원가입
@User_BP.route('/regist', methods=["POST"])
def regist():
    user = request.json
    connection = sql_runner.get_db_connection()

    message = "성공적으로 가입이 완료되었습니다"
    status = 1
    # ID중복 검사
    if not sql_runner_User.regist(connection, user):
        message = "이미 존재하는 유저입니다."
        status = 0
    
    connection.close()
    return jsonify({
        "message" : message,
        "status" : status
    })


# 로그인
@User_BP.route('/login', methods=['POST'])
def login():    
    data = request.json
    ID = data['ID']
    password = data['password']
    connection = sql_runner.get_db_connection()

    status = 1
    message = "환영합니다"
    # ID및 비밀번호 확인
    if not sql_runner_User.login(connection, ID, password):
        status = 0
        message = "아이디 또는 비밀번호가 일치하지 않습니다."
        
    connection.close()
    return jsonify({
        "message" : message,
        "status" : status
    })      


# 로그아웃 ??? 


# 동아리 가입권유 조회
@User_BP.route("/invitations/<ID>", methods=['GET'])
def get_invitations(ID):
    connection = sql_runner.get_db_connection()

    results =sql_runner_User.get_invitations(connection, ID)

    if results:
        connection.close()
        return jsonify({
            "results" : [data['club_name'] for data in results],
            "status" : 1
        })
    elif results == ():
        connection.close()
        return jsonify({
            "message" : "입부 제안이 없습니다.",
            "status" : 2
        })
    else:
        connection.close()
        return jsonify({
            "message" : "입부제안을 받아오는 도중 오류가 발생했습니다",
            "status" : 0
        })


# 동아리 가입권유 수락
    # 특정 동아리로 부터 초대가 왔는지 우선 확인
    # 수락시 Crews테이블에 추가되도록 구현
    # 수락한 가입권유 행은 테이블에서 삭제
@User_BP.route("/accept_invitation", methods=['POST'])
def accept_invitation():
    data = request.json
    ID = data['ID']
    club_name = data['club_name']
    connection = sql_runner.get_db_connection()

    status = 0
    message = None

    # 유효한 초대장인지 확인
    invitations =  sql_runner_User.get_invitations(connection, ID)
    invitations_from = [inv['club_name'] for inv in invitations]
    # 가입권유가 온 것이 맞다면
    if club_name in invitations_from:
        # 동아리원으로서 추가
        # 정상적으로 추가되었다면 초대함에서 해당 동아리의 초대 삭제
        if sql_runner_Club.add_new_crew(connection, ID, club_name):
            sql_runner_User.delete_invitations(connection, ID, club_name)
            message = f"{club_name}의 부원이 되었습니다."
            status = 1
        else:
            message = "부원추가 도중 오류가 발생했습니다"
            status = 0
    else: # 아니라면
        message = "유효하지 않은 가입권유입니다."
        status = 0

    connection.close()
    return jsonify({
        "message" : message,
        "status" : status
    })


# 게시글 목록 조회
@User_BP.route("/get_posts", methods=["GET"])
def get_posts():
    connection = sql_runner.get_db_connection()

    results = sql_runner_User.get_posts(connection)
    connection.close()
    if results == 0:
        return jsonify({
            "message" : "게시글을 조회하는 도중 오류가 발생했습니다",
            "status" : 0
        })
    elif len(results) == 0:
        return jsonify({
            "results" : "게시글이 조회되지 않았습니다",
            "status" : 1
        })
    else:
        return jsonify({
            "results" : results,
            "status" : 1
        })
    

# 게시글 하나 조회 
@User_BP.route("/get_posts/<post_ID>", methods=["GET"])
def get_post(post_ID):
    connection = sql_runner.get_db_connection()

    result = sql_runner_User.get_entire_post(connection, post_ID)
    connection.close()
    if result == None:
        return jsonify({
            "message" : "게시글 조회 도중 오류가 발생했습니다",
            "status" : 0
        })
    elif result == 2:
        return jsonify({
            "message" : "존재하지 않는 게시글입니다",
            "status" : 0
        })
    else:
        return jsonify({
            "result" : result,
            "status" : 1
        })
        

# 포스팅 지원 
@User_BP.route("/post_apply", methods=["POST"])
def post_apply():
    data = request.json
    ID = data['ID']
    post_ID = data['post_ID']
    
    connection = sql_runner.get_db_connection()
    
    message = None
    status = None

    status = sql_runner_User.add_applicants(connection, ID, post_ID)
    
    if status == 1:
        message = "성공적으로 지원했습니다"
    elif status == 2:
        message = "이미 지원했습니다"
    elif status == 3:
        message = "지원을 할 수 있는 게시글이 아닙니다"
    else:
        message = "지원 도중 오류가 발생했습니다"

    connection.close()
    return jsonify({
        "message" : message,
        "status" : status
    })



# 리뷰 추가 
@User_BP.route("/review/add", methods=["POST"])
def add_review():
    review_contensts = request.json
    connection = sql_runner.get_db_connection()

    status = sql_runner_User.add_review(connection, review_contensts)
    message = "리뷰를 추가했습니다" if status else "리뷰 추가를 실패했습니다"

    connection.close()
    return jsonify({
        "message" : message,
        "status" : status
    })
    


# 리뷰 조회 
@User_BP.route("/review/get/<club_name>", methods=["GET"])
def get_reviews(club_name):
    connection = sql_runner.get_db_connection()
    
    status = None
    message = None
    try:
        results = sql_runner_User.get_reviews(connection, club_name)
        message = "조회 성공" if results != () else "조회된 리뷰가 없습니다."
        status = 1
    except:
        message = "리뷰 조회 도중 오류가 발생했습니다."
        status = 0

    connection.close()
    if status:
        return jsonify({
            "results" : results,
            "message" : message,
            "status" : status
        })
    else:
        return jsonify({
            "message" : message,
            "status" : status
        })


    
# 리뷰 삭제 
    # 내 리뷰 불러오기
    # 삭제하려는 리뷰와 내 리뷰가 동일한지 확인
        # 삭제 
@User_BP.route("/review/delete", methods=["DELETE"])
def update_review():
    data = request.json
    ID = data['ID']
    review_ID = data['review_ID']

    connection = sql_runner.get_db_connection()
    
    status = None
    message = None

    cond = sql_runner_User.check_my_review(connection, ID, review_ID)
    if cond == 1:
        status = sql_runner_User.delete_review(connection, review_ID)
        message = "리뷰가 삭제되었습니다" if status else "리뷰 삭제 도중 오류가 발생했습니다."
    elif cond == 2:
        message = "권한이 없습니다."
        status = 0
    else:
        message = "권한을 확인하는 도중 오류가 발생했습니다"
        status = 0

    connection.close()
    return jsonify({
        "message" : message,
        "status" : status
    })


# 동아리 랭킹 점수 제약성 추가하기

# 지원자 수 카운트 제약성 추가 필요