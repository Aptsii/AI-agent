# Coding Expert AI Agent

이 프로젝트는 개발 관련 질문에 답변하기 위해 실시간 웹 검색을 수행하는 AI 에이전트입니다. LangGraph와 Google Gemini를 기반으로 하며, FastAPI를 통해 웹 API로 제공됩니다.

## 주요 기능

- **실시간 웹 검색**: DuckDuckGo Search를 사용하여 최신 정보를 바탕으로 답변합니다.
- **다양한 주제 처리**: 프로그래밍 언어, 기업 기술 스택 등 다양한 코딩 관련 질문에 답변할 수 있습니다.
- **API 기반 제공**: FastAPI를 사용하여 웹사이트나 다른 애플리케이션에 쉽게 통합할 수 있습니다.

---

## 🚀 시작하기

### 1. 사전 요구사항

- [Python 3.10 이상](https://www.python.org/)
- `uv`: 초고속 파이썬 패키지 설치 도구. 만약 설치되어 있지 않다면, 아래 명령어로 설치하세요.
  ```bash
  pip install uv
  ```

### 2. 프로젝트 설정

1.  **저장소 복제 및 이동**:

    ```bash
    # (이 프로젝트는 이미 복제되어 있다고 가정합니다.)
    cd copy/coding-expert-agent
    ```

2.  **의존성 설치**: `uv`를 사용하여 필요한 모든 라이브러리를 설치합니다.

    ```bash
    uv sync
    ```

3.  **환경 변수 설정**: 프로젝트 루트(`copy/coding-expert-agent`)에 `.env` 파일을 생성하고, Google AI Studio에서 발급받은 API 키를 입력하세요.
    ```
    # .env 파일 내용
    GOOGLE_API_KEY="여기에_본인의_Google_API_키를_입력하세요"
    ```
    > 🔑 **API 키 발급**: [Google AI Studio](https://aistudio.google.com/app/apikey)에서 무료로 키를 발급받을 수 있습니다.

---

## 🖥️ API 서버 실행

아래 명령어를 프로젝트 루트(`copy/coding-expert-agent`)에서 실행하여 API 서버를 시작합니다.

```bash
uv run uvicorn coding_expert_agent.api:app --app-dir src --reload
```

- `--app-dir src`: uvicorn에게 앱 코드가 `src` 디렉토리에 있다고 알려줍니다.
- `--reload`: 코드가 변경될 때마다 서버를 자동으로 재시작하여 개발에 편리합니다.
- 서버가 성공적으로 실행되면, 터미널에 `http://127.0.0.1:8000` 주소에서 실행 중이라는 메시지가 나타납니다.

---

## 🛠️ API 사용법

API 서버가 실행되면, 웹 브라우저나 API 테스트 도구(예: Postman, curl)를 사용하여 AI 에이전트와 상호작용할 수 있습니다.

### 자동 생성된 API 문서

웹 브라우저에서 아래 주소로 접속하면, FastAPI가 자동으로 생성해주는 API 문서를 확인할 수 있습니다. 이 페이지에서 직접 API를 테스트해볼 수도 있습니다.

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### `curl`을 이용한 예제

터미널에서 `curl` 명령어를 사용하여 API를 호출하는 예제입니다.

```bash
curl -X POST "http://127.0.0.1:8000/ask" \
-H "Content-Type: application/json" \
-d '{"question": "React와 Vue의 차이점은 뭐야?"}'
```

#### 예상 응답

요청이 성공하면, 아래와 같은 JSON 형식의 응답을 받게 됩니다.

```json
{
  "answer": "React와 Vue는 모두 인기 있는 자바스크립트 라이브러리/프레임워크이지만 몇 가지 주요 차이점이 있습니다.\n\n**React:**\n* **라이브러리:** React는 UI를 만들기 위한 라이브러리에 가깝습니다. 라우팅이나 상태 관리 등을 위해 다른 라이브러리(React Router, Redux 등)와 조합하여 사용하는 경우가 많습니다.\n* **JSX:** JavaScript XML(JSX)이라는 문법을 사용하여 HTML 구조를 JavaScript 코드 내에서 직접 작성합니다.\n* **가상 DOM:** 변경 사항을 가상 DOM에 먼저 적용하여 실제 DOM과의 차이점을 계산하고, 변경된 부분만 효율적으로 업데이트합니다.\n\n**Vue:**\n* **프레임워크:** Vue는 프레임워크에 더 가깝습니다. 라우팅, 상태 관리 등을 위한 공식 라이브러리를 기본적으로 제공하여 더 통합된 개발 경험을 제공합니다.\n* **템플릿 문법:** 일반적인 HTML 파일과 유사한 템플릿 문법을 사용하여 코드를 더 쉽게 이해하고 작성할 수 있습니다.\n* **점진적 적용:** 기존 프로젝트에 점진적으로 도입하기 쉽게 설계되었습니다."
}
```

이제 이 API를 당신의 웹사이트 프론트엔드와 연동하여 AI 기능을 통합할 수 있습니다.

---

## 📖 배포 가이드

이 AI 에이전트를 클라우드에 배포하고 실제 웹사이트에 적용하는 방법에 대한 전체 가이드를 별도의 문서로 상세히 작성해두었습니다.

➡️ **[전체 배포 가이드 읽기 (DEPLOYMENT.md)](./DEPLOYMENT.md)**
