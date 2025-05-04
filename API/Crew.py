from flask import Blueprint, jsonify, request, send_file
import io
import pandas as pd
from urllib.parse import quote

from model import sql_runner, sql_runner_Club



Crew_Bp = Blueprint('Crew', __name__)


# 동아리원 조회
# 접근권한 확인 필요
@Crew_Bp.route('/crews', methods=['POST'])
def get_crew_list():
    data = request.json
    ID = data['ID']
    club_name = data['club_name']

    connection = sql_runner.get_db_connection()

    results = None
    message = None
    status = 1

    rule = sql_runner_Club.check_rule(connection, ID, club_name)
    # 임원진이 아니라면
    if rule == None or rule['rule'] == "부원":
        return jsonify({
            "message" : "접근 권한이 없습니다",
            "status" : 0
        })
    elif rule["rule"] == "임원진":
        try:
            results = sql_runner_Club.get_crew_info(connection, club_name)
            message = f"{club_name}의 부원 리스트 입니다."
        except:
            message =f"동아리원 리스트를 가져오는 도중 오류가 발생했습니다."
            status = 0
        
        
    connection.close()
    return jsonify({
        "message" : message,
        "results" : results,
        "status" : status
    })



# 부원 명단 추출
@Crew_Bp.route("/crews/get_csv", methods=["POST"])
def get_crew_csv():
    data = request.json
    ID = data['ID']
    club_name = data['club_name']
    
    connection = sql_runner.get_db_connection()

    # 권한 확인
    rule = sql_runner_Club.check_rule(connection, ID, club_name)
    if rule is None or rule['rule'] != "임원진":
        connection.close()
        return jsonify({
            "message": "권한이 없습니다",
            "status": 0
        })

    # 부원 정보 조회
    results = sql_runner_Club.get_crew_info(connection, club_name)
    connection.close()

    if results == 0:
        return jsonify({
            "message": "조회 도중 오류가 발생했습니다",
            "status": 0
        })

    df = pd.DataFrame(results)
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False, encoding='utf-8-sig')  # Excel용 한글 깨짐 방지
    csv_buffer.seek(0)
    # postman으로 파일을 전달받으면 한글 파일명 디코딩이 안되는 문제 발생
    # 브라우저 상에서 다운로드 해서 한글명 제대로 나오는지 확인 필요
    file_name = quote(f"{club_name}_회원명단.csv")

    return send_file(
        io.BytesIO(csv_buffer.getvalue().encode('utf-8-sig')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=file_name
    )



# 임원진만 가입권유 전송가능
    # 현재 동아리 멤버라면 보내기 불가 -> "이미 동아리 부원입니다"
@Crew_Bp.route('/invite', methods=["POST"])
def send_invitation():
    data =request.json
    ID = data['ID']
    club_name = data['club_name']
    target = data['target']
    connection = sql_runner.get_db_connection()

    message = None
    status = None

    # 권환 확인
    rule = sql_runner_Club.check_rule(connection, ID, club_name)
    if rule['rule'] == '임원진':
        # 이미 동아리 부원인지 확인
        crews = sql_runner_Club.get_crew_list(connection, club_name)
        if target in [crew['ID'] for crew in crews]:
            status = 0
            message = "이미 존재하는 회원입니다"
        else: # 아니라면 초대 전송
            print()
            status = sql_runner_Club.send_invitation(connection, club_name, target)
            if status == 1:
                message = f"{target}님을 초대했습니다"
            elif status == 2:
                message = f"{target}님에게 이미 초대를 전송했습니다"
            else:
                message = "전송 도중 오류가 발생했습니다"
    else:
        status = 0
        message = "권한이 없습니다."

    connection.close()
    return jsonify({
        "message" : message,
        "status" : status
    })


# 부원 부서 변경(rule, position)
# rule = 임원진? 부원?
# postion = 회장 부회장 총무 등등
@Crew_Bp.route('/change_position', methods=["POST"])
def change_position():
    data = request.json
    ID = data['ID']
    club_name = data['club_name']
    target = data['target']
    attribute = data['attribute']
    value = data['value']
    connection = sql_runner.get_db_connection()

    message = None
    status = None

    rule = sql_runner_Club.check_rule(connection, ID, club_name)
    if rule == None or rule['rule'] == "부원":
        status = 0
        message = "권한이 없습니다."
    elif rule['rule'] == '임원진':
        crew_list = sql_runner_Club.get_crew_list(connection, club_name)
        crew_list = [data['ID'] for data in crew_list]
        
        if target in crew_list:
            status = sql_runner_Club.change_position(connection, target, club_name, value, attribute)
            message = f"성공적으로 {target}님의 {attribute}을 {value}(으)로 변경했습니다." if status else "부서 변환 도중 오류가 발생했습니다"
        else:
            status = 0
            message = "존재하지 않는 부원 입니다"
        

    connection.close()
    return jsonify({
        "message" : message,
        "status" : status
    })



# 글 게시(리크루팅, 연합활동, 활동내역)
# contents = {
    # "club_name" : ,
    # "post_type" : ,
    # "title" : ,
    # "text" : ,
# }

# !recruiting!
# format = {
#     "capacity" : ,
#     "start_date" : ,
#     "end_date" : 
# }

# !activity!
# format = {
#     "activity_day" : ,
#     "activity_image" : ,
# }

# !union!
# format = {
#     "start_date" : ,
#     "end_date" : ,
# }
@Crew_Bp.route("/post", methods=["POST"])
def post():
    data = request.json
    ID = data['ID']
    contents = data['contents']
    club_name = contents['club_name']
    format = data['format']

    connection = sql_runner.get_db_connection()
    message = None
    status = None

    # 권한 확인
    rule = sql_runner_Club.check_rule(connection, ID, club_name)
    if rule == None or rule['rule'] == "부원":
        message = "권한이 없습니다"
        status = 0
    elif rule['rule'] == "임원진":
        status = sql_runner_Club.post(connection, contents, format)
        message = "글을 포스팅 했습니다" if status else "포스팅 도중 오류가 발생했습니다."
    else :
        message = "권한을 확인하는 도중 문제가 발생했습니다."
        status = 0

    connection.close()
    return jsonify({
        "message" : message,
        "status" : status
    })


# 포스팅 신청 화인 
@Crew_Bp.route("/post/get_applicants", methods=['POST'])
def get_applicants():
    data = request.json
    ID = data['ID']
    club_name = data['club_name']
    post_ID = data['post_ID']

    connection = sql_runner.get_db_connection()
    message = None
    status = None
    
    rule = sql_runner_Club.check_rule(connection, ID, club_name)
    if rule == None or rule['rule'] == '부원':
        message = "권한이 없습니다"
        status = 0
    elif rule['rule'] == '임원진':
        try:
            results = sql_runner_Club.get_applicants(connection, post_ID)    
            status = 1
        except:
            message = "조회를 하는 도중 오류가 발생했습니다"
            status = 0

    connection.close()
    if status:
        return jsonify({
            "results" : results,
            "status" : status
        })
    else:
        return jsonify({
            "message" : message,
            "status" : status
        })


# 포스팅 삭제 
@Crew_Bp.route("/post/delete", methods=["DELETE"])
def post_delete():
    data =request.json
    ID = data['ID']
    club_name = data['club_name']
    post_ID = data['post_ID']

    connection = sql_runner.get_db_connection()
    message = None
    status = None


    rule = sql_runner_Club.check_rule(connection, ID, club_name)
    if rule == None or rule['rule'] == '부원':
        message = "권한이 없습니다"
        status = 0
    elif rule['rule'] == "임원진":
        status = sql_runner_Club.delete_post(connection, post_ID)
        message = "포스팅이 삭제되었습니다" if status else "삭제 도중 오류가 발생했습니다"
    
    connection.close()
    return jsonify({
        "message" : message,
        "status" : status
    })


# 입부신청 승인 
@Crew_Bp.route("/post/approve", methods=["POST"])
def approve():
    data = request.json
    ID = data['ID']
    club_name = data['club_name']
    post_ID = data['post_ID']
    target = data['target']

    status = None
    message = None
    
    connection = sql_runner.get_db_connection()
    
    rule = sql_runner_Club.check_rule(connection, ID, club_name) # 권한 확인
    if rule == None or rule['rule'] == "부원":
        message = "권한이 없습니다"
        status = 0
    elif rule['rule'] == "임원진":
        # Crews 테이블에 행 추가
        cond1 = sql_runner_Club.add_new_crew(connection, target, club_name)
        if cond1 == 1: 
            # Applicants 테이블에서 신청자 삭제
            cond2 = sql_runner_Club.delete_applicant(connection, target, post_ID) 
            if cond2 == 1:
                message = f"{target}님이 입부했습니다!"
                status = 1
            else:
                sql_runner_Club.delete_crew(connection, ID, club_name) 
                message = "승인을 하는 도중 오류가 발생했습니다(delete_crew)"
                status = 0
        elif cond1 == 2:
            message = "이미 존재하는 부원입니다"
            status = 2
        else:
            message = "승인을 하는 도중 오류가 발생했습니다"
            status = 0

    connection.close()
    return jsonify({
        "message" : message,
        "status" : status
    })



fee_publish_message_table = [
    "발행 도중 오류가 발생했습니다",
    "발행되었습니다",
    "이미 발행한 부원이 있습니다"
]
# 회비 납부 발행 
    # 권한 확인
        # 발행
@Crew_Bp.route("/fee_publish", methods=["POST"])
def fee_publish():
    data = request.json
    ID = data['ID']
    club_name = data['club_name']
    IDs = data['IDs']
    fee = data['fee']

    connection = sql_runner.get_db_connection()
    message = None
    status = None

    rule = sql_runner_Club.check_rule(connection, ID, club_name)
    print(rule)
    if rule == None or rule['rule'] == "부원":
        message = "권한이 없습니다"
        status = 0
    elif rule['rule'] == "임원진":
        status = sql_runner_Club.add_club_fee_table(connection, club_name, IDs, fee)
        message = fee_publish_message_table[status]
    

    return jsonify({
        "message" : message,
        "status" : status
    })


# 회비 납부 완료전환 
@Crew_Bp.route('/fee_publish/complete', methods=['PUT'])
def fee_publish_complete():
    data = request.json
    ID = data['ID']
    club_name = data['club_name']
    IDs = data['IDs']
    publications = data['publications']
    state = data['state'] # 1이면 납부 완료, 0이면 미납 상태로 변경

    connection = sql_runner.get_db_connection()
    message = None
    status = None
    
    rule = sql_runner_Club.check_rule(connection, ID, club_name)
    if rule == None or rule['rule'] == '부원':
        message = '권한이 없습니다'
        status = 0
    elif rule['rule'] == '임원진':
        status = sql_runner_Club.update_payment(connection, club_name, IDs, publications, state)
        message = "성공적으로 납부 상태가 업데이트 되었습니다" if status else "납부 상태 업데이트 도중 오류가 발생했습니다"
    
    return jsonify({
        "message" : message,
        "status" : status
    })


# 회비 발행 취소 
@Crew_Bp.route("/fee_publish/cancel", methods=['DELETE'])
def fee_publish_cancel():
    data = request.json
    ID = data['ID']
    club_name = data['club_name']
    IDs = data['IDs']
    publications = data['publications']

    connection = sql_runner.get_db_connection()
    message = None
    status = None
    
    print("==================================")
    print(ID)
    print(club_name)
    print(IDs)
    print(publications)
    print("==================================")


    rule = sql_runner_Club.check_rule(connection, ID, club_name)
    if rule != None and rule['rule'] == '부원':
        message = "권한이 없습니다"
        status = 0
    elif rule != None and rule['rule'] == '임원진':
        status = sql_runner_Club.payment_cancel(connection, club_name, IDs, publications)
        message = "성공적으로 발행이 취소되었습니다" if status else "발행 취소 도중 오류가 발생했습니다"
    else:
        message = "권한을 확인하는 도중 오류가 발생했습니다"
        status = 0

    return jsonify({
        "message" : message,
        "status" : status
    })



# 회비 납부 테이블 조회 
@Crew_Bp.route("/fee_publish/table", methods=['POST'])
def get_publish_table():
    data = request.json

    ID = data['ID']
    club_name = data['club_name']
    publication = data['publication']

    connection = sql_runner.get_db_connection()
    results = None
    message = None
    status = None
    
    
    rule = sql_runner_Club.check_rule(connection, ID, club_name)
    if rule == None or rule['rule'] == "부원":
        message = "권한이 없습니다"
        status = 0
    elif rule["rule"] == "임원진":
        try:
            results = sql_runner_Club.get_payment_table(connection, club_name, publication)
            message = "회비 납부 테이블 조회 완료"
            status = 1
        except:
            message = "회비 납부 테이블 조회 도중 오류 발생"
            status = 0
    
    return jsonify({
        "message" : message,
        "results" : results,
        "status" : status
    })




# 권한 확인
# 동아리 관리자 페이지 접속 전 확인용
@Crew_Bp.route("/check_rule", methods=['POST'])
def check_rule():
    data = request.json
    ID = data['ID']
    club_name = data['club_name']

    connection = sql_runner.get_db_connection()
    message = None
    status = None

    rule = sql_runner_Club.check_rule(connection, ID, club_name)

    
    if rule == None:
        message = "권한이 없습니다"
        status = 0
    elif rule.get('rule') == "임원진":
        message = "권한이 확인되었습니다"
        status = 1

        
    return jsonify({
        "message" : message,
        "status" : status
    })




