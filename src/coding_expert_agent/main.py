from langgraph.graph import StateGraph, START, END
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_google_genai import ChatGoogleGenerativeAI
from .tools import get_company_stack, explain_language, simple_search_summary


tools = [get_company_stack, explain_language, simple_search_summary]

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest")
llm_with_tools = llm.bind_tools(tools)


class State(MessagesState):
    pass


def coding_expert(state: State) -> State:
    response = llm_with_tools.invoke(
        f"""
    당신은 개발자들을 위한 세계 최고 수준의 AI 어시스턴트, "Stackload AI"입니다. 당신의 페르소나는 도움이 되고, 전문적이며, 매우 박식합니다.

    당신의 주요 임무는 주어진 도구를 효과적으로 사용하여 프로그래밍 언어, 회사 기술 스택, 그리고 다른 개발 관련 주제에 대한 사용자의 질문에 답변하는 것입니다.

    **핵심 지침:**
    1. **질의 분석:** 사용자의 의도를 깊이 이해하세요. 특정 회사, 개념, 비교에 대한 질문인가요?
    2. **올바른 도구 선택:** 의도에 따라 가장 적절한 도구(`get_company_stack`, `explain_language`, `simple_search_summary`)를 선택하세요.
    3. **실행 및 종합:** 도구를 실행하여 정보를 수집하세요. **도구의 원시 결과를 그대로 출력해서는 안 됩니다.** 정보를 종합하여 포괄적이고 읽기 쉬우며 잘 구조화된 답변으로 만들어야 합니다. 서식을 위해 마크다운(예: 목록, 굵게)을 사용하세요.
    4. **직접 답변:** 최종적으로 종합된 답변을 사용자에게 직접 제공하세요. 사용한 도구에 대해 언급하지 마세요. "검색에 따르면..."과 같은 말은 하지 마세요. 박식한 전문가로서 정보를 제공하세요.
    5. **실패 처리:** 도구가 실패하거나 유용한 정보를 반환하지 못하는 경우, 요청한 특정 정보를 찾을 수 없다고 정중하게 사용자에게 알리세요. 정보를 지어내지 마세요.

    사용자의 질문과 대화 기록을 바탕으로 대화를 시작하세요.

    대화 기록:
    {state['messages']}
    """
    )
    return {"messages": [response]}


tool_node = ToolNode(tools=tools)

graph_builder = StateGraph(State)
graph_builder.add_node("agent", coding_expert)
graph_builder.add_node("tools", tool_node)
graph_builder.add_edge(START, "agent")
graph_builder.add_conditional_edges("agent", tools_condition)
graph_builder.add_edge("tools", "agent")
graph_builder.add_edge("agent", END)

graph = graph_builder.compile(name="coding_expert")


def main():
    print("[CodingExpert] 질문을 입력하세요. 종료하려면 빈 입력 후 Enter.")
    while True:
        user = input("You: ").strip()
        if user == "":
            break
        result = graph.invoke({"messages": [
            {"role": "user", "content": user}
        ]})
        ai_msg = result["messages"][-1]
        print("AI:", getattr(ai_msg, "content", str(ai_msg)))


if __name__ == "__main__":
    main()


