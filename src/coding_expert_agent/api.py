import dotenv

# FastAPI 앱이 시작되기 전에 .env 파일을 로드하여 환경 변수를 설정합니다.
# 이것이 서버 애플리케이션의 가장 안정적인 진입점입니다.
dotenv.load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any

# main.py에서 에이전트 그래프를 가져옵니다.
# .py 파일이므로 .main이 아닌 main으로 가져옵니다.
from .main import graph

app = FastAPI(
    title="Coding Expert AI Agent API",
    description="코딩 관련 질문에 답변하는 AI 에이전트 API 서버입니다.",
    version="1.0.0",
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 프로덕션에서는 특정 도메인만 허용하세요.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    """API 요청 본문을 위한 Pydantic 모델"""
    question: str

class AnswerResponse(BaseModel):
    """API 응답 본문을 위한 Pydantic 모델"""
    answer: str

@app.get("/", summary="Health Check")
def read_root():
    """서버가 정상적으로 실행 중인지 확인하는 기본 엔드포인트"""
    return {"status": "ok", "message": "코딩 전문가 AI 에이전트 API가 실행 중입니다."}


@app.post("/ask", response_model=AnswerResponse, summary="AI 에이전트에게 질문하기")
def ask_agent(request: QuestionRequest) -> Any:
    """사용자의 질문을 받아 AI 에이전트의 답변을 반환합니다."""
    # LangGraph 체인을 실행합니다.
    inputs = {"messages": [("user", request.question)]}
    result = graph.invoke(inputs)
    
    # 마지막 AI 메시지를 추출하여 반환합니다.
    ai_message = result["messages"][-1]
    answer = getattr(ai_message, "content", str(ai_message))
    
    return {"answer": answer}
