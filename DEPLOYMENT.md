# AI 에이전트 배포 및 웹사이트 적용 가이드

이 문서는 로컬에서 실행되는 AI 에이전트 서버를 클라우드에 배포하고, 실제 운영 중인 웹사이트에 적용하는 전체 과정을 안내합니다.

---

## 📚 1부: 개념 이해하기 - Docker란 무엇인가?

배포를 하려면 먼저 Docker에 대해 알아야 합니다. Docker는 배포 과정을 아주 간단하게 만들어주는 핵심 기술입니다.

### Docker, 왜 필요한가요?

- **문제점**: "제 컴퓨터에서는 잘 되는데, 왜 서버 컴퓨터에서는 오류가 나죠?"
- **원인**: 내 컴퓨터와 서버 컴퓨터는 설치된 프로그램 버전, 설정 등 환경이 미세하게 다르기 때문입니다.
- **Docker의 해결책**: 우리 AI 서버 코드, 설치된 라이브러리들(`fastapi`, `langchain` 등), 심지어 파이썬 프로그램 자체를 **하나의 "소프트웨어 컨테이너"에 통째로 담아 포장**합니다.

이 "컨테이너"는 어디로 옮기든 내용물이 변하지 않는 완벽한 이삿짐 박스와 같습니다. 따라서 내 컴퓨터에서 이 박스를 만들어 클라우드 서버로 옮기면, 환경이 달라서 생기는 오류가 절대 발생하지 않습니다.

### `Dockerfile` 상세 분석

`Dockerfile`은 이 "이삿짐 박스"를 어떻게 만들지 적어놓은 **상세한 포장 설명서**입니다. Render 같은 클라우드 서비스는 이 설명서를 보고 그대로 따라서 우리를 위한 서버를 만들어줍니다.

아래는 우리가 만든 `Dockerfile`의 각 줄이 어떤 의미인지 설명한 것입니다.

```dockerfile
# 1. 기반 이미지 설정 ("어떤 종류의 컴퓨터를 준비할까?")
# 파이썬 3.11 버전이 미리 설치된, 가볍고 깨끗한 리눅스 컴퓨터를 준비합니다.
FROM python:3.11-slim

# 2. 작업 디렉토리 설정 ("어디에 짐을 풀까?")
# 이 컴퓨터 안에 앞으로 작업할 기본 폴더를 '/app'이라는 이름으로 만듭니다.
WORKDIR /app

# 3. 환경 설정 (컴퓨터 최적화)
# 불필요한 파일 생성을 막고, 프로그램 출력이 바로바로 보이도록 설정합니다.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 4. uv 설치 ("가장 빠른 설치 도구 준비")
# 파이썬 라이브러리들을 설치하기 위해, 'uv'라는 아주 빠른 설치 프로그램을 먼저 설치합니다.
RUN pip install uv

# 5. 의존성 파일 복사 및 설치 ("설치 설명서대로 부품 조립")
# 먼저 라이브러리 목록이 적힌 '설치 설명서'(pyproject.toml, uv.lock)를 컴퓨터로 복사합니다.
COPY pyproject.toml uv.lock ./
# 'uv'를 이용해 설명서에 적힌 모든 라이브러리를 컴퓨터에 설치합니다.
RUN uv sync --system

# 6. 소스 코드 복사 ("우리 프로그램 옮기기")
# 이제 우리의 실제 AI 에이전트 소스 코드(src 폴더 전체)를 컴퓨터로 복사합니다.
COPY src ./src

# 7. 서버 실행 ("마지막으로 서버 켜기")
# 모든 준비가 끝났으니, 이 컴퓨터가 켜지면 자동으로 이 명령어를 실행해서 AI 서버를 시작합니다.
# --host 0.0.0.0 : 컴퓨터의 어떤 주소로든 접속을 허용합니다. (공개 접속용)
# --port $PORT : 클라우드 서비스(Render)가 지정해주는 포트 번호를 사용합니다.
CMD ["uvicorn", "coding_expert_agent.api:app", "--host", "0.0.0.0", "--port", "$PORT"]
```

> **결론:** 이 `Dockerfile` 덕분에, 우리는 Render.com에 "이 설명서대로 서버 하나 만들어줘!" 라고 말하기만 하면 됩니다. 복잡한 서버 설정은 Render와 Docker가 알아서 전부 처리해줍니다.

---

## 🚀 2부: AI 서버 배포하기 (Render.com 기준)

이제 Docker로 우리 AI 서버를 어떻게 포장하는지 이해했으니, 실제로 클라우드에 배포해 보겠습니다.

### 1단계: 배포 준비 (GitHub)

1.  **GitHub 저장소 생성**: 이 프로젝트 코드(Dockerfile 포함)를 본인의 GitHub 계정에 새로운 저장소(Repository)로 만들어 `push` 해두어야 합니다.
2.  **`.gitignore` 확인**: `.env` 파일은 절대 GitHub에 올리면 안 됩니다.

### 2단계: Render.com에서 배포 실행하기

