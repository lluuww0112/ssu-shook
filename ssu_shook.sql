CREATE DATABASE IF NOT EXISTS ssu_shook
CHARACTER SET utf8mb4
COLLATE utf8mb4_general_ci;

USE ssu_shook;


CREATE TABLE Club_Activities
(
  Activity_ID    VARCHAR(50)   NOT NULL COMMENT '활동내역 아이디',
  club_name      VARCHAR(50)   NOT NULL COMMENT '동아리 명',
  activity_title VARCHAR(100)  NOT NULL COMMENT '활동 제목',
  activity_day   DATE          NOT NULL COMMENT '활동일',
  activity       VARCHAR(1000) NOT NULL COMMENT '활동 내용',
  activity_image VARCHAR(100)  NULL     COMMENT '활동 사진 경로',
  added          DATE          NOT NULL COMMENT '작성일',
  updated        DATE          NULL     COMMENT '수정일',
  PRIMARY KEY (Activity_ID)
) COMMENT '동아리 활동 내역';

CREATE TABLE Club_fee_table
(
  club_name   VARCHAR(50) NOT NULL COMMENT '동아리 명',
  ID          VARCHAR(50) NOT NULL COMMENT '로그인 아이디',
  publication DATE        NOT NULL COMMENT '발행일',
  fee         INT         NOT NULL COMMENT '청구 비용',
  payment     INT         NOT NULL DEFAULT 0 COMMENT '납부 여부'
) COMMENT '회비납부 관리 테이블';

