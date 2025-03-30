import pymysql
import jwt
import pendulum

from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER
from config import DEFAULT_ARGS


# ================================================================================================================================================================================================================================================


class SQL_runner:
    # db연결 및 connection 객체 생성
    def get_db_connection(self, DB_HOST=DB_HOST, DB_USER=DB_USER, DB_PASSWORD=DB_PASSWORD, DB_NAME=DB_NAME):
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor  # 쿼리 결과를 dict로 반환
        )
        return connection

    def info_mapper(self, data): # sql문 실행을 위한 tuple생성
        return tuple([data[key] for key in list(data)])
        

# ================================================================================================================================================================================================================================================


# 회원가입, 유저정보 조회
class User(SQL_runner):
    def add_User(self, connection, user):
        sql = '''
            insert into Users
            values(%s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        data = self.info_mapper(user)

        flag = True
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, data)
                connection.commit()  
        except pymysql.MySQLError as e:  
            print(f"Error at sql_runner.User.add_User : {e}")
            flag = False
        return flag

    def get_User(self, connection, ID): # Users 테이블에서 입력된 ID에 대한 유저 정보를 가져옴
        sql = f'''
            select * from Users
            where
                ID="{ID}"
        '''
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchone()
                # ID로 유저 정보를 검색
                return result
        except pymysql.MySQLError as e:
            print(f"Error at sql_runner.User.check_id_duplication : {e}")
            return None
            
    # high : 유저 가입
    def regist(self, user):
        connection = self.get_db_connection(**DEFAULT_ARGS)
        ID = user['ID']

        flag = True
        if not self.get_User(connection, ID): # 동일한 ID의 유저가 없다면 User행 추가
            self.add_User(connection, user)
        else:
            flag = False

        connection.close()

        return flag # ID 또는 이메일이 중복이 아니라면 참을 반환

    # high : 로그인 요청, 로그인 성공시 참을 반환
    # 서버에서는 jwt로 클라이언트로 액세스 토큰을 날려야 함
    def login(self, ID, password):
        connection = self.get_db_connection(**DEFAULT_ARGS)

        user = self.get_User(connection, ID)
        connection.close()

        flag = True if (user['password'] == password) else False
        return flag
            

# ================================================================================================================================================================================================================================================


class Club(SQL_runner):
    def add_club(self, connection, club): # Clubs테이블의 행 추가
        sql = '''
            INSERT INTO Clubs(club_name, category, banner_path, introduction)
            VALUES(%s, %s, %s, %s)
        '''
        data = self.info_mapper(club)

        flag = True
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, data)
                connection.commit()
        except pymysql.MySQLError as e:
            print(f"Error at sql_runner.Club.add_club : {e}")
            flag = False
        finally: 
            return flag

    def get_club(self, connection, club_name): # Clubs 테이블에서 입력된 club_name에 대한 동아리 정보를 가져옴
        sql = f'''
            select * from Clubs
            where
                club_name="{club_name}"
        '''
        result = None
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchone()
        except pymysql.MySQLError as e:
            print(f"Error at sql_runner.Club.get_club : {e}")
        finally:
            return result

    def add_new_crew(self, connection, crew): # Crews에 행 추가
        joinded_date = pendulum.now().format('YYYY-MM-DD')
        # crews : club_name(varchar), id(varchar), rule(varchar) 부원 / 임원진, position 직책(회장, 부회장, 총무 등등), joined(date)
        data = self.info_mapper(crew) + (joinded_date, ) 

        sql = '''
            INSERT INTO Crews
            VALUES(%s,%s,%s,%s,%s);
        '''
        
        flag = True
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, data)
                connection.commit()
        except pymysql.MySQLError as e:
            print(f'Error at sql_runner.Club.add_new_crew : {e}')
            flag = False
        
        return flag
    
    def get_crew_list(self, connection, club_name):
        sql = f'''
            select * from Crews
            where
               club_name="{club_name}" 
        '''

        results = None
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f"Error at sql_runner.Club.get_crew_list : {e}")
        
        return results

    def check_rule(self, connection, ID, club_name): # 동아리원 직책 확인
        sql = f'''
            select rule, position from Crews
            where
                ID="{ID}" and club_name="{club_name}"
        '''
        
        results = None
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                results = cursor.fetchone()
        except pymysql.MySQLError as e:
            print(f"Error at sql_runner.Club.check_rule : {e}")    
        return results
    
    def change_rule(self, connection, ID, club_name, value, object="rule"): # rule을 이용하면 임원진 설정 가능, position을 이용하면 직책 설정
        sql = f'''
            UPDATE Crews
            SET
                {object}="{value}"
            WHERE
                club_name="{club_name}" AND
                ID="{ID}" 
        '''

        flag = True
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                connection.commit()
        except pymysql.MySQLError as e:
            print(f"Error at sql_runner.Club.change_rule : {e}")
            flag = False    
        return flag
    

# ================================================================================================================================================================================================================================================



user1 = {
    "ID" : "tgur0620",
    "password" : "ajdcjddl2" ,
    "student_id": 20211737,
    "name" : "윤세혁",
    "college" : "IT",
    "major" : "AI",
    "grade" : 3,
    "phone_number" : "010-4823-0620",
    "e_mail" : "tgur0620@gmail.com",
}

user2 = {
    "ID" : "tgur7170",
    "password" : "ajdcjddl2" ,
    "student_id": 20211737,
    "name" : "윤세혁",
    "college" : "IT",
    "major" : "AI",
    "grade" : 3,
    "phone_number" : "010-4823-0620",
    "e_mail" : "tgur0620@gmail.com",
}

club1 = {
    "club_name" : "빛누리",
    "category" : "창작전시분과",
    "banner_path" : None,
    "introduction" : "사진동아리 입니다."
}

crew1 = {
    "club_name" : "빛누리",
    "ID"  : "tgur0620",
    "rule" : "부원",
    "position" : None,
}



sql_runner = SQL_runner() 
sql_runner_User = User()
sql_runner_Club = Club()

connection = sql_runner.get_db_connection()



print(sql_runner_Club.check_rule(connection, "tgur0620", "빛누리"))

connection.close()
