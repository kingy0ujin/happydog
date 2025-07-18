# app/schemas/pet_schema.py

from pydantic import BaseModel, constr, Field
from datetime import date
from typing import Literal

class PetCreateSchema(BaseModel):
    # """반려동물 등록 요청을 위한 유효성 검사 스키마"""
    name: str = Field(..., min_length=1, max_length=50, description="반려동물 이름")
    breed: str = Field(..., min_length=1, max_length=50, description="품종")
    # YYYY-MM-DD 형식의 날짜 문자열을 받아서 date 객체로 변환합니다.
    birth_date: date = Field(..., description="생년월일 (YYYY-MM-DD)")
    gender: Literal['Male', 'Female', 'Unknown'] = Field(..., description="성별")
    
    class Config:
        # Pydantic 모델을 dict 뿐만 아니라 ORM 객체 등에서도 사용할 수 있게 함
        orm_mode = True
        
        
# pydantic.BaseModel을 상속받아 스키마 클래스를 만듭니다.

# 타입 힌트(str, date)를 사용하여 각 필드의 타입을 지정합니다. Pydantic이 자동으로 해당 타입으로 변환하거나 유효성을 검사합니다.

# Field를 사용하면 최소/최대 길이, 설명 등 더 상세한 유효성 검사 규칙을 추가할 수 있습니다.

# Literal 타입을 사용해 gender 필드가 정해진 값('Male', 'Female', 'Unknown') 중 하나만 갖도록 제한합니다.