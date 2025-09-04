from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from openai import OpenAI
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
import os

load_dotenv()
pdf_path = Path(__file__).parent/ "C++_notes.pdf" 
client =OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


loader = PyPDFLoader(
    file_path=pdf_path,
)
docs =loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
split_docs= text_splitter.split_documents(documents=docs)
embedder =OpenAIEmbeddings(
    model="text-embedding-3-large",
    
)

# vector_store=QdrantVectorStore.from_documents(
#     documents=split_docs,
#     collection_name="learning C++",
#     url="http://localhost:6333",
#     embedding=embedder
# )

# vector_store.add_documents(documents=split_docs)
print("Injection Done")

retriver =QdrantVectorStore.from_existing_collection(
     collection_name="learning C++",
     url="http://localhost:6333",
     embedding=embedder
)


# while True:
#     query = input("\nAsk me something about C++ (or type 'exit' to quit): ")

#     if query.lower() in ["exit", "quit"]:
#         print("Goodbye!")
#         break

#    
#     search_result = retriver.similarity_search(query=query, k=3)

#     if not search_result:
#         print(" No relevant chunks found.")
#         continue

#     # print chunks
#     for i, doc in enumerate(search_result):
#         page_number = doc.metadata.get("page", "Unknown")
#         print(f"\n--- Relevant Chunk {i+1} ---")
#         print("Content:\n", doc.page_content.strip())
#         print(f"Page Number: {page_number}")


llm = ChatOpenAI(
    model="gpt-4o-mini",   
    temperature=0 ,        
    
)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriver.as_retriever(),
    chain_type="stuff",  
)

while True:
    query = input("\nAsk me something about C++ (or type 'exit' to quit): ")

    if query.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break


    answer = qa_chain.invoke(query)
    print("\n💡 Structured Answer:\n", answer)
