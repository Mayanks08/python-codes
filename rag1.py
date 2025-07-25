from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from openai import OpenAI
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient


pdf_path = Path(__file__).parent/ "C++_notes.pdf" 

loader = PyPDFLoader(
    file_path=pdf_path,
)
docs =loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
split_docs= text_splitter.split_documents(documents=docs)
embedder =OpenAIEmbeddings(
    model="text-embedding-3-large",
    api_key=apikey
)

# vector_store=QdrantVectorStore.from_documents(
#     documents=split_docs,
#     collection_name="learning_langchain",
#     url="http://localhost:6333",
#     embedding=embedder
# )

# vector_store.add_documents(documents=split_docs)
print("Injection Done")

retriver =QdrantVectorStore.from_existing_collection(
     collection_name="learning_langchain",
     url="http://localhost:6333",
     embedding=embedder
)

search_result = retriver.similarity_search(query="what is Pointer in c++?")
print("Relevant chunks",search_result)