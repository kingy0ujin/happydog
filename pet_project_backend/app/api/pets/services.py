# app/api/pets/services.py

from firebase_admin import firestore
from datetime import datetime

# db 객체는 firebase_service에서 초기화된 것을 그대로 사용 가능
db = firestore.client()

def create_pet(user_id: str, pet_data: dict) -> str:
    # """
    # 새로운 반려동물 정보를 Firestore에 저장합니다.
    # :param user_id: 반려동물 주인의 user_id (우리 서비스의 내부 ID)
    # :param pet_data: 유효성 검사를 통과한 반려동물 데이터
    # :return: 생성된 반려동물 문서의 ID
    # """
    pets_ref = db.collection('pets')
    
    # 데이터에 주인 ID와 생성 시간을 추가
    pet_document = pet_data.copy()
    pet_document['owner_id'] = user_id
    pet_document['created_at'] = firestore.SERVER_TIMESTAMP
    
    # 생년월일이 date 객체일 경우, Firestore 저장을 위해 문자열로 변환
    if isinstance(pet_document.get('birth_date'), datetime):
        pet_document['birth_date'] = pet_document['birth_date'].strftime('%Y-%m-%d')

    # Firestore에 새 반려동물 문서를 추가
    update_time, new_pet_ref = pets_ref.add(pet_document)
    
    return new_pet_ref.id


# create_pet 함수는 주인의 user_id와 유효성 검사를 마친 반려동물 데이터를 받습니다.

# 데이터에 owner_id를 추가하여 어떤 사용자의 반려동물인지 명확히 연결합니다. 이것은 나중에 "내 반려동물 목록 조회" 같은 기능을 구현할 때 필수적입니다.

# pets 컬렉션에 문서를 추가하고, 생성된 문서의 고유 ID를 반환합니다.