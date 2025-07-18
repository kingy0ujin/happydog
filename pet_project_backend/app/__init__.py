# app/__init__.py

from flask import Flask, jsonify
from .core.config import Config

# Firebase Admin SDK
import firebase_admin
from firebase_admin import credentials, firestore

# Firestore 클라이언트를 다른 파일에서 쉽게 사용할 수 있도록 db 객체를 선언합니다.
db = None

def create_app():
    """
    Flask 앱 인스턴스를 생성하고 초기화하는 앱 팩토리 함수입니다.
    """
    global db

    # Flask 앱 생성
    app = Flask(__name__)

    # 1. 설정 파일 로드
    app.config.from_object(Config)
    
    # 2. 한글 JSON 깨짐 방지
    app.json.ensure_ascii = False

    # 3. Firebase 초기화
    try:
        cred_path = app.config['FIREBASE_CREDENTIALS_PATH']
        # 이미 초기화된 경우를 대비하여 예외 처리
        if not firebase_admin._apps:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            print("Firebase가 성공적으로 초기화되었습니다.")
        
        db = firestore.client()
    except Exception as e:
        print(f"Firebase 초기화 실패: {e}")

    # 4. 블루프린트 등록
    from .api.auth.routes import auth_bp
    from .api.pets.routes import pet_bp
    from .api.analysis.routes import analysis_bp
    from .api.survey.routes import survey_bp
    
    # API 경로에 접두사를 붙여서 등록합니다.
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(pet_bp, url_prefix='/api/pets')
    app.register_blueprint(analysis_bp, url_prefix='/api/analysis')
    app.register_blueprint(survey_bp, url_prefix='/api/survey')
    
    # 5. 기본 상태 확인용 라우트
    @app.route("/")
    def index():
        return jsonify({"status": "ok", "message": "Pet Project Backend is running!"})

    return app