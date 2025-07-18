Pet Project Backend: 팀 온보딩 가이드
시작하며
안녕하세요, 팀원 여러분. 이 문서는 우리 "Pet Project Backend"의 전체적인 설계와 폴더 구조를 설명하는 온보딩 가이드입니다. 협업이 처음이거나 앱 개발이 익숙하지 않은 분들도 이 문서 하나로 프로젝트의 전체 그림을 이해하고, 자신감 있게 개발에 참여하는 것을 목표로 합니다.

우리 프로젝트의 핵심 설계 원칙은 **'역할과 책임의 명확한 분리'**입니다. 사용자의 요청을 처리하는 app 폴더와 인공지능 모델을 담당하는 ml_models 폴더로 작업 영역을 나누었습니다. 이를 통해 특정 기능(예: API 개발 또는 모델 최적화)에 집중할 때 다른 영역의 코드에 미치는 영향을 최소화하고, 각자 독립적인 개발 흐름을 유지할 수 있도록 돕습니다.

1. 프로젝트 시작하기 (Getting Started)
새로운 팀원이 가장 먼저 수행해야 할 작업 순서입니다.

1. 프로젝트 복제 (Clone)
Git 저장소에서 프로젝트를 로컬 컴퓨터로 복제합니다.

2. 가상환경 생성
⚠️ 중요: environment.yml 파일 수정하기

environment.yml 파일은 팀원들의 개발 환경을 통일하기 위한 중요한 파일이지만, 생성한 사람의 개인 컴퓨터 경로가 기록되어 있을 수 있습니다.

conda env create 명령어를 실행하기 전, 반드시 environment.yml 파일을 텍스트 편집기로 열어 맨 아래에 있는 prefix: 로 시작하는 줄을 찾아 삭제해주세요.
```
name: pet_project_backend
channels:
  - defaults
dependencies:
  - python=3.9
  - flask
  - ... (기타 라이브러리)
prefix: C:\Users\jeongho\anaconda3\envs\pet_project_backend  # <-- 이 줄을 반드시 삭제!
```
이 prefix 줄을 삭제해야만, 각 팀원의 컴퓨터 환경에 맞는 올바른 경로에 가상환경이 성공적으로 설치됩니다.

이제 아래 명령어를 실행하여 Anaconda 가상환경을 생성합니다.
```
conda env create -f environment.yml
```
3. 가상환경 활성화
아래 명령어로 생성된 가상환경에 진입합니다.
```
conda activate pet_project_backend
```
4. .env 파일 설정
프로젝트 루트에 있는 .env.example 파일을 복사하여 .env 파일을 생성한 뒤, 내부의 값들을 자신의 개발 환경에 맞게 채워 넣습니다. 이 파일은 민감한 정보를 담고 있으므로 Git에 포함되지 않습니다.

5. 비밀 키 파일 배치
팀 리드로부터 전달받은 Firebase 서비스 계정 키(.json) 파일을 /secrets 폴더 안에 위치시킵니다.

6. 서버 실행
모든 설정이 완료되면, 아래 명령어로 개발용 애플리케이션 서버를 실행합니다.
```
python run.py
```
서버가 정상적으로 실행되면, 이제 코드 개발을 시작할 준비가 된 것입니다.

2. 프로젝트 폴더 구조
프로젝트의 전체 폴더 구조는 다음과 같으며, 실제 개발 현황을 정확하게 반영합니다.
```
/pet_project_backend/
|
|-- /app/                        # Flask 애플리케이션 코어
|   |-- /api/                    # 기능별 API 경로 (블루프린트)
|   |-- /core/                   # 공통 핵심 모듈 (설정, 보안)
|   |-- /models/                 # 데이터 구조 정의 (Firestore 문서)
|   |-- /schemas/                # 데이터 유효성 검증 (API 입국 심사관)
|   |-- /services/               # 여러 기능이 공유하는 공통 로직
|   `-- __init__.py              # ✨ 앱을 조립하는 총괄 공장장
|
|-- /ml_models/                  # 머신러닝 관련 코드
|   |-- /inference/              # 모델 추론 로직
|   |-- /saved_models/           # 학습된 모델 파일
|   `-- /scripts/                # 모델 학습 등 오프라인 스크립트
|
|-- /uploads/                    # 사용자 업로드 파일 임시 저장
|-- /secrets/                    # Firebase 키 등 비밀 파일
|
|-- run.py                       # 앱 서버 실행 스크립트
|-- .env                         # 환경변수
|-- .gitignore                   # Git 추적 제외 목록
|-- environment.yml              # Conda 환경 설정 파일
```

