-- CREATE DATABASE IF NOT EXISTS ssu_shook
-- CHARACTER SET utf8mb4
-- COLLATE utf8mb4_general_ci;

-- USE ssu_shook;


-- CREATE TABLE Applicants
-- (
--   post_ID VARCHAR(50) NOT NULL COMMENT '게시글 아이디',
--   ID      VARCHAR(50) NOT NULL COMMENT '로그인 아이디',
--   PRIMARY KEY(post_ID, ID)
-- ) COMMENT '지원자';

-- CREATE TABLE Club_Activities
-- (
--   post_ID        VARCHAR(50)  NOT NULL COMMENT '게시글 아이디',
--   activity_day   DATE         NOT NULL COMMENT '활동일',
--   activity_image VARCHAR(100) NULL     COMMENT '활동사진 경로',
--   PRIMARY KEY (post_ID)
-- ) COMMENT '동아리 활동 내역';

-- CREATE TABLE Club_fee_table
-- (
--   club_name   VARCHAR(50) NOT NULL COMMENT '동아리 명',
--   ID          VARCHAR(50) NOT NULL COMMENT '로그인 아이디',
--   publication DATE        NOT NULL COMMENT '발행일',
--   fee         INT         NOT NULL COMMENT '청구 비용',
--   payment     INT         NOT NULL DEFAULT 0 COMMENT '납부 여부',
--   PRIMARY KEY (club_name, ID, publication)
-- ) COMMENT '회비납부 관리 테이블';

-- CREATE TABLE Club_Reviews
-- (
--   review_ID VARCHAR(50)  NOT NULL COMMENT '리뷰 아이디',
--   ID        VARCHAR(50)  NOT NULL COMMENT '로그인 아이디',
--   club_name VARCHAR(50)  NOT NULL COMMENT '동아리 명',
--   score     INT          NOT NULL COMMENT '별점',
--   review    VARCHAR(300) NOT NULL COMMENT '리뷰 내용',
--   added     DATE         NOT NULL COMMENT '작성일',
--   updated   DATE         NULL     COMMENT '수정일',
--   PRIMARY KEY (review_ID)
-- ) COMMENT '동아리 리뷰';

-- CREATE TABLE Clubs
-- (
--   club_name    VARCHAR(50)  NOT NULL COMMENT '동아리 명',
--   category     VARCHAR(50)  NOT NULL COMMENT '분과구분',
--   banner_path  VARCHAR(100) NULL     COMMENT '동아리 배너 이미지 경로',
--   introduction VARCHAR(300) NOT NULL COMMENT '동아리 소개',
--   rating       INT          NOT NULL DEFAULT 0 COMMENT '동아리 리뷰 평점',
--   activity     INT          NOT NULL DEFAULT 0 COMMENT '동아리 활동 점수',
--   score        INT          NOT NULL DEFAULT 0 COMMENT '동아리 랭킹 점수(리뷰 및 활동점수 취합)',
--   PRIMARY KEY (club_name)
-- ) COMMENT '동아리 목록';

-- ALTER TABLE Clubs
--   ADD CONSTRAINT UQ_club_name UNIQUE (club_name);

-- CREATE TABLE Crews
-- (
--   club_name VARCHAR(50) NOT NULL COMMENT '동아리 명',
--   ID        VARCHAR(50) NOT NULL COMMENT '로그인 아이디',
--   rule      VARCHAR(50) NOT NULL DEFAULT '부원' COMMENT '역할(부원 / 임원진)',
--   position  VARCHAR(50) NULL     COMMENT '직책(회장, 부회장, 총무 등등)',
--   joined    DATE        NOT NULL COMMENT '가입일시',
--   PRIMARY KEY (club_name, ID)
-- ) COMMENT '동아리 회원 리스트';

-- CREATE TABLE Invitations
-- (
--   club_name VARCHAR(50) NOT NULL COMMENT '동아리 명',
--   ID        VARCHAR(50) NOT NULL COMMENT '로그인 아이디',
--   PRIMARY KEY (club_name, ID)
-- ) COMMENT '동아리 초대자 목록';

-- CREATE TABLE New_club_Applicants
-- (
--   New_club_id VARCHAR(50) NOT NULL COMMENT '신규 동아리 개설 모집 아이디',
--   ID          VARCHAR(50) NOT NULL COMMENT '로그인 아이디'
-- ) COMMENT '신규 동아리 임원진 신청자 리스틑';

