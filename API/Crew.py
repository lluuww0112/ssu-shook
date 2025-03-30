from flask import Blueprint, jsonify, request
from model import sql_runner, sql_runner_Club



Crew_Bp = Blueprint('Crew', __name__)


# 동아리원 확인, 접근권한 확인 필요
@Crew_Bp.route('/crew_list', methods=['POST'])
def get_crew_list():
    data = request.json
    ID = data['ID']
    club_name = data['club_name']

    connection = sql_runner.get_db_connection()
    rule = sql_runner_Club.check_rule(connection, ID, club_name)

    # rule이 없다면
    if not rule:
        return jsonify({
            "message" : "접근 권한이 없습니다",
            "status" : 0
        })
    else: # rule이 있다면
        results = None
        message = None
        try:
            results = sql_runner_Club.get_crew_list(connection, club_name)
            message = f"{club_name}의 동아리원 리스트 입니다."
        except:
            message =f"동아리원 리스트를 가져오는 도중 오류가 발생했습니다."
        
        return jsonify({
            "message" : message,
            "results" : results
        })
        

