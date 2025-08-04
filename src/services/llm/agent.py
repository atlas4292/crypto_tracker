from langchain_ollama import ChatOllama


def test_llm(sentence_to_translate):
    llm = ChatOllama(
        model="qwen3:4b",
        temperature=0,
        # other params...
    )

    messages = [
        (
            "system",
            "You are a helpful assistant that translates English to French. Translate the user sentence.",
        ),
        ("human", sentence_to_translate),
    ]

    print("Asking LLM to translate the sentence...")
    return llm.invoke(messages)
