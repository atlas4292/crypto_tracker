from langchain_ollama import ChatOllama


def test_llm(sentence_to_translate):
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
        ("human", sentence_to_translate),
    ]

    print("Asking LLM to translate the sentence...")
    ai_msg = llm.invoke(messages)
    print(ai_msg.content)