1.  **Render 가입 및 대시보드 이동**: [Render.com](https://render.com/)에 GitHub 계정으로 가입하고 로그인합니다.
2.  **새로운 웹 서비스 생성**:
    - **[New +]** > **[Web Service]**를 선택합니다.
    - 준비한 GitHub 저장소를 찾아 **[Connect]** 버튼을 누릅니다.
3.  **배포 설정하기**:
    - **Name**: 서비스 이름을 정합니다. (예: `my-coding-agent`)
    - **Runtime**: **`Docker`**를 선택합니다. (Render가 `Dockerfile`을 보고 자동으로 추천)
    - **Free Plan**: **`Free`** 플랜을 선택합니다.
4.  **환경 변수 설정 (가장 중요!)**:
    - **[Advanced]** 섹션을 열고 **[Add Environment Variable]** 버튼을 클릭합니다.
    - **Key**: `GOOGLE_API_KEY`
    - **Value**: 본인의 **Google Gemini API 키**
5.  **배포 시작**:
    - **[Create Web Service]** 버튼을 누릅니다.
    - 배포가 완료되면, 페이지 상단에 `https://my-coding-agent.onrender.com` 과 같은 공개 주소가 생성됩니다.

---

## 🌐 3부: 웹사이트에 적용하기

배포가 완료되어 얻은 공개 주소를 실제 웹사이트의 JavaScript 코드에 적용하는 방법입니다.

### JavaScript `fetch` 코드 수정

웹사이트에서 AI 서버를 호출하는 부분의 주소만 **Render에서 받은 공개 주소**로 변경하면 됩니다.

- **수정 전 (로컬)**: `fetch('http://127.0.0.1:8000/ask', ...)`
- **수정 후 (배포)**: `fetch('https://my-coding-agent.onrender.com/ask', ...)`

### 전체 예제 (`index.html`)

(이전과 동일한 예제 코드...)

```html
<!DOCTYPE html>
<html lang="ko">
  <head>
    <title>AI 에이전트 연동 예제</title>
  </head>
  <body>
    <h1>AI 에이전트에게 질문하기</h1>
    <input
      type="text"
      id="question-input"
      placeholder="여기에 질문을 입력하세요..."
    />
    <button id="ask-button" onclick="askAI()">질문 보내기</button>
    <h2>AI 답변:</h2>
    <div
      id="answer-box"
      style="white-space: pre-wrap; background-color: #f5f5f5; padding: 15px;"
    >
      답변이 여기에 표시됩니다.
    </div>
    <script>
      async function askAI() {
        const questionInput = document.getElementById("question-input");
        const answerBox = document.getElementById("answer-box");
        const askButton = document.getElementById("ask-button");
        const question = questionInput.value;
        if (!question) {
          alert("질문을 입력해주세요!");
          return;
        }
        answerBox.innerText = "AI가 생각 중입니다...";
        askButton.disabled = true;
        try {
          // 💡 바로 이 주소를 Render에서 받은 공개 주소로 바꿔주세요!
          const API_ENDPOINT = "http://127.0.0.1:8000/ask";
          const response = await fetch(API_ENDPOINT, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: question }),
          });
          if (!response.ok) {
            throw new Error(`서버 오류: ${response.statusText}`);
          }
          const data = await response.json();
          answerBox.innerText = data.answer;
        } catch (error) {
          answerBox.innerText = `오류가 발생했습니다: ${error.message}`;
        } finally {
          askButton.disabled = false;
        }
      }
    </script>
  </body>
</html>
```

이 가이드를 통해 성공적으로 AI 에이전트를 배포하고 웹사이트에 적용하시기를 바랍니다!

---

## 🤔 부록: 어떤 클라우드 플랫폼이 가장 좋을까?

"Render 말고 다른 곳은 없나요?"라는 질문에 답변해 드립니다. 결론부터 말하면, **입문용으로는 Render가 가장 좋습니다.**

### 주요 클라우드 플랫폼 비교

| 특징             | **Render (현재 가이드)**                                      | **Google Cloud Run**                                                        | **Amazon Web Services (AWS)**                                 |
| :--------------- | :------------------------------------------------------------ | :-------------------------------------------------------------------------- | :------------------------------------------------------------ |
| **핵심 컨셉**    | **"가장 쉬운 배포"**                                          | **"가장 빠른 확장성"**                                                      | **"가장 많은 기능"**                                          |
| **장점**         | - 압도적인 사용 편의성<br>- 직관적인 UI<br>- 예측 가능한 가격 | - 서버리스 (사용 안 하면 0원)<br>- 엄청난 자동 확장 속도<br>- Google 생태계 | - 업계 표준<br>- 거의 무한한 기능<br>- 방대한 커뮤니티와 자료 |
| **단점**         | - 상대적으로 적은 기능<br>- 복잡한 인프라에는 부적합          | - 약간의 학습 곡선<br>- 가격 예측의 어려움                                  | - 가장 높은 복잡도<br>- 복잡한 가격 체계 ("요금 폭탄" 주의)   |
| **이럴 때 추천** | **AI 프로젝트를 빠르고 쉽게 세상에 공개하고 싶을 때**         | 전 세계 사용자를 대상으로 하는 서비스를 만들고 싶을 때                      | 대규모의 안정적인 상용 서비스를 구축하고 싶을 때              |

**결론:**

> 우리 프로젝트처럼 **단일 AI 서버를 배포하는 것이 목표**라면, 복잡한 기능 없이 쉽고 빠르게 배포할 수 있는 **Render가 시간과 노력을 아낄 수 있는 가장 현명한 선택**입니다.
>
> 나중에 프로젝트가 커지면 다른 플랫폼으로 이전하는 것을 고려해볼 수 있습니다. Docker로 포장해두었기 때문에 이전 과정도 비교적 간단합니다.
