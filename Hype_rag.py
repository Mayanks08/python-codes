from openai import OpenAI
from dotenv import load_dotenv
import os
from pathlib import Path
from collections import Counter
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
from openai import OpenAI
import os


load_dotenv()


load_dotenv()
apikey = os.environ["OPENAI_API_KEY"]
client = OpenAI(api_key=apikey)


pdf_path = Path(__file__).parent / "node_js_sample.pdf"
loader = PyPDFLoader(pdf_path)
docs = loader.load()

# Split document into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)
split_docs = text_splitter.split_documents(documents=docs)


embedder = OpenAIEmbeddings(
    model="text-embedding-3-large",
    api_key=apikey
)

# Only run the below once to insert data into Qdrant
# vector_store = QdrantVectorStore.from_documents(
#     documents=split_docs,
#     embedding=embedder,
#     url="http://localhost:6333",
#     collection_name="learning_node_js",
# )
# vector_store.add_documents(documents=split_docs)

# Connect to existing Qdrant vector store

retriever = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning_node_js",
    embedding=embedder,
)

print("📄 PDF Ingestion Complete!\n")

user_input = input("Please enter your question on node js : >  ")

system_prompt=f"""
you are a helpful assistant that provides relevant answer of user query

now give answer to the question

user input : ${user_input}
"""

print("\n🧠 LLM Thinking \n")

llm_answer = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role":"system","content":system_prompt}]
)

print("\n🧠 LLM generated answer\n")
print(llm_answer.choices[0].message.content.replace("*","").replace("`",""))

print("\n🧠 Preparing final answer : \n")

hypothetical_answer=llm_answer.choices[0].message.content.replace("*","").replace("`","")
query_embedding = embedder.embed_query(hypothetical_answer)

#  embedding to do similarity search
docs = retriever.similarity_search_by_vector(query_embedding, k=5)

#  Final answer from LLM using context + question
context_text = "\n\n".join([doc.page_content for doc in docs])

final_prompt = f"""
You are a Node.js expert. Answer the user's question using the context below.

Context:
{context_text}

User question: {user_input}
"""

final_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": final_prompt}
    ]
)

print("\n✅ Final Answer:\n")
print(final_response.choices[0].message.content.replace("*","").replace("`",""))
