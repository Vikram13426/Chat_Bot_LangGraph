from langchain_core.messages import SystemMessage

from services.llm_service import llm
from tools.api_tools import TOOLS
from prompts.system_prompt import SYSTEM_PROMPT


llm_with_tools = llm.bind_tools(TOOLS)


def agent_node(state):
    """
    Agent node responsible for:
    1. Reading conversation history
    2. Deciding whether tools are needed
    3. Calling tools when required
    4. Generating final answers
    """

    messages = [
        SystemMessage(content=SYSTEM_PROMPT)
    ] + state["messages"]
    print("\n===== AGENT INPUT =====")
    for msg in messages:
        print(msg)
    print("=======================\n")

    response = llm_with_tools.invoke(messages)
    
    print("\n===== AGENT RESPONSE =====")
    print(response)
    print("=========================\n")

    return {
        "messages": [response]
    }