3. 프로젝트의 심장, app/__init__.py 파헤치기 (가장 중요한 파일!)
이 프로젝트의 구조를 이해하려면 app/__init__.py 파일의 역할을 아는 것이 가장 중요합니다. 이 파일이 없다면, 각 기능들은 뿔뿔이 흩어진 부품에 불과합니다. 이 파일은 **'앱 조립 공장의 총괄 공장장'**과 같습니다.

run.py가 python run.py 명령으로 실행될 때, 가장 먼저 이 공장장을 찾아 create_app()이라는 조립 라인을 가동시킵니다. 조립 과정은 다음과 같습니다.

1단계: 앱의 뼈대 만들기

app = Flask(__name__) 코드를 통해 비어있는 플라스크(Flask) 앱 객체를 생성합니다. 이는 마치 레고를 조립하기 위해 가장 먼저 텅 빈 레고 판을 꺼내는 것과 같습니다.

2단계: 설정 정보 주입하기 (설계도 읽기)

config.py 파일에서 데이터베이스 주소, 비밀 키 같은 중요한 설정 정보들을 읽어와 앱에 등록합니다. 이제 우리 앱은 어떤 데이터베이스에 연결하고, 어떻게 보안을 유지해야 할지 알게 됩니다. 레고 조립 설명서를 읽고, 어떤 부품이 필요한지 파악하는 단계입니다.

3단계: 기능별 부품(블루프린트) 등록하기

이 단계가 가장 중요합니다. 공장장은 app/api 폴더를 쭉 둘러보며 auth, pets 등 각 기능 폴더 안에 있는 routes.py(기능별 설계도)를 하나씩 가져옵니다.

그리고 app.register_blueprint() 명령으로 가져온 설계도들을 앱의 뼈대에 차곡차곡 연결하고, 각각의 주소(URL)를 부여합니다.

이 과정을 통해, 흩어져 있던 '로그인 기능', '펫 등록 기능'들이 비로소 http://서버주소/auth/login, http://서버주소/pets 와 같은 실제 주소를 갖는 하나의 완성된 서비스로 합쳐집니다.

4단계: 완성품 출하

모든 조립이 끝나면, 공장장은 완성된 앱(app)을 run.py에게 돌려줍니다. run.py는 이 완성품을 받아 서버를 가동시켜 손님(클라이언트)을 맞이할 준비를 마칩니다.

💡 왜 이렇게 복잡하게 '공장'처럼 만들까요?

코드 꼬임 방지: 만약 pets 기능과 auth 기능이 서로를 필요로 할 때, 직접 불러오려고 하면 "누가 먼저냐" 문제가 생겨 코드가 엉망이 됩니다. 하지만 공장장이 앱을 먼저 만들고 나중에 둘을 조립하면, 이런 문제가 깔끔하게 해결됩니다. 이를 **'순환 참조 방지'**라고 합니다.

4. /app 디렉토리 상세 분석: 애플리케이션의 심장부
/api (API 계층: 기능별 독립 부서)
외부 클라이언트의 모든 HTTP 요청을 기능별로 분리하여 처리하는 곳입니다. 각 기능 폴더는 하나의 독립적인 **'기능별 미니 앱(블루프린트)'**입니다.

블루프린트(Blueprint)란?

거대한 앱을 잘게 나눈 '기능 단위의 부품'입니다. '인사팀', '회계팀'처럼 각자 맡은 역할이 명확해서, 다른 팀에 신경 쓰지 않고 자신의 업무에만 집중할 수 있게 해줍니다.

서비스 계층의 이중 구조: 전담 요리사와 공용 창고
우리 프로젝트는 서비스 로직을 두 가지 형태로 관리하여 명확성과 재사용성을 모두 확보합니다.

