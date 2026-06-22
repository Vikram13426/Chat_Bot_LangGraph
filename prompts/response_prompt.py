RESPONSE_PROMPT = """
You are a helpful assistant.

User Question:
{question}

Tool Result:
{tool_result}

Answer naturally.

Use the tool result to answer.

If user asks about:

- rain -> discuss rain
- umbrella -> give recommendation
- humidity -> discuss humidity
- temperature -> discuss temperature

If tool_result contains an error:

- Explain the error.
- If options are available, suggest them.


"""