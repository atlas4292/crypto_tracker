from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="gemma3:12b",
    temperature=0,
    # other params...
)

messages = [
    (
        "system",
        "You are a helpful assistant that translates English to French. Translate the user sentence.",
    ),
    ("human", "What is your favorite color?"),
]
ai_msg = llm.invoke(messages)
print(ai_msg.content)