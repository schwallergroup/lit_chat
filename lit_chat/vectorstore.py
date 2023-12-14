import os
import argparse
import openai
from prompts import META_PROMPT
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.pydantic_v1 import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from langchain import LLMChain, PromptTemplate
from pypdf import PdfReader
import shutil


class GetMetadata(BaseModel):
    Authors: str = Field(..., description="Authors of the paper")
    Year: str = Field(..., description="Year of publication")
    Title: str = Field(..., description="Title of the paper")


metadata_parser = PydanticOutputParser(pydantic_object=GetMetadata)


def _load_split_docs(filename, chunk_size=1000, chunk_overlap=100, meta_data=None):
    r_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap, length_function=len
    )

    docs = None
    if filename.endswith(".pdf"):
        docs = PyPDFLoader(f"{filename}").load()

    elif filename.endswith(".txt"):
        docs = TextLoader(f"{filename}").load()

    docs_split = r_splitter.split_documents(docs)

    if meta_data is not None:
        for _docs in docs_split:
            _docs.metadata["source"] = meta_data["Title"]
            _docs.metadata["authors"] = meta_data["Authors"]
            _docs.metadata["year"] = meta_data["Year"]

    return docs_split


def _create_vecdb(docs_split, persist_directory):
    if os.path.exists(persist_directory):
        shutil.rmtree(persist_directory)
        os.mkdir(persist_directory)

    vectordb = Chroma.from_documents(
        documents=docs_split, embedding=embedding, persist_directory=persist_directory
    )

    vectordb.persist()


def _update_vecdb(docs_split, persist_directory):
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)

    vectordb.add_documents(
        documents=docs_split, embedding=embedding, persist_directory=persist_directory
    )

    vectordb.persist()


def _set_metadata_llm():
    prompt = META_PROMPT

    llm = ChatOpenAI(temperature=0.0, model_name="gpt-4", request_timeout=1000)

    prompt_template = PromptTemplate(
        template=prompt,
        input_variables=["text"],
        partial_variables={
            "format_instructions": metadata_parser.get_format_instructions()
        },
    )

    llmchain = LLMChain(prompt=prompt_template, llm=llm)

    return llmchain


def _get_metadata(filename, llmchain):
    """'read first 2 pages of a pdf file and extract author, year,title
    for meta data"""
    reader = PdfReader(f"{filename}")
    text = ""
    for page in reader.pages[:2]:
        text += page.extract_text() + "\n"

    response = llmchain.run(text=text)
    metadata = metadata_parser.parse(response).dict()

    return metadata


def set_vectorstore(file_dir, chunk_size=1000, chunk_overlap=100):
    llmchain = _set_metadata_llm()
    persist_directory = "/home/wellawatte/Documents/lit_chat/lit_chat/vectorstore"
    for i, filename in enumerate(os.listdir(file_dir)):
        filename = os.path.join(file_dir, filename)
        print(f"processing {i}th file")

        metadatas = _get_metadata(filename=filename, llmchain=llmchain)
        print(metadatas)

        docs_split = _load_split_docs(
            filename, chunk_size, chunk_overlap, meta_data=metadatas
        )

        if 

        if i == 0:
            _create_vecdb(docs_split, persist_directory)

        else:
            _update_vecdb(docs_split, persist_directory)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--openai_key", type=str, help="Your OPENAI_API_KEY", required=True
    )
    parser.add_argument("--file_dir", type=str, help="Directory of PDFs", required=True)
    parser.add_argument(
        "--chunk_size", type=int, default=1000, help="chunk size for splitting"
    )
    parser.add_argument(
        "--chunk_overlap", type=int, default=100, help="chunk overlap for splitting"
    )
    
    parser.add_argument(
        "--create_new", type=bool, default=True, help="To create a new vectorstore from scratch. Set to False if you want to add more documents of existing vectorestore."
    )

    args = parser.parse_args()
    file_dir = args.file_dir
    chunk_size = args.chunk_size
    chunk_overlap = args.chunk_overlap

    print("arguments received", args)

    if args.openai_key:
        os.environ["OPENAI_API_KEY"] = args.openai_key
        openai.api_key = args.openai_key
        embedding = OpenAIEmbeddings()

    set_vectorstore(file_dir, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
