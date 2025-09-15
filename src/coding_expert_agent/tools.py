from langchain_core.tools import tool
from ddgs import DDGS

# DuckDuckGoSearchRun 대신 DDGS를 직접 사용하여 더 많은 제어를 합니다.
# DDGS().text()는 검색 결과의 제목과 스니펫을 반환합니다.
# max_results를 설정하여 가져오는 정보의 양을 조절할 수 있습니다.
search_client = DDGS()

def search_and_summarize(query: str, max_results: int = 5) -> str:
    """주어진 쿼리로 웹 검색을 수행하고 결과를 요약하여 반환합니다."""
    try:
        results = search_client.text(query, max_results=max_results)
        if not results:
            return "검색 결과가 없습니다."
        
        # [snippet: ..., title: ..., url: ...] 형식의 결과를 하나의 문자열로 결합합니다.
        return "\n\n".join(
            f"출처 제목: {res['title']}\n내용: {res['body']}"
            for res in results
        )
    except Exception as e:
        return f"검색 중 오류가 발생했습니다: {e}"

@tool
def get_company_stack(company: str) -> str:
    """회사 이름을 받아 해당 회사의 기술 스택에 대한 웹 검색 결과를 반환합니다."""
    query = f"{company} 기술 스택 채용 공고"
    return search_and_summarize(query, max_results=5)

@tool
def explain_language(language: str) -> str:
    """프로그래밍 언어 이름을 받아 해당 언어에 대한 웹 검색 결과를 반환합니다."""
    query = f"프로그래밍 언어 {language} 특징과 주요 사용 사례"
    return search_and_summarize(query, max_results=3)

@tool
def simple_search_summary(query: str) -> str:
    """일반적인 질문에 대해 웹 검색을 수행하고 그 결과를 반환합니다."""
    return search_and_summarize(query, max_results=5)



