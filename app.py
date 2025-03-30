from flask import Flask, app
from flask_cors import CORS


from API.Login import Login_BP
from API.Crew import Crew_Bp

app = Flask(__name__)

CORS(app)


# API 요청 포인트 추가
app.register_blueprint(Login_BP, url_prefix="/login")
app.register_blueprint(Crew_Bp, url_prefix="/crew")



if __name__ == "__main__":
    app.run(host='127.0.0.1', port=3000, debug=True)
    
    