-- CREATE TABLE New_clubs
-- (
--   new_club_id           VARCHAR(50)   NOT NULL COMMENT '신규 동아리 개설 모집 아이디',
--   new_club_name         VARCHAR(50)   NOT NULL COMMENT '신규 동아리 명',
--   new_club_introduction VARCHAR(1000) NOT NULL COMMENT '신규 동아리 임원진 모집 요강',
--   new_club_applicants   INT           NOT NULL DEFAULT 0 COMMENT '지원자 수',
--   PRIMARY KEY (new_club_id)
-- ) COMMENT '신규 동아리 임원진 모집 공고';

-- CREATE TABLE Posts
-- (
--   post_ID   VARCHAR(50)   NOT NULL COMMENT '게시글 아이디',
--   club_name VARCHAR(50)   NOT NULL COMMENT '동아리 명',
--   post_type VARCHAR(20)   NOT NULL COMMENT '게시글 타입',
--   title     VARCHAR(100)  NOT NULL COMMENT '게시글 제목',
--   text      VARCHAR(1000) NULL     COMMENT '게시글 내용',
--   added     DATE          NOT NULL COMMENT '게시일',
--   updated   DATE          NULL     COMMENT '수정일',
--   PRIMARY KEY (post_ID)
-- ) COMMENT '게시글';

-- CREATE TABLE Recruitings
-- (
--   post_ID    VARCHAR(50) NOT NULL COMMENT '게시글 아이디',
--   capacity   INT         NOT NULL COMMENT '모집인원',
--   applicants INT         NOT NULL DEFAULT 0 COMMENT '신청자수',
--   start_date DATE        NOT NULL COMMENT '모집 시작일',
--   end_date   DATE        NOT NULL COMMENT '모집 종료일',
--   PRIMARY KEY (post_ID)
-- ) COMMENT '부원 모집 게시글';

-- CREATE TABLE Union_activities
-- (
--   post_ID         VARCHAR(50) NOT NULL COMMENT '게시글 아이디',
--   start_date      DATE        NOT NULL COMMENT '모집 시작일',
--   end_date        DATE        NOT NULL COMMENT '모집 종료일',
--   applicants_club INT         NOT NULL DEFAULT 0 COMMENT '참여희망 동아리 수',
--   PRIMARY KEY (post_ID)
-- ) COMMENT '연합활동 모집 게시글';

-- CREATE TABLE Users
-- (
--   ID           VARCHAR(50) NOT NULL COMMENT '로그인 아이디',
--   password     VARCHAR(50) NOT NULL COMMENT '로그인 패스워드',
--   student_id   INT         NOT NULL COMMENT '학번',
--   name         VARCHAR(50) NOT NULL COMMENT '이름',
--   college      VARCHAR(50) NULL     COMMENT '단과대',
--   major        VARCHAR(50) NOT NULL COMMENT '학과',
--   grade        INT         NOT NULL COMMENT '학년',
--   phone_number VARCHAR(20) NOT NULL COMMENT '전화번호',
--   e_mail       VARCHAR(50) NOT NULL COMMENT '이메일',
--   PRIMARY KEY (ID)
-- ) COMMENT '사용자 목록';

-- ALTER TABLE Club_Reviews
--   ADD CONSTRAINT FK_Clubs_TO_Club_Reviews
--     FOREIGN KEY (club_name)
--     REFERENCES Clubs (club_name) ON DELETE CASCADE;

-- ALTER TABLE Club_Reviews
--   ADD CONSTRAINT FK_Users_TO_Club_Reviews
--     FOREIGN KEY (ID)
--     REFERENCES Users (ID);

-- ALTER TABLE Crews
--   ADD CONSTRAINT FK_Users_TO_Crews
--     FOREIGN KEY (ID)
--     REFERENCES Users (ID) ON DELETE CASCADE;

-- ALTER TABLE New_club_Applicants
--   ADD CONSTRAINT FK_Users_TO_New_club_Applicants
--     FOREIGN KEY (ID)
--     REFERENCES Users (ID) ON DELETE CASCADE;

-- ALTER TABLE Invitations
--   ADD CONSTRAINT FK_Clubs_TO_Invitations
--     FOREIGN KEY (club_name)
--     REFERENCES Clubs (club_name) ON DELETE CASCADE;

-- ALTER TABLE Invitations
--   ADD CONSTRAINT FK_Users_TO_Invitations
--     FOREIGN KEY (ID)
--     REFERENCES Users (ID) ON DELETE CASCADE;

-- ALTER TABLE Posts
--   ADD CONSTRAINT FK_Clubs_TO_Posts
--     FOREIGN KEY (club_name)
--     REFERENCES Clubs (club_name) ON DELETE CASCADE;

