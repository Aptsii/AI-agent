import os
import dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

print("--- Google API 키 진단을 시작합니다 ---")

# .env 파일 경로를 찾아서 로드합니다.
# 이 스크립트는 'src/coding_expert_agent'에 있으므로 .env 파일은 두 단계 위에 있습니다.
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
is_loaded = dotenv.load_dotenv(dotenv_path)

if is_loaded:
    print("✅ .env 파일을 성공적으로 찾았습니다.")
else:
    print("🚨 오류: .env 파일을 찾을 수 없습니다.")
    print("   'copy/coding-expert-agent' 폴더에 .env 파일이 있는지 확인해주세요.")
    exit()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("🚨 오류: .env 파일에서 GOOGLE_API_KEY를 찾을 수 없습니다.")
    print("   파일 내용은 GOOGLE_API_KEY=\"AIza...\" 형식이어야 합니다.")
    exit()
else:
    print(f"✅ API 키를 찾았습니다. (시작: {api_key[:5]}...)")

try:
    print("⏳ Gemini 모델 초기화를 시도합니다...")
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest")
    print("✅ 모델 초기화 성공. 모델 호출을 시도합니다...")
    
    response = llm.invoke("Hello!")
    
    print("\n🎉🎉🎉 성공! 🎉🎉🎉")
    print("API 키가 정상이며, 모델이 성공적으로 응답했습니다.")
    print(f"모델 응답: {response.content}")

except Exception as e:
    print("\n🔥🔥🔥 실패! 🔥🔥🔥")
    print("API 키를 사용해 모델을 호출하는 중 오류가 발생했습니다.")
    print(f"오류 종류: {type(e).__name__}")
    print("--- 오류 상세 내용 ---")
    print(e)
    print("--------------------")
    print("\n[해결 방법]")
    print("1. Google AI Studio에서 API 키를 다시 한번 확인하고 복사하여 .env 파일에 붙여넣어 보세요.")
    print("2. Google Cloud 프로젝트에서 'Generative Language API'가 '사용 설정' 되어 있는지 확인해주세요.")
