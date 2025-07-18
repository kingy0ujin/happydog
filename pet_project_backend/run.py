from app import create_app

# 앱 팩토리로부터 Flask 앱 객체를 생성합니다.
app = create_app()

if __name__ == "__main__":
    # 이 스크립트가 직접 실행될 때만 개발 서버를 가동합니다.
    # host='0.0.0.0'은 외부 네트워크에서도 서버에 접속할 수 있게 합니다.
    # debug=True는 코드 변경 시 자동으로 서버를 재시작하고, 오류 발생 시 디버깅 정보를 보여줍니다.
    app.run(host='0.0.0.0', port=5000, debug=True)