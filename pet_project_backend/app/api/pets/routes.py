# app/api/pets/routes.py

from flask import Blueprint, request, jsonify, g
from pydantic import ValidationError
from app.core.security import jwt_required
from app.schemas.pet_schema import PetCreateSchema
from app.api.pets import services as pet_services

pet_bp = Blueprint('pets', __name__)

@pet_bp.route('/', methods=['POST'])
@jwt_required
def register_pet():
    # """
    # 로그인한 사용자의 반려동물을 등록합니다.
    # """
    try:
        # 1. 요청 본문(JSON)을 Pydantic 스키마로 유효성 검사
        request_data = request.get_json()
        validated_data = PetCreateSchema(**request_data)
    except ValidationError as e:
        # 유효성 검사 실패 시 400 Bad Request 에러 반환
        return jsonify({"error": e.errors()}), 400
    except Exception:
        return jsonify({"error": "Invalid request data"}), 400
        
    # 2. @jwt_required 데코레이터가 g.user에 저장한 페이로드에서 user_id 추출
    user_id = g.user.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID not found in token"}), 401
    
    try:
        # 3. 서비스 함수를 호출하여 반려동물 생성
        # Pydantic 모델을 딕셔너리로 변환하여 전달
        pet_id = pet_services.create_pet(user_id=user_id, pet_data=validated_data.model_dump())
        
        # 4. 성공 응답 반환
        return jsonify({
            "message": "Pet registered successfully!",
            "pet_id": pet_id
        }), 201 # 201 Created 상태 코드 사용
    except Exception as e:
        # 로깅을 추가하면 더 좋습니다.
        # print(f"Error creating pet: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500