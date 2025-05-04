import pymysql
import pendulum
import uuid


from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER

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

     
    def easy_runner(self, sql, method):
        connection = self.get_db_connection()
        result = None

        try: 
            with connection.cursor() as cursor:
                cursor.execute(sql)
                if method == "fetchall":
                    result = cursor.fetchall()
                elif method == "fechone":
                    result = cursor.fetchone()
                elif method == "commit":
                    connection.commit()
                    result = 1
        except pymysql.MySQLError as e:
            print(f'Error at easy_sql_runner : {e}')
            result = 0

        return result

# ================================================================================================================================================================================================================================================


# 회원가입, 유저정보 조회
class User(SQL_runner):
    def add_User(self, connection, user): # 유저 추가
        sql = '''
            insert into Users
            values(%s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        data = self.info_mapper(user)

        flag = 1
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, data)
                connection.commit()  
        except pymysql.MySQLError as e:  
            print(f"Error at sql_runner.User.add_User : {e}")
            flag = 0
        return flag


    def get_User(self, connection, ID): # Users 테이블에서 입력된 ID에 대한 유저 정보를 가져옴
        sql = '''
            select * from Users
            where
                ID=%s
        '''

        result = None
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, (ID,))
                result = cursor.fetchone()
                # ID로 유저 정보를 검색
        except pymysql.MySQLError as e:
            print(f"Error at sql_runner.User.check_id_duplication : {e}")
        return result


    # high : 유저 가입
    def regist(self, connection, user): 
        ID = user['ID']

        flag = 1
        if not self.get_User(connection, ID): # 동일한 ID의 유저가 없다면 User행 추가
            self.add_User(connection, user)
        else:
            flag = 0
        return flag # ID 또는 이메일이 중복이 아니라면 참을 반환


    # high : 로그인 요청, 로그인 성공시 참을 반환
    def login(self, connection, ID, password):
        user = self.get_User(connection, ID)
        status = None

        try: 
            if user['password'] == password:
                status = 1
            else:
                status = 0
        except:
            status = 0

        return status


    def get_invitations(self, connection, ID): # 동아리 가입권유 조회
        sql = '''
            SELECT * FROM Invitations
            WHERE 
                ID = %s
        '''

        results = None
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, (ID, ))
                results = cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f'Error at sql_runner.User.get_invitations : {e}')

        return results
    

    def delete_invitations(self, connection, ID, club_name): # 동아리 가입권유 삭제(수락 또는 거절시 해당 메서드 사용)
        sql = '''
            DELETE FROM Invitations
            WHERE
                ID=%s AND club_name=%s
        '''

        flag = 1
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, (ID, club_name, ))
                connection.commit()
        except pymysql.MySQLError as e:
            print(f"Error ar sql_runner.User.delete_invitations : {e}")
            flag = 0
        return flag

    
    def get_posts(self, connection, club_name=None, post_type=None): # 포스트 테이블에서만 조회 
        sql = '''
            SELECT * FROM Posts
            WHERE 1=1
        '''
        params = []

        if club_name is not None:
            sql += ' AND club_name=%s'
            params.append(club_name)
        
        if post_type is not None:
            sql += ' AND post_type=%s'
            params.append(post_type)
        
        sql += ' ORDER BY added DESC'

        results = None
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, tuple(params))
                results = cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f"Error at sql_runner.User.get_posts : {e}")
            results = 0
        return results



    def get_entire_post(self, connection, post_ID): # 글 하나 전체를 조회
        sql1 = '''
            SELECT post_type FROM Posts
            WHERE
                post_ID=%s
        '''
        post_type = None
        table = None
        results = None
        try: 
            with connection.cursor() as cursor:
                cursor.execute(sql1, (post_ID, ))
                post_type = cursor.fetchone()
                if post_type == None:
                    return 2

                post_type = post_type['post_type']
                if post_type=="activity":
                    table = "Club_Activities"
                elif post_type == "union":
                    table = "Union_activities"
                elif post_type == "recruiting":
                    table = "Recruitings"
                
                sql2 = f'''
                    SELECT * 
                    FROM Posts
                            NATURAL JOIN
                                {table}
                    WHERE
                        post_ID="{post_ID}"
                '''
                cursor.execute(sql2)
                results = cursor.fetchone()
        except pymysql.MySQLError as e:
            print(f"Error at sql_runner.User.get_entire_post : {e}")

        return results
            

    def add_applicants(self, connection, ID, post_ID): # 포스팅 글 지원 
        sql = '''
            INSERT INTO Applicants
            VALUES(%s, %s)
        '''

        flag = None
        
        try:
            result = self.get_entire_post(connection, post_ID)
            if result['post_type'] == "activity":
                flag = 3
            else:
                with connection.cursor() as cursor:
                    cursor.execute(sql, (post_ID, ID, ))
                    connection.commit()
                    flag = 1
        except pymysql.MySQLError as e:
            print(f'Error at sql_runner.User.add_applicants : {e}')
            # 중복지원시
            if e.args[0] == 1062:
                flag = 2
            else:
                flag = 0
        
        return flag


    def add_review(self, connection, review_contents): # Club_Reviews에 추가
        sql = '''
            INSERT INTO 
            Club_Reviews(review_ID, ID, club_name, score, review, added)
            values(%s, %s, %s, %s, %s, %s)
        '''
        review_ID =str(uuid.uuid4())
        ID = review_contents['ID']
        club_name = review_contents['club_name']
        score = review_contents['score']
        review = review_contents['review']
        added = pendulum.now().format("YYYY-MM-DD")
        
        flag = None
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, (review_ID, ID, club_name, score, review, added))
                connection.commit()
                flag = 1
        except pymysql.MySQLError as e:
            print(f"Error at the sql_runner.User.add_review : {e}")
            flag = 0
        return flag


    def get_reviews(self, connection, club_name): # 리뷰 조회
        print(club_name)
        sql = '''
            SELECT * 
            FROM Club_Reviews
            where
                club_name=%s
            ORDER BY
                added DESC
        '''

        results = None
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, (club_name,))
                results = cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f"Error at the sql_runner.User.get_reivews : {e}")
            raise
        return results


    def delete_review(self, connection, review_ID): # review_ID로 리뷰 삭제
        sql = '''
            DELETE FROM Club_Reviews
            WHERE
                review_ID=%s
        '''

        flag = None
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, (review_ID, ))
                connection.commit()
                flag = 1
        except pymysql.MySQLError as e:
            print(f"Error at the sql_runner.User.delete_review : {e}")
            flag = 0
            raise
        return flag

    
    def check_my_review(self, connection, ID, review_ID): # 본인이 작성한 리뷰인지 확인
        sql = '''
            SElECT * FROM Club_Reviews
            WHERE
                review_ID=%s
        '''

        flag = None
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, (review_ID, ))
                result = cursor.fetchone()
                flag = 1 if result['ID'] == ID else 2
        except pymysql.MySQLError as e:
            print(f"Error at the sql_runner.User.check_my_review : {e}")
            flag = 0
        return flag 


    def get_club(self, connection, club_name): # 동아리 정보 조회(전체 or 특정)
        sql = None
        if club_name == None:
            sql = '''
                SELECT 
                    club_name,
                    category,
                    rating,
                    activity,
                    score 
                FROM Clubs
            '''
        else:
            sql = f'''
                SELECT * FROM Clubs
                WHERE 
                    club_name="{club_name}"

            '''

        results = None
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f"Error at the sql_runner.User.get_club : {e}")
            results = 0
        
        return results

    
    def get_club_ranking(self, connection): # 동아리 랭킹 조회
        sql = '''
            SELECT * FROM Ranking
        '''
        
        results = None
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f"Error at the sql_runner.User.get_club_ranking : {e}")
            results = 0

        return results


    def get_my_club(self, connection, ID): # 내 동아리 불러오기
        sql = '''
            SELECT 
                club_name,
                category,
                rating,
                activity,
                score
            FROM 
                Clubs NATURAL JOIN Crews
            WHERE
                ID=%s
        '''

        results = None
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, (ID))
                results = cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f"Error at the sql_runner.User.get_my_club : {e}")
            results = 0
        
        return results
        


# ================================================================================================================================================================================================================================================


class Club(SQL_runner):
    def add_club(self, connection, club): # Clubs테이블의 행 추가
        sql = '''
            INSERT INTO Clubs(club_name, category, banner_path, introduction)
            VALUES(%s, %s, %s, %s)
        '''
        data = self.info_mapper(club)

        flag = 1
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, data)
                connection.commit()
        except pymysql.MySQLError as e:
            print(f"Error at sql_runner.Club.add_club : {e}")
            flag = 0
        finally: 
            return flag


    def add_new_crew(self, connection, ID, club_name): # Crews에 행 추가
        joinded_date = pendulum.now().format('YYYY-MM-DD')
        # crews : club_name(varchar), id(varchar), rule(varchar) 부원 / 임원진, position 직책(회장, 부회장, 총무 등등), joined(date)
        sql = '''
            INSERT INTO Crews(ID, club_name, joined)
            VALUES(%s, %s, %s)
        '''
        
        flag = 1
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, (ID, club_name, joinded_date, ))
                connection.commit()
        except pymysql.MySQLError as e:
            print(f'Error at sql_runner.Club.add_new_crew : {e}')
            if e.args[0] == 1062:
                flag = 2
            else:
                flag = 0
        
        return flag
    
    def delete_crew(self, connection, ID, club_name): # 크루 삭제(신규 회원을 추가하는 도중 오류가 발생하면 사용)
        sql = '''
            DELETE FROM Crews
            WHERE
                ID=%s,
                club_name=%s
        '''

        flag = None
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, (ID, club_name, ))
                connection.commit()
                flag = 1
        except pymysql.MySQLError as e:
            print(f"Error at the sql_runner.Club.delete_crew : {e}")
            flag = 0
        
        return flag

    def delete_applicant(self, connection, ID, post_ID): # 동아리 지원자 삭제
        sql = '''
            DELETE FROM Applicants
            WHERE
                post_ID=%s AND ID=%s
        '''
        
        flag = None
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, (post_ID, ID))
                connection.commit()
                flag = 1
        except pymysql.MySQLError as e:
            print(f"Error at sql_runner.Club.delete_applicants : {e}")
            falg = 0
            raise
        return flag


    def get_crew_list(self, connection, club_name): # 동아리 리스트 조회
        sql = '''
            select * from Crews
            where
               club_name=%s
        '''

        results = None
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, (club_name, ))
                results = cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f"Error at sql_runner.Club.get_crew_list : {e}")
            raise
        
        return results

    def get_crew_info(self, connection, club_name):
        sql = '''
            SELECT 
                ID as 아이디,
                rule AS 직책,
                position AS 부서,
                name AS 이름, 
                student_id AS 학번, 
                college AS 단과대, 
                major AS 전공, 
                grade AS 학년, 
                phone_number AS 전화번호,
                e_mail AS 이메일
            FROM 
                Crews NATURAL JOIN Users
            WHERE
                club_name=%s
        '''

        results = None
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, (club_name, ))
                results = cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f"Error at the sql_runner.Club.get_crew_list : {e}")
            results = 0
        return results


    def check_rule(self, connection, ID, club_name): # 동아리원 직책 확인
        sql = '''
            select rule, position from Crews
            where
                ID=%s and club_name=%s
        '''
        
        results = None
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, (ID, club_name,))
                results = cursor.fetchone()
        except pymysql.MySQLError as e:
            print(f"Error at sql_runner.Club.check_rule : {e}")    
        return results
    

    def change_position(self, connection, ID, club_name, value, attribute="rule"): # 동아리원 직책 변경
        if attribute not in ["rule", "position"]:  # 허용된 컬럼만 사용
            raise ValueError("Invalid attribute")
        
        sql = f'''
            UPDATE Crews
            SET {attribute}="{value}"
            WHERE
                club_name="{club_name}" AND
                ID="{ID}"
        '''

        flag = 1
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                connection.commit()
        except pymysql.MySQLError as e:
            print(f"Error at sql_runner.Club.change_rule : {e}")
            flag = 0    
        return flag
    
    
    def send_invitation(self, connection, club_name, target): # 초대권 전송
        sql = '''
            INSERT INTO Invitations
            VALUES(%s, %s)
        '''

        flag = 1        
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, (club_name, target, ))
                connection.commit()
        except pymysql.MySQLError as e:
            print(f'Error at sql_runner.Club.send_invitation : {e}')
            if e.args[0] == 1062:
                flag = 2
        
        return flag


    def add_activity(self, connection, post_ID, format): # 활동글 게시
        activity_day = format['activity_day']
        activity_image = format['activity_image']

        sql = '''
            INSERT INTO Club_Activities
            values(%s, %s, %s)
        '''

        flag = None
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, (post_ID, activity_day, activity_image, ))
                connection.commit()
                flag = 1
        except pymysql.MySQLError as e:
            print(f"Error at sql_runner.Club.add_activity : {e}")
            flag = 0
        
        return flag


    def add_union_activites(self, connection, post_ID, format): # 연합활동 게시
        start_date = format['start_date']
        end_date = format['end_date']

        sql = '''
            INSERT INTO 
            Union_activities(post_ID, start_date, end_date)
            values(%s, %s, %s)
        '''

        flag = None
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, (post_ID, start_date, end_date,))
                connection.commit()
                flag =  1
        except pymysql.MySQLError as e:
            print(f"Error at sql_runner.Club.add_Union_activites : {e}")
            flag = 0

        return flag


    def add_recruitings(self, connectoin, post_ID, format): # 리크루팅 글 게시
        capacity = format['capacity']
        start_date = format['start_date']
        end_date = format['end_date']

        sql = '''
            INSERT INTO
            Recruitings(post_ID, capacity, start_date, end_date)
            values(%s, %s, %s, %s)
        '''

        flag = None
        try:
            with connectoin.cursor() as cursor:
                cursor.execute(sql, (post_ID, capacity, start_date, end_date, ))
                connectoin.commit()
                flag = 1
        except pymysql.MySQLError as e:
            print(f"Error at sql_runner.Club.add)recruitings : {e}")
            flag = 0
        return flag


    def add_post(self, connection, post_ID, contents): # post_type = activity, union, recruiting
        sql = '''
            INSERT INTO 
            Posts(post_ID, club_name, post_type, title, text, added)
            values(%s, %s, %s, %s, %s, %s)
        '''
       
        club_name = contents['club_name']
        post_type = contents['post_type']
        title = contents['title']
        text = contents['text']
        added = pendulum.now().format("YYYY-MM-DD")


        flag = None
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, (post_ID, club_name, post_type, title, text, added, ))
                connection.commit()
                flag = 1
        except pymysql.MySQLError as e:
            print(f"Error at sql_runner.Club.add_post : {e}")
            flag = 0

        return flag
        
    
    # high : posting
    def post(self, connection, contents, format):
        
        post_ID = str(uuid.uuid4())
        post_type = contents['post_type']

        flag = None
        # add_post를 성공하면
        if self.add_post(connection, post_ID, contents):
            if post_type == "activity":
                flag = self.add_activity(connection, post_ID, format)
            elif post_type == "union":
                flag = self.add_union_activites(connection, post_ID, format)
            elif post_type == "recruiting":
                flag = self.add_recruitings(connection, post_ID, format)
        # activity, union, recruiting을 게시하는 도중 문제가 발생하면 Post테이블에 올렸던 글을 삭제
        if flag == 0:
            self.delete_post(connection, post_ID)    

        return flag

    def delete_post(self, connection, post_ID): # 포스팅 삭제
        sql = '''
            delete from Posts
            where
                post_ID=%s
        '''
        
        flag = None

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, (post_ID, ))
                connection.commit()
                flag = 1
        except pymysql.MySQLError as e:
            print(f"Error at mysql_runner.Club.delete_post : {e}")
            flag = 0

        return flag 


    def get_applicants(self, connection, post_ID): # 지원자 조회
        sql = '''
            select 
                ID,
                Name,
                e_mail
            from 
                Applicants
                    NATURAL JOIN Users
            where
                post_ID=%s
        '''

        results = None
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, (post_ID))
                results = cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f'Error at sql_runner.User.get_applicants : {e}')
            raise

        return results


    def add_club_fee_table(self, connection, club_name, IDs, fee): # 회비 납부 테이블 발행, ID는 리스트로 해당 리스트에 있는 ID를 모두 추가한다 
        sql = '''
            INSERT INTO 
            Club_fee_table(club_name, ID, publication, fee)
            VALUES
        '''

        publication = pendulum.now().format("YYYY-MM-DD")
        values = []
        placeholders = []

        # sql문 생성
        for ID in IDs:
            placeholders.append("(%s, %s, %s, %s)")
            values.extend([club_name, ID, publication, fee])

        sql += ",\n".join(placeholders)

        status = None
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, values)
                connection.commit()
                status = 1
        except Exception as e:
            print(f"Error at the sql_runner.Club.add_club_fee_table : {e}")
            if e.args[0] == 1062:
                status = 2
            else:
                status = 0
        return status
    

    def update_payment(self, connection, club_name, IDs, publications, state=1):  # 납부 완료 전환
        placeholders = ' OR '.join(['(ID=%s AND publication=%s)'] * len(IDs))
        sql = '''
            UPDATE Club_fee_table
            SET payment = %s
            WHERE 
                club_name = %s AND 
                ({})
        '''.format(placeholders)

        params = [state, club_name]
        for ID, pub in zip(IDs, publications):
            params.extend([ID, pub])

        flag = None
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, params)
                connection.commit()
                flag = 1
        except pymysql.MySQLError as e:
            print(f"Error at the sql_runner.Club.update_payment : {e}")
            flag = 0

        return flag


    def payment_cancel(self, connection, club_name, IDs, publications): # 납부 발행 취소
        sql = f'''
            DELETE FROM Club_fee_table
            WHERE
                club_name=%s AND
                ({' OR\n'.join(['ID=%s AND publication=%s']*len(IDs))})
        '''

        parmas = [club_name]
        for ID, publicatoin in zip(IDs, publications):
            parmas.extend([ID, publicatoin])
        
        flag = None
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, parmas)
                connection.commit()
                flag = 1
        except pymysql.MySQLError as e:
            print(f"Error at the sql_runner.Club.payment_cancel : {e}")
            flag = 0
        
        return flag

    
    # 납부 테이블 조회 
    def get_payment_table(self, connection, club_name, publication=None):
        sql = '''
            SELECT * FROM Club_fee_table
            WHERE
                club_name=%s
        '''

        if publication != None:
            sql += f'''
                AND publication="{publication}"
            '''

        results = None
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, (club_name, ))
                results = cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f"Error at the sql_runner.Club.get_payment_table : {e}")
        
        return results




sql_runner = SQL_runner() 
sql_runner_User = User()
sql_runner_Club = Club()


