from model import sql_runner
from model import sql_runner_Club, sql_runner_User


# 테스트 데이터 ================================================================================================================================================================================================================================================

# 유저 데이터
user1 = {
    "ID": "test1",
    "password": "test1",
    "student_id": 20211737,
    "name": "윤세혁",
    "college": "공과대학",
    "major": "AI",
    "grade": 3,
    "phone_number": "010-4823-0620",
    "e_mail": "tgur0620@gmail.com",
}

user2 = {
    "ID": "test2",
    "password": "test2",
    "student_id": 20211738,
    "name": "김철수",
    "college": "공과대학",
    "major": "컴퓨터공학",
    "grade": 2,
    "phone_number": "010-1234-5678",
    "e_mail": "chulsoo@example.com",
}

user3 = {
    "ID": "test3",
    "password": "test3",
    "student_id": 20211739,
    "name": "이영희",
    "college": "인문대학",
    "major": "영문학",
    "grade": 1,
    "phone_number": "010-2345-6789",
    "e_mail": "younghee@example.com",
}

user4 = {
    "ID": "test4",
    "password": "test4",
    "student_id": 20211740,
    "name": "박민수",
    "college": "사회과학대학",
    "major": "경제학",
    "grade": 4,
    "phone_number": "010-3456-7890",
    "e_mail": "minsoo@example.com",
}

user5 = {
    "ID": "test5",
    "password": "test5",
    "student_id": 20211741,
    "name": "최수정",
    "college": "자연과학대학",
    "major": "물리학",
    "grade": 3,
    "phone_number": "010-4567-8901",
    "e_mail": "sujeong@example.com",
}


# 동아리 데이터
club1 = {
    "club_name": "빛누리",
    "category": "창작전시분과",
    "banner_path": None,
    "introduction": "사진동아리 입니다.",
}

club2 = {
    "club_name": "코딩마스터",
    "category": "학술분과",
    "banner_path": None,
    "introduction": "프로그래밍을 배우고 연구하는 동아리입니다.",
}

club3 = {
    "club_name": "음악사랑",
    "category": "예술분과",
    "banner_path": None,
    "introduction": "음악을 사랑하는 사람들의 모임입니다.",
}


# 추가된 동아리 데이터
club4 = {
    "club_name": "스포츠매니아",
    "category": "체육분과",
    "banner_path": None,
    "introduction": "다양한 스포츠 활동을 즐기는 동아리입니다.",
}

club5 = {
    "club_name": "책읽는사람들",
    "category": "문화분과",
    "banner_path": None,
    "introduction": "독서를 좋아하는 사람들의 모임입니다.",
}


# Recruiting 테스트 데이터
Recruiting1 = {
    "club_name": "빛누리",
    "capacity": 10,  # 모집 인원
    "start_date": "2025-04-01",  # 모집 시작일
    "end_date": "2025-04-15",  # 모집 종료일
}

Recruiting2 = {
    "club_name": "코딩마스터",
    "capacity": 15,
    "start_date": "2025-04-05",
    "end_date": "2025-04-20",
}

Recruiting3 = {
    "club_name": "음악사랑",
    "capacity": 8,
    "start_date": "2025-04-10",
    "end_date": "2025-04-25",
}



# 기존 동아리 리스트에 추가
users =[user1, user2, user3, user4, user5]
clubs = [club1, club2, club3, club4, club5]


# 모집 데이터 리스트
recruitings = [Recruiting1, Recruiting2, Recruiting3]



# ===================================================






# 테스트 코드 ================================================================================================================================================================================================================================================

connection = sql_runner.get_db_connection()

# 유저 가입
for user in users:
    sql_runner_User.regist(connection, user)

# 동아리 생성
for club in clubs:
    sql_runner_Club.add_club(connection, club)

# 각 동아리 임원진으로 임명
for i in range(5):
    club_name = clubs[i]['club_name']
    ID = users[i]['ID']
    sql_runner_Club.add_new_crew(connection, ID, club_name)
    sql_runner_Club.change_position(connection, ID, club_name, "임원진")
    sql_runner_Club.change_position(connection, ID, club_name, "회장", attribute="position")

# 동아리 초대 전송
sql_runner_Club.send_invitation(connection, "빛누리", "test2")



# contents = {
#     "club_name" : "빛누리",
#     "post_type" : "activity",
#     "title" : "빛누리 신입부원 모집한다",
#     "text" : "빛누리로 오라"
# }

# sql_runner_Club.add_post(connection, contents)


connection.close()

# ===================================================