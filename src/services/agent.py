from langchain_ollama import ChatOllama
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)


def configure_llm_only_chain(llm):
    # LLM only response
    template = """
    You are a helpful assistant that helps a support agent with answering programming questions.
    If you don't know the answer, just say that you don't know, you must not make up an answer.
    """
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = "{question}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )
    chain = chat_prompt | llm | StrOutputParser()
    return chain

def configure_qa_chain():
    pass

def test_llm_only_chain(question):
    llm = ChatOllama(
        model="gemma3:12b",
        temperature=0,
        # other params...
    )
    chain = configure_llm_only_chain(llm)
    response = chain.invoke(question)
    print(response)


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

print("Asking LLM to translate the sentence...")
ai_msg = llm.invoke(messages)
print(ai_msg.content)

test_llm_only_chain("What is the capital of France?")