app/api/*/services.py (기능별 전담 요리사)

오직 특정 기능 하나만을 위해 일하는 전문가입니다. pets/services.py는 '반려동물'과 관련된 요리(로직)만 담당합니다. 다른 기능에서는 이 요리사를 부르지 않습니다.

/app/services/ (공용 재료 창고)

모든 요리사가 함께 사용하는 재료 창고입니다. firebase_service.py는 Firestore 데이터베이스에 접근하는 방법을 제공하며, '사용자', '반려동물', '게시글' 등 모든 기능이 필요할 때마다 이 창고에서 재료(기능)를 가져다 씁니다.

/schemas (API 입국 심사관)
API로 데이터가 들어오고 나갈 때, 모든 관문을 지키는 **'입국 심사관'**입니다. 두 가지 중요한 임무를 수행합니다.

들어올 때 (요청 데이터 검증): "이 데이터, 우리 시스템에 들어올 자격(올바른 형식)이 되나요?" 라며 데이터의 형식을 꼼꼼히 검사합니다. 형식이 틀리면 입장을 거부하여 시스템을 보호합니다.

나갈 때 (응답 데이터 변환): "이 데이터, 외부 세계(클라이언트)가 이해할 수 있는 언어(JSON)로 번역되었나요?" 라며 우리 시스템의 데이터를 표준 언어인 JSON으로 깔끔하게 포장해서 내보냅니다.

5. /ml_models 디렉토리 상세 분석: 독립적인 AI 엔진
애플리케이션 서버(app)와 개발 관심사가 분리된 머신러닝 전용 공간입니다.

/scripts: 모델 학습, 데이터 전처리 등 오프라인에서 실행하는 연구/개발용 스크립트를 보관합니다. python run.py와는 별개로, AI 담당자가 필요할 때 직접 실행하는 파일들입니다.

6. 주요 기능 동작 원리 (쉬운 비유)
비문 분석 로직 (Faiss 활용) - 도서관 색인 카드
사전 준비 (오프라인): AI 담당자가 수많은 비문 데이터를 미리 분석해서, 어떤 비문이 어디에 있는지 알려주는 **'색인 카드(Index)'**를 만들어 둡니다. (책 전체를 읽지 않고 '찾아보기' 페이지만 만드는 것과 같습니다.)

사용자 요청 (온라인): 사용자가 비문 사진을 보내면, 서버는 그 사진의 특징을 찾습니다.

빠른 검색: 서버는 이 특징을 가지고 도서관 전체(모든 데이터)를 뒤지는 대신, 미리 만들어 둔 '색인 카드'만 보고 "이 특징과 가장 비슷한 비문은 3번 선반에 있습니다!" 라고 순식간에 결과를 찾아냅니다.

멍스타그램 '만화 생성' 로직 (비동기 처리) - 은행 대기 번호표
처리 시간이 긴 이 기능은 사용자를 하염없이 기다리게 하지 않습니다.

작업 요청 및 즉시 응답: 사용자가 만화 생성을 요청하면, 서버는 바로 만화를 만들지 않습니다. 대신 "네, 접수되었습니다. 고객님 대기번호는 7번입니다" 라는 **'대기 번호표(작업 ID)'**만 즉시 발급하고 응답을 마칩니다.

백그라운드 작업: 서버는 뒤에서 조용히 7번 고객의 업무(DALL-E API 호출, 이미지 생성)를 처리합니다. 사용자는 그동안 다른 기능을 자유롭게 이용할 수 있습니다.

결과 확인: 사용자의 앱은 잠시 후, "7번 고객님 업무 끝났나요?" 라고 서버에 물어봅니다. 작업이 완료되었다면, 완성된 이미지 주소를 전달하고 사용자는 만화를 볼 수 있습니다.










<h1>Pet Project Backend: Technical Onboarding (v2.0)</h1>
1. Preamble
본 문서는 "Pet Project Backend"의 시스템 아키텍처, 설계 원칙, 그리고 표준 개발 워크플로우를 정의하는 기술 온보딩 가이드입니다. 모든 팀원은 본 문서를 숙지하여 프로젝트의 기술적 컨텍스트를 이해하고, 일관된 코드 품질 및 개발 생산성을 유지해야 합니다.

본 프로젝트는 Flask 기반의 모놀리식(Monolithic) 아키텍처를 채택하되, 내부적으로는 계층화된 설계(Layered Architecture)와 모듈화를 통해 시스템의 각 컴포넌트가 높은 응집도와 낮은 결합도를 갖도록 설계되었습니다. 핵심 설계 철학은 **'관심사의 분리(Separation of Concerns)'**이며, 이는 애플리케이션 로직(app)과 머신러닝 로직(ml_models)의 물리적 분리에서 명확히 드러납니다.

2. Environment Setup & Configuration
로컬 개발 환경을 구성하기 위한 절차입니다.

2.1. Prerequisites
Git

Anaconda or Miniconda

2.2. Initial Setup
Clone Repository

git clone <repository_url>
cd pet_project_backend

Conda Environment Creation

[Critical] environment.yml의 prefix 필드는 환경 생성자의 로컬 경로를 포함하므로, 공유 시 충돌을 유발합니다. conda env create 실행 전, 파일 하단의 prefix: 라인을 반드시 삭제하십시오.
```
# 1. (If exists) Remove the 'prefix' line from environment.yml
# 2. Create the environment
conda env create -f environment.yml

Activate Environment

conda activate pet_project_backend
```
Configure Environment Variables
.env.example 파일을 복제하여 .env 파일을 생성하고, 로컬 환경에 맞게 변수들을 설정합니다. 이 파일은 Git에서 추적하지 않습니다(untracked).
```
cp .env.example .env
```
Place Service Account Key
팀 리드로부터 전달받은 Firebase Service Account Key(.json)를 secrets/ 디렉토리 내에 위치시킵니다. 이 디렉토리 역시 Git에서 추적하지 않습니다.

Launch Development Server
```
python run.py
```
서버가 0.0.0.0:5000에서 정상적으로 실행되면 초기 설정이 완료된 것입니다.

3. System Architecture
3.1. High-Level Overview
본 시스템은 두 개의 핵심 컴포넌트로 구성됩니다.

Application Core (app/): Flask 기반의 웹 애플리케이션으로, API 엔드포인트 제공, 비즈니스 로직 처리, 데이터 영속성 관리 등 핵심적인 백엔드 기능을 수행합니다.

ML Engine (ml_models/): 머신러닝 모델의 추론 및 관련 스크립트를 관리하는 독립된 파이썬 패키지입니다. Application Core에 의해 호출되지만, 반대 방향의 의존성은 존재하지 않아 ML 관련 코드의 독립적인 개발 및 테스트를 보장합니다.

3.2. Application Core (app/) Deep Dive
3.2.1. Request Lifecycle
클라이언트의 HTTP 요청은 다음과 같은 계층을 순차적으로 통과합니다.
Client -> WSGI Server -> Flask App -> Blueprint (routes.py) -> Service Layer -> Model/Schema Layer -> Database

3.2.2. Application Factory (app/__init__.py)
본 프로젝트는 애플리케이션 팩토리(Application Factory) 패턴을 사용합니다. create_app() 함수는 애플리케이션의 인스턴스화 및 초기 설정을 담당하는 유일한 진입점입니다.

목적:

순환 참조 방지 (Circular Import Prevention): 앱 객체를 먼저 생성하고, 이후에 블루프린트나 확장 기능들을 등록함으로써 모듈 간의 순환 참조 문제를 원천적으로 방지합니다.

동적 설정 주입 (Dynamic Configuration): 테스트, 개발, 운영 등 다양한 환경에 맞는 설정을 동적으로 주입하여 유연한 애플리케이션 인스턴스 생성을 가능하게 합니다.

의존성 관리: Flask 확장 기능(extensions)과 블루프린트를 체계적으로 등록하고 관리합니다.

3.2.3. Directory Structure & Responsibilities
```
/app
|-- /api/         # Presentation Layer: 기능 도메인별 Blueprint 관리
|-- /core/        # Core Logic: 인증, 설정 등 프로젝트 전반의 핵심 로직
|-- /models/      # Data Model Layer: 데이터베이스 스키마(구조) 정의
|-- /schemas/     # Data Transfer Object (DTO) & Validation Layer
|-- /services/    # Shared Infrastructure Service Layer
`-- __init__.py   # Application Factory
```
/api: 각 하위 디렉토리는 하나의 기능 도메인(e.g., pets, auth)을 나타내는 Blueprint입니다. routes.py는 해당 도메인의 API 엔드포인트와 HTTP 메서드를 정의합니다.

/services: 공유 인프라 서비스를 정의합니다. firebase_service.py와 같이 여러 도메인에서 공통으로 사용되는 저수준(low-level)의 비즈니스 로직이나 외부 서비스와의 연동을 담당합니다.

/api/{domain}/services.py: 도메인 특화 서비스를 정의합니다. 특정 도메인에 강하게 결합된 비즈니스 로직을 포함합니다. 예를 들어, pets/services.py는 반려동물 프로필 생성과 관련된 복잡한 비즈니스 규칙을 처리합니다.

/models: 데이터베이스 컬렉션과 필드를 클래스 형태로 정의합니다. 데이터의 영속적인 구조를 나타냅니다.

/schemas: API의 요청(Request)과 응답(Response) 데이터 구조를 정의하고 유효성을 검증하는 DTO(Data Transfer Object) 계층입니다. Marshmallow와 같은 라이브러리를 사용하여 데이터 직렬화(Serialization) 및 역직렬화(Deserialization)를 수행합니다.

4. Core Implementation Patterns
4.1. Asynchronous Task Processing
'만화 생성'과 같이 처리 시간이 긴(long-running) 작업은 사용자 경험(UX) 저하를 막기 위해 비동기적으로 처리됩니다.

Request & Task Queuing: 클라이언트가 작업을 요청하면, 서버는 즉시 요청을 백그라운드 작업 큐(e.g., Celery, RQ)에 등록하고, 추적 가능한 task_id를 즉시 반환합니다.

Background Execution: 별도의 Worker 프로세스가 큐에서 작업을 가져와 외부 API 호출, 이미지 생성 등의 무거운 로직을 수행합니다.

Polling & Result Retrieval: 클라이언트는 발급받은 task_id를 이용해 주기적으로(polling) 작업 상태를 확인하는 엔드포인트를 호출하고, 작업 완료 시 최종 결과(이미지 URL 등)를 수신합니다.

4.2. High-Performance Similarity Search (Faiss)
'비문 분석' 기능은 대규모 벡터 데이터셋에서 유사 벡터를 효율적으로 검색하기 위해 Faiss를 활용합니다.

Offline Indexing: ml_models/scripts/의 스크립트를 통해 사전에 등록된 모든 비문 이미지의 특징 벡터를 추출하고, 이를 검색에 최적화된 Faiss 인덱스 파일로 구축합니다.

In-Memory Search: 애플리케이션 서버는 시작 시 이 인덱스 파일을 메모리에 로드합니다.

Online Querying: 사용자 요청이 들어오면, 입력 이미지의 벡터를 추출한 뒤 전체 DB를 스캔하는 대신 메모리에 있는 인덱스에 질의(query)하여 k-NN(k-Nearest Neighbors) 탐색을 압도적으로 빠른 속도로 수행합니다.

5. Development Workflow
5.1. Git Branching Strategy
본 프로젝트는 Git Flow의 원칙을 따릅니다.

main: 배포 가능한 프로덕션 코드만 포함합니다.

develop: 다음 릴리즈를 위한 개발의 통합 브랜치입니다.

feature/{feature-name}: 신규 기능 개발을 위한 브랜치입니다. develop 브랜치에서 분기하며, 개발 완료 후 develop으로 Pull Request를 생성합니다.

5.2. Pull Request & Code Review
모든 코드는 develop 브랜치로 머지되기 전, 동료의 코드 리뷰를 거쳐야 합니다. PR은 최소 1명 이상의 승인(Approve)을 받아야 머지될 수 있습니다.

5.3. Dependency Management
새로운 라이브러리 추가 시, conda install <package_name>으로 설치 후 반드시 environment.yml 파일을 업데이트해야 합니다.
```
명령어: conda env export --no-builds > environment.yml
```