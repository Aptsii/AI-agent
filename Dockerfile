# ==========================================
# Render 배포용 Dockerfile
# ==========================================

# 1. 기반 이미지
FROM python:3.11-slim

# 2. 작업 디렉토리
WORKDIR /app

# 3. 환경 변수
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 4. pip 업그레이드 & uv, uvicorn 설치
RUN pip install --upgrade pip uv uvicorn
RUN pip install python-dotenv langgraph langchain-core pydantic langchain-google-genai ddgs fastapi

# 5. 소스 코드 복사
COPY . .

# 6. 의존성 설치
RUN uv sync

# 7. 컨테이너 시작 시 uvicorn 실행
# Render에서는 런타임에서 $PORT 환경 변수를 제공합니다.
CMD ["sh", "-c", "uvicorn src.coding_expert_agent.api:app --host 0.0.0.0 --port ${PORT}"]

#로컬 테스트
#CMD ["sh", "-c", "uvicorn src.coding_expert_agent.api:app --host 0.0.0.0 --port ${PORT:-8000}"]