CREATE TABLE Club_Reviews
(
  Review_ID VARCHAR(50)  NOT NULL COMMENT '리뷰 아이디',
  ID        VARCHAR(50)  NOT NULL COMMENT '로그인 아이디',
  club_name VARCHAR(50)  NOT NULL COMMENT '동아리 명',
  score     INT          NOT NULL COMMENT '별점',
  review    VARCHAR(300) NOT NULL COMMENT '리뷰 내용',
  added     DATE         NOT NULL COMMENT '작성일',
  updated   DATE         NULL     COMMENT '수정일',
  PRIMARY KEY (Review_ID)
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

CREATE TABLE Inviters
(
  club_name VARCHAR(50) NOT NULL COMMENT '동아리 명',
  ID        VARCHAR(50) NOT NULL COMMENT '로그인 아이디'
) COMMENT '동아리 초대자 목록';

CREATE TABLE New_club_Applicants
(
  New_club_id VARCHAR(50) NOT NULL COMMENT '신규 동아리 개설 모집 아이디',
  ID          VARCHAR(50) NOT NULL COMMENT '로그인 아이디'
) COMMENT '신규 동아리 임원진 신청자 리스틑';

CREATE TABLE New_clubs
(
  New_club_id           VARCHAR(50)   NOT NULL COMMENT '신규 동아리 개설 모집 아이디',
  new_club_name         VARCHAR(50)   NOT NULL COMMENT '신규 동아리 명',
  new_club_introduction VARCHAR(1000) NOT NULL COMMENT '신규 동아리 임원진 모집 요강',
  new_club_applicants   INT           NOT NULL DEFAULT 0 COMMENT '지원자 수',
  PRIMARY KEY (New_club_id)
) COMMENT '신규 동아리 임원진 모집 공고';

CREATE TABLE New_clubs_Ripples
(
  New_club_id VARCHAR(50)  NOT NULL COMMENT '신규 동아리 개설 모집 아이디',
  ID          VARCHAR(50)  NOT NULL COMMENT '로그인 아이디',
  ripple      VARCHAR(300) NOT NULL COMMENT '댓글',
  added       DATE         NOT NULL COMMENT '작성일',
  updated     DATE         NULL     COMMENT '수정일'
) COMMENT '신규 동아리 임원진 모집공고 댓글';

CREATE TABLE Recruiting
(
  Recruiting_id VARCHAR(50) NOT NULL COMMENT '리크루팅 아이디',
  club_name     VARCHAR(50) NOT NULL COMMENT '동아리 명',
  capacity      INT         NOT NULL COMMENT '모집인원',
  applicants    INT         NOT NULL DEFAULT 0 COMMENT '신청자수',
  start_date    DATE        NOT NULL COMMENT '모집 시작일',
  end_date      DATE        NOT NULL COMMENT '모집 종료일',
  added         DATE        NOT NULL COMMENT '작성일',
  updated       DATE        NULL     COMMENT '수정일',
  PRIMARY KEY (Recruiting_id)
) COMMENT '부원 모집 게시글';

CREATE TABLE Recruiting_Applicants
(
  Recruiting_id VARCHAR(50) NOT NULL COMMENT '리크루팅 아이디',
  ID            VARCHAR(50) NOT NULL COMMENT '로그인 아이디'
) COMMENT '부원 모집 신청자 목록';

CREATE TABLE Union_activities
(
  Union_activity_id VARCHAR(50)   NOT NULL COMMENT '연합활동 아이디',
  club_name         VARCHAR(50)   NOT NULL COMMENT '작성 동아리',
  union_title       VARCHAR(100)  NOT NULL COMMENT '연합활동 이름',
  union_activity    VARCHAR(1000) NULL     COMMENT '연합활동 설명',
  start_date        DATE          NOT NULL COMMENT '모집 시작일',
  end_date          DATE          NOT NULL COMMENT '모집 종료일',
  added             DATE          NOT NULL COMMENT '작성일',
  updated           DATE          NULL     COMMENT '수정일',
  applicants_club   INT           NOT NULL DEFAULT 0 COMMENT '참여희망 동아리 수',
  PRIMARY KEY (Union_activity_id)
) COMMENT '연합활동 모집 게시글';

CREATE TABLE Union_Applicants
(
  Union_activity_id VARCHAR(50) NOT NULL COMMENT '연합활동 아이디',
  club_name         VARCHAR(50) NOT NULL COMMENT '동아리 명'
) COMMENT '연합활동 신청 동아리 목록';

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

ALTER TABLE Club_Activities
  ADD CONSTRAINT FK_Clubs_TO_Club_Activities
    FOREIGN KEY (club_name)
    REFERENCES Clubs (club_name);

ALTER TABLE Club_fee_table
  ADD CONSTRAINT FK_Crews_TO_Club_fee_table
    FOREIGN KEY (club_name, ID)
    REFERENCES Crews (club_name, ID);

ALTER TABLE Club_Reviews
  ADD CONSTRAINT FK_Clubs_TO_Club_Reviews
    FOREIGN KEY (club_name)
    REFERENCES Clubs (club_name);

ALTER TABLE Club_Reviews
  ADD CONSTRAINT FK_Users_TO_Club_Reviews
    FOREIGN KEY (ID)
    REFERENCES Users (ID);

ALTER TABLE Crews
  ADD CONSTRAINT FK_Users_TO_Crews
    FOREIGN KEY (ID)
    REFERENCES Users (ID);

ALTER TABLE Crews
  ADD CONSTRAINT FK_Clubs_TO_Crews
    FOREIGN KEY (club_name)
    REFERENCES Clubs (club_name);

ALTER TABLE New_club_Applicants
  ADD CONSTRAINT FK_New_clubs_TO_New_club_Applicants
    FOREIGN KEY (New_club_id)
    REFERENCES New_clubs (New_club_id);

ALTER TABLE New_club_Applicants
  ADD CONSTRAINT FK_Users_TO_New_club_Applicants
    FOREIGN KEY (ID)
    REFERENCES Users (ID);

ALTER TABLE New_clubs_Ripples
  ADD CONSTRAINT FK_New_clubs_TO_New_clubs_Ripples
    FOREIGN KEY (New_club_id)
    REFERENCES New_clubs (New_club_id);

ALTER TABLE New_clubs_Ripples
  ADD CONSTRAINT FK_Users_TO_New_clubs_Ripples
    FOREIGN KEY (ID)
    REFERENCES Users (ID);

ALTER TABLE Recruiting
  ADD CONSTRAINT FK_Clubs_TO_Recruiting
    FOREIGN KEY (club_name)
    REFERENCES Clubs (club_name);

ALTER TABLE Recruiting_Applicants
  ADD CONSTRAINT FK_Recruiting_TO_Recruiting_Applicants
    FOREIGN KEY (Recruiting_id)
    REFERENCES Recruiting (Recruiting_id);

ALTER TABLE Recruiting_Applicants
  ADD CONSTRAINT FK_Users_TO_Recruiting_Applicants
    FOREIGN KEY (ID)
    REFERENCES Users (ID);

ALTER TABLE Union_activities
  ADD CONSTRAINT FK_Clubs_TO_Union_activities
    FOREIGN KEY (club_name)
    REFERENCES Clubs (club_name);

ALTER TABLE Union_Applicants
  ADD CONSTRAINT FK_Union_activities_TO_Union_Applicants
    FOREIGN KEY (Union_activity_id)
    REFERENCES Union_activities (Union_activity_id);

ALTER TABLE Union_Applicants
  ADD CONSTRAINT FK_Clubs_TO_Union_Applicants
    FOREIGN KEY (club_name)
    REFERENCES Clubs (club_name);

ALTER TABLE Inviters
  ADD CONSTRAINT FK_Clubs_TO_Inviters
    FOREIGN KEY (club_name)
    REFERENCES Clubs (club_name);

ALTER TABLE Inviters
  ADD CONSTRAINT FK_Users_TO_Inviters
    FOREIGN KEY (ID)
    REFERENCES Users (ID);

CREATE UNIQUE INDEX ID
  ON Crews (ID ASC);
