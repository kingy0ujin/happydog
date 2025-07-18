# app/api/auth/routes.py

from flask import Blueprint, request, jsonify
# from google.oauth2 import id_token # 실제 구현 시 구글 토큰 검증 라이브러리
# from google.auth.transport import requests as google_requests
from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token
from app.services import firebase_service

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/social', methods=['POST'])
def social_login():
    # """
    # 구글 로그인을 처리하고 서비스 JWT를 발급합니다.
    # 클라이언트는 구글로부터 받은 ID Token을 요청 바디에 담아 보냅니다.
    # """
    data = request.get_json()
    google_id_token = data.get('token')

    if not google_id_token:
        return jsonify({"error": "Google ID token is required"}), 400

    # --- 실제 프로덕션에서는 이 부분에 구글 토큰 검증 로직이 들어갑니다 ---
    # try:
    #     id_info = id_token.verify_oauth2_token(
    #         google_id_token, google_requests.Request(), settings.GOOGLE_CLIENT_ID)
    #     user_info = id_info
    # except ValueError:
    #     return jsonify({"error": "Invalid Google token"}), 401
    # -----------------------------------------------------------------
    
    # [개발용] 현재는 구글 검증을 생략하고, 전달된 정보를 그대로 사용한다고 가정합니다.
    # 실제로는 위 주석처럼 반드시 검증해야 합니다.
    # 클라이언트에서 이미 검증 후 user_info를 보내준다고 가정.
    user_info_from_google = data.get('userInfo')
    if not user_info_from_google:
        return jsonify({"error": "User info is required for this mock setup"}), 400

    # Firebase에서 사용자 조회 또는 생성
    user_profile = firebase_service.get_or_create_user_by_social(user_info_from_google)

    if not user_profile or 'user_id' not in user_profile:
        return jsonify({"error": "Failed to get or create user"}), 500

    # 우리 서비스의 JWT를 생성하기 위한 페이로드
    jwt_payload = {
        'user_id': user_profile['user_id'],
        'email': user_profile['email']
    }

    # Access Token, Refresh Token 생성
    access_token = create_access_token(data=jwt_payload)
    refresh_token = create_refresh_token(data=jwt_payload)

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }), 200
    
    
# Blueprint를 사용하여 이 파일의 라우트들을 그룹화하고, url_prefix를 설정합니다.

# 구글 토큰 검증 (중요!): 실제 서비스에서는 클라이언트가 보낸 구글 ID 토큰을 서버에서 반드시 검증해야 합니다. 
# 주석 처리된 부분이 그 예시입니다. 지금은 요청에 userInfo가 포함되어 온다고 가정하고 진행합니다.

# firebase_service의 함수를 호출하여 우리 DB에서 사용자 정보를 가져옵니다.

# 가져온 사용자의 고유 user_id를 페이로드에 담아 create_access_token과 create_refresh_token을 호출합니다.

# 생성된 두 토큰을 클라이언트에게 JSON 형태로 반환합니다