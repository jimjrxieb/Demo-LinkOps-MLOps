import os

import chromadb
from langchain.document_loaders import PDFPlumberLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter

UPLOAD_DIR = "rag/uploads"


def embed_all_docs():
    client = chromadb.PersistentClient(path="rag/chroma_db")
    collection = client.get_or_create_collection("documents")

    for file in os.listdir(UPLOAD_DIR):
        path = os.path.join(UPLOAD_DIR, file)
        if file.endswith(".pdf"):
            loader = PDFPlumberLoader(path)
        else:
            loader = TextLoader(path)
        docs = loader.load()
        chunks = CharacterTextSplitter(
            chunk_size=1000, chunk_overlap=100
        ).split_documents(docs)

        for chunk in chunks:
            collection.add(
                documents=[chunk.page_content],
                metadatas=[{"source": file}],
                ids=[f"{file}-{hash(chunk.page_content)}"],
            )
