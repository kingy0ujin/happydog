# app/core/config.py

import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()

class Config:
    # """애플리케이션 환경 설정 값을 담고 있는 클래스"""
    # Flask 설정
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')

    # Firebase 설정
    FIREBASE_CREDENTIALS_PATH = os.getenv('FIREBASE_CREDENTIALS_PATH')

    # JWT 설정
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    ACCESS_TOKEN_EXPIRE_MINUTES = 15
    REFRESH_TOKEN_EXPIRE_DAYS = 7

    # Google Social Login 설정
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')

# 인스턴스화하여 다른 모듈에서 쉽게 가져다 쓸 수 있도록 합니다.
settings = Config()


# python-dotenv 라이브러리의 load_dotenv()를 사용해 .env 파일의 변수들을 환경 변수로 로드합니다.

# Config 클래스는 os.getenv()를 사용해 각 설정 값을 클래스 변수로 할당합니다.

# settings라는 인스턴스를 만들어, 다른 파일에서 from app.core.config import settings와 같이 쉽게 설정 값에 접근할 수 있도록 합니다.