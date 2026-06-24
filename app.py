from langchain_core.messages import HumanMessage

from graph import graph


def run_chat():

    while True:

        query = input("\nYou: ")

        if query.lower() in ["exit", "quit"]:
            break

        result = graph.invoke(
            {
                "messages": [
                    HumanMessage(content=query)
                ]
            }
        )

        print(
            "\nAssistant:",
            result["messages"][-1].content
        )


if __name__ == "__main__":
    run_chat()