-- ALTER TABLE Recruitings
--   ADD CONSTRAINT FK_Posts_TO_Recruitings
--     FOREIGN KEY (post_ID)
--     REFERENCES Posts (post_ID) ON DELETE CASCADE;

-- ALTER TABLE Union_activities
--   ADD CONSTRAINT FK_Posts_TO_Union_activities
--     FOREIGN KEY (post_ID)
--     REFERENCES Posts (post_ID) ON DELETE CASCADE;

-- ALTER TABLE Club_Activities
--   ADD CONSTRAINT FK_Posts_TO_Club_Activities
--     FOREIGN KEY (post_ID)
--     REFERENCES Posts (post_ID) ON DELETE CASCADE;

-- ALTER TABLE New_club_Applicants
--   ADD CONSTRAINT FK_New_clubs_TO_New_club_Applicants
--     FOREIGN KEY (New_club_id) 
--     REFERENCES New_clubs (new_club_id) ON DELETE CASCADE;

-- ALTER TABLE Club_fee_table
--   ADD CONSTRAINT FK_Crews_TO_Club_fee_table
--     FOREIGN KEY (club_name, ID)
--     REFERENCES Crews (club_name, ID) ON DELETE CASCADE;

-- ALTER TABLE Crews
--   ADD CONSTRAINT FK_Clubs_TO_Crews
--     FOREIGN KEY (club_name)
--     REFERENCES Clubs (club_name) ON DELETE CASCADE;

-- ALTER TABLE Applicants
--   ADD CONSTRAINT FK_Users_TO_Applicants
--     FOREIGN KEY (ID)
--     REFERENCES Users (ID) ON DELETE CASCADE;

-- ALTER TABLE Applicants
--   ADD CONSTRAINT FK_Posts_TO_Applicants
--     FOREIGN KEY (post_ID) REFERENCES Posts (post_ID) ON DELETE CASCADE;

CREATE DATABASE IF NOT EXISTS ssu_shook
CHARACTER SET utf8mb4
COLLATE utf8mb4_general_ci;

USE ssu_shook;


CREATE TABLE Applicants
(
  post_ID VARCHAR(50) NOT NULL COMMENT '게시글 아이디',
  ID      VARCHAR(50) NOT NULL COMMENT '로그인 아이디',
  PRIMARY KEY(post_ID, ID)
) COMMENT '지원자';

CREATE TABLE Club_Activities
(
  post_ID        VARCHAR(50)  NOT NULL COMMENT '게시글 아이디',
  activity_day   DATE         NOT NULL COMMENT '활동일',
  activity_image VARCHAR(100) NULL     COMMENT '활동사진 경로',
  PRIMARY KEY (post_ID)
) COMMENT '동아리 활동 내역';

CREATE TABLE Club_fee_table
(
  club_name   VARCHAR(50) NOT NULL COMMENT '동아리 명',
  ID          VARCHAR(50) NOT NULL COMMENT '로그인 아이디',
  publication DATE        NOT NULL COMMENT '발행일',
  fee         INT         NOT NULL COMMENT '청구 비용',
  payment     INT         NOT NULL DEFAULT 0 COMMENT '납부 여부',
  PRIMARY KEY (club_name, ID, publication)
) COMMENT '회비납부 관리 테이블';

CREATE TABLE Club_Reviews
(
  review_ID VARCHAR(50)  NOT NULL COMMENT '리뷰 아이디',
  ID        VARCHAR(50)  NOT NULL COMMENT '로그인 아이디',
  club_name VARCHAR(50)  NOT NULL COMMENT '동아리 명',
  score     INT          NOT NULL COMMENT '별점',
  review    VARCHAR(300) NOT NULL COMMENT '리뷰 내용',
  added     DATE         NOT NULL COMMENT '작성일',
  updated   DATE         NULL     COMMENT '수정일',
  PRIMARY KEY (review_ID)
) COMMENT '동아리 리뷰';

CREATE TABLE Clubs
(
  club_name    VARCHAR(50)  NOT NULL COMMENT '동아리 명',
  category     VARCHAR(50)  NOT NULL COMMENT '분과구분',
  banner_path  VARCHAR(100) NULL     COMMENT '동아리 배너 이미지 경로',
  introduction VARCHAR(300) NOT NULL COMMENT '동아리 소개',
  rating       INT          NOT NULL DEFAULT 0 COMMENT '동아리 리뷰 평점',
  activity     INT          NOT NULL DEFAULT 0 COMMENT '동아리 활동 점수',
  score        INT          NOT NULL DEFAULT 0 COMMENT '동아리 랭킹 점수(리뷰 및 활동점수 취합)',
  PRIMARY KEY (club_name)
) COMMENT '동아리 목록';

