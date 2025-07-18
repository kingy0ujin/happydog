# app/core/security.py

import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify, g
from app.core.config import settings

ALGORITHM = "HS256"

def create_access_token(data: dict) -> str:
    # """
    # Access Token을 생성합니다. (유효기간 15분)
    # :param data: 토큰에 담을 데이터 (payload)
    # :return: 인코딩된 Access Token 문자열
    # """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    # """
    # Refresh Token을 생성합니다. (유효기간 7일)
    # :param data: 토큰에 담을 데이터 (payload)
    # :return: 인코딩된 Refresh Token 문자열
    # """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def jwt_required(f):
    # """
    # JWT 토큰이 유효한지 검증하는 데코레이터.
    # 유효한 경우, g.user에 페이로드를 저장하여 라우트 함수에서 사용할 수 있게 합니다.
    # """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"error": "Authorization header is missing"}), 401

        parts = auth_header.split()

        if parts[0].lower() != "bearer" or len(parts) != 2:
            return jsonify({"error": "Invalid Authorization header format"}), 401
        
        token = parts[1]

        try:
            payload = jwt.decode(
                token, 
                settings.JWT_SECRET_KEY, 
                algorithms=[ALGORITHM],
                options={"require": ["exp"]} # 'exp' 클레임이 반드시 존재해야 함
            )
            # g 객체에 유저 정보를 저장합니다.
            g.user = payload
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        
        return f(*args, **kwargs)

    return decorated_function


# create_access_token / create_refresh_token: PyJWT 라이브러리를 사용하여 JWT를 생성합니다.
# exp (만료 시간) 클레임을 설정하여 토큰의 유효 기간을 지정합니다. 시간은 UTC 기준으로 처리하는 것이 안전합니다.

# @jwt_required:

# functools.wraps를 사용하여 원본 함수의 메타데이터(__name__, __doc__ 등)를 유지합니다.

# request.headers.get("Authorization")를 통해 Authorization 헤더를 가져옵니다.

# Bearer <token> 형식이 맞는지 확인하고 토큰을 추출합니다.

# jwt.decode를 사용하여 토큰을 검증합니다. 시크릿 키, 알고리즘이 일치해야 하며 만료되지 않아야 합니다.

# 검증에 성공하면, 토큰의 페이로드(사용자 정보)를 flask.g 객체에 저장합니다. g는 단일 요청 내에서 데이터를 공유하기 위한 Flask의 전역 객체입니다.

# 실패 시 적절한 401 Unauthorized 에러 메시지를 반환합니다.


