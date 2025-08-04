from langchain_ollama import ChatOllama
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_neo4j import Neo4jVector

from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

from src.services.utils import format_docs

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

def configure_reddit_rag_chain(llm, embeddings, embeddings_store_url, username, password):
    general_system_template = """ 
    Use the following pieces of context to answer the question at the end.
    The context contains posts and comments from Reddit discussions about bitcoin/cryptocurrency price prediction/events.
    You should prefer information from highly upvoted posts and comments with substantial discussion.
    Make sure to rely on information from the comments and analysis rather than just speculation to provide accurate responses.
    When you find particular post or comment in the context useful, make sure to cite it in the answer using the Reddit link.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    ----
    {summaries}
    ----
    Each answer you generate should contain a section at the end that links to 
    Reddit posts and comments you found useful, which are described under Source value.
    You can only use links to Reddit posts that are present in the context and always
    add links to the end of the answer in the style of citations.
    Generate concise answers with references sources section of links to 
    relevant Reddit posts only at the end of the answer.
    """
    general_user_template = "Question:```{question}```"
    
    messages = [
        SystemMessagePromptTemplate.from_template(general_system_template),
        HumanMessagePromptTemplate.from_template(general_user_template),
    ]

    qa_prompt = ChatPromptTemplate.from_messages(messages)

    # Vector + Knowledge Graph response
    kg = Neo4jVector.from_existing_index(
        embedding=embeddings,
        url=embeddings_store_url,
        username=username,
        password=password,
        database="neo4j",  # neo4j by default
        index_name="reddit",  # vector by default
        text_node_property="body",  # text by default
        retrieval_query="""
    WITH node as RedditPost
    CALL  { with reddit_post
        MATCH (question)<-[:ANSWERS]-(answer)
        WITH answer
        ORDER BY answer.is_accepted DESC, answer.score DESC
        WITH collect(answer)[..2] as answers
        RETURN reduce(str='', answer IN answers | str + 
                '\n### Answer (Accepted: '+ answer.is_accepted +
                ' Score: ' + answer.score+ '): '+  answer.body + '\n') as answerTexts
    } 
    RETURN '##Question: ' + question.title + '\n' + question.body + '\n' 
        + answerTexts AS text, similarity as score, {source: question.link} AS metadata
    ORDER BY similarity ASC // so that best answers are the last
    """,
    )

    kg_qa = (
        RunnableParallel(
            {
                "summaries": kg.as_retriever(search_kwargs={"k": 2}) | format_docs,
                "question": RunnablePassthrough(),
            } # this dict is passed to the next steps, runnnablepassthrough pushes the data through unchanged
        )
        | qa_prompt
        | llm
        | StrOutputParser()
    )
    return kg_qa

def test_llm_only_chain(question):
    print("Testing LLM only chain with question:", question)

    llm = ChatOllama(
        model="gemma3:12b",
        temperature=0,
        # other params...
    )

    chain = configure_llm_only_chain(llm)
    response = chain.invoke(question)
    print(response)
