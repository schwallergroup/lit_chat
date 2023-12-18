import openai
import os

keys_file = open("/home/wellawatte/Desktop/key.txt")
lines = keys_file.readlines()
apikey = lines[0].rstrip()
os.environ["OPENAI_API_KEY"] = apikey
openai.api_key = apikey
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from lit_chat.prompts import QA_PROMPT


embedding = OpenAIEmbeddings()


def get_docs(query, **kwargs):
    """gather evidence from a file for a given query"""

    ## TODO: ADD PATH TO VECTORSTORE
    persist_directory = "vectorstore"
    top_k = kwargs.get("top_k", 10)
    num_chunks = 30

    db = Chroma(persist_directory=persist_directory, embedding_function=embedding)

    doc_chunks = db.similarity_search_by_vector_with_relevance_scores(
        embedding.embed_query(query), k=num_chunks
    )

    # lower the score the most similar, already sorted
    if len(doc_chunks) > top_k:
        doc_chunks = doc_chunks[:top_k]

    evidence = ""
    for doc in doc_chunks:
        chunk = doc[0].page_content
        try:
            authors = doc[0].metadata["authors"]
            year = doc[0].metadata["year"]
            citation = f"{authors} ({year})"
            evidence += f"{chunk} \ncitation: {citation}"

        except:
            evidence += chunk

    return evidence


def ask_gpt_with_docs(question):
    evidence = get_docs(question)

    prompt = QA_PROMPT.format(question, evidence)

    messages = [
        {
            "role": "system",
            "content": "Your goal is to find answers to asked questions based on literature.",
        },
        {"role": "user", "content": prompt},
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.1,
    )
    answer = response.choices[0].message["content"]

    return answer