ALTER TABLE Clubs
  ADD CONSTRAINT UQ_club_name UNIQUE (club_name);

CREATE TABLE Crews
(
  club_name VARCHAR(50) NOT NULL COMMENT '동아리 명',
  ID        VARCHAR(50) NOT NULL COMMENT '로그인 아이디',
  rule      VARCHAR(50) NOT NULL DEFAULT '부원' COMMENT '역할(부원 / 임원진)',
  position  VARCHAR(50) NULL     COMMENT '직책(회장, 부회장, 총무 등등)',
  joined    DATE        NOT NULL COMMENT '가입일시',
  PRIMARY KEY (club_name, ID)
) COMMENT '동아리 회원 리스트';

CREATE TABLE Invitations
(
  club_name VARCHAR(50) NOT NULL COMMENT '동아리 명',
  ID        VARCHAR(50) NOT NULL COMMENT '로그인 아이디',
  PRIMARY KEY (club_name, ID)
) COMMENT '동아리 초대자 목록';

CREATE TABLE New_club_Applicants
(
  New_club_id VARCHAR(50) NOT NULL COMMENT '신규 동아리 개설 모집 아이디',
  ID          VARCHAR(50) NOT NULL COMMENT '로그인 아이디'
) COMMENT '신규 동아리 임원진 신청자 리스틑';

CREATE TABLE New_clubs
(
  new_club_id           VARCHAR(50)   NOT NULL COMMENT '신규 동아리 개설 모집 아이디',
  new_club_name         VARCHAR(50)   NOT NULL COMMENT '신규 동아리 명',
  new_club_introduction VARCHAR(1000) NOT NULL COMMENT '신규 동아리 임원진 모집 요강',
  new_club_applicants   INT           NOT NULL DEFAULT 0 COMMENT '지원자 수',
  PRIMARY KEY (new_club_id)
) COMMENT '신규 동아리 임원진 모집 공고';

CREATE TABLE Posts
(
  post_ID   VARCHAR(50)   NOT NULL COMMENT '게시글 아이디',
  club_name VARCHAR(50)   NOT NULL COMMENT '동아리 명',
  post_type VARCHAR(20)   NOT NULL COMMENT '게시글 타입',
  title     VARCHAR(100)  NOT NULL COMMENT '게시글 제목',
  text      VARCHAR(1000) NULL     COMMENT '게시글 내용',
  added     DATE          NOT NULL COMMENT '게시일',
  updated   DATE          NULL     COMMENT '수정일',
  PRIMARY KEY (post_ID)
) COMMENT '게시글';

CREATE TABLE Recruitings
(
  post_ID    VARCHAR(50) NOT NULL COMMENT '게시글 아이디',
  capacity   INT         NOT NULL COMMENT '모집인원',
  applicants INT         NOT NULL DEFAULT 0 COMMENT '신청자수',
  start_date DATE        NOT NULL COMMENT '모집 시작일',
  end_date   DATE        NOT NULL COMMENT '모집 종료일',
  PRIMARY KEY (post_ID)
) COMMENT '부원 모집 게시글';

CREATE TABLE Union_activities
(
  post_ID         VARCHAR(50) NOT NULL COMMENT '게시글 아이디',
  start_date      DATE        NOT NULL COMMENT '모집 시작일',
  end_date        DATE        NOT NULL COMMENT '모집 종료일',
  applicants_club INT         NOT NULL DEFAULT 0 COMMENT '참여희망 동아리 수',
  PRIMARY KEY (post_ID)
) COMMENT '연합활동 모집 게시글';

CREATE TABLE Users
(
  ID           VARCHAR(50) NOT NULL COMMENT '로그인 아이디',
  password     VARCHAR(50) NOT NULL COMMENT '로그인 패스워드',
  student_id   INT         NOT NULL COMMENT '학번',
  name         VARCHAR(50) NOT NULL COMMENT '이름',
  college      VARCHAR(50) NULL     COMMENT '단과대',
  major        VARCHAR(50) NOT NULL COMMENT '학과',
  grade        INT         NOT NULL COMMENT '학년',
  phone_number VARCHAR(20) NOT NULL COMMENT '전화번호',
  e_mail       VARCHAR(50) NOT NULL COMMENT '이메일',
  PRIMARY KEY (ID)
) COMMENT '사용자 목록';

ALTER TABLE Club_Reviews
  ADD CONSTRAINT FK_Clubs_TO_Club_Reviews
    FOREIGN KEY (club_name)
    REFERENCES Clubs (club_name) ON DELETE CASCADE;

ALTER TABLE Club_Reviews
  ADD CONSTRAINT FK_Users_TO_Club_Reviews
    FOREIGN KEY (ID)
    REFERENCES Users (ID);

ALTER TABLE Crews
  ADD CONSTRAINT FK_Users_TO_Crews
    FOREIGN KEY (ID)
    REFERENCES Users (ID) ON DELETE CASCADE;

ALTER TABLE New_club_Applicants
  ADD CONSTRAINT FK_Users_TO_New_club_Applicants
    FOREIGN KEY (ID)
    REFERENCES Users (ID) ON DELETE CASCADE;

ALTER TABLE Invitations
  ADD CONSTRAINT FK_Clubs_TO_Invitations
    FOREIGN KEY (club_name)
    REFERENCES Clubs (club_name) ON DELETE CASCADE;

ALTER TABLE Invitations
  ADD CONSTRAINT FK_Users_TO_Invitations
    FOREIGN KEY (ID)
    REFERENCES Users (ID) ON DELETE CASCADE;

ALTER TABLE Posts
  ADD CONSTRAINT FK_Clubs_TO_Posts
    FOREIGN KEY (club_name)
    REFERENCES Clubs (club_name) ON DELETE CASCADE;

ALTER TABLE Recruitings
  ADD CONSTRAINT FK_Posts_TO_Recruitings
    FOREIGN KEY (post_ID)
    REFERENCES Posts (post_ID) ON DELETE CASCADE;

ALTER TABLE Union_activities
  ADD CONSTRAINT FK_Posts_TO_Union_activities
    FOREIGN KEY (post_ID)
    REFERENCES Posts (post_ID) ON DELETE CASCADE;

ALTER TABLE Club_Activities
  ADD CONSTRAINT FK_Posts_TO_Club_Activities
    FOREIGN KEY (post_ID)
    REFERENCES Posts (post_ID) ON DELETE CASCADE;

ALTER TABLE New_club_Applicants
  ADD CONSTRAINT FK_New_clubs_TO_New_club_Applicants
    FOREIGN KEY (New_club_id) 
    REFERENCES New_clubs (new_club_id) ON DELETE CASCADE;

ALTER TABLE Club_fee_table
  ADD CONSTRAINT FK_Crews_TO_Club_fee_table
    FOREIGN KEY (club_name, ID)
    REFERENCES Crews (club_name, ID) ON DELETE CASCADE;

ALTER TABLE Crews
  ADD CONSTRAINT FK_Clubs_TO_Crews
    FOREIGN KEY (club_name)
    REFERENCES Clubs (club_name) ON DELETE CASCADE;

ALTER TABLE Applicants
  ADD CONSTRAINT FK_Users_TO_Applicants
    FOREIGN KEY (ID)
    REFERENCES Users (ID) ON DELETE CASCADE;

ALTER TABLE Applicants
  ADD CONSTRAINT FK_Posts_TO_Applicants
    FOREIGN KEY (post_ID) REFERENCES Posts (post_ID) ON DELETE CASCADE;

-- Club_Reviews 테이블에 대한 트리거 추가
DELIMITER //

CREATE TRIGGER update_club_rating_after_insert
AFTER INSERT ON Club_Reviews
FOR EACH ROW
BEGIN
    UPDATE Clubs
    SET rating = (
        SELECT AVG(score)
        FROM Club_Reviews
        WHERE club_name = NEW.club_name
    )
    WHERE club_name = NEW.club_name;
END//

CREATE TRIGGER update_club_rating_after_update
AFTER UPDATE ON Club_Reviews
FOR EACH ROW
BEGIN
    UPDATE Clubs
    SET rating = (
        SELECT AVG(score)
        FROM Club_Reviews
        WHERE club_name = NEW.club_name
    )
    WHERE club_name = NEW.club_name;
END//

CREATE TRIGGER update_club_rating_after_delete
AFTER DELETE ON Club_Reviews
FOR EACH ROW
BEGIN
    UPDATE Clubs
    SET rating = (
        SELECT COALESCE(AVG(score), 0)
        FROM Club_Reviews
        WHERE club_name = OLD.club_name
    )
    WHERE club_name = OLD.club_name;
END//

DELIMITER ;
