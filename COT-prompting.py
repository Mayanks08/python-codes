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
import ast

load_dotenv()


# Load environment variables from .env file
load_dotenv()
apikey = os.environ["OPENAI_API_KEY"]

# Initialize OpenAI client
client = OpenAI(api_key=apikey)

#  Load and split PDF
pdf_path = Path(__file__).parent / "node_js_sample.pdf"
loader = PyPDFLoader(pdf_path)
docs = loader.load()

# Split document into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)
split_docs = text_splitter.split_documents(documents=docs)

#  Create an embedder
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

question = input("Please enter your question on node js : >  ")

sys_prompt = f"""
You are an intelligent ai assistant who break down the user input into multiple step of thoughts for better undeerstanding of context 
and for gnerrating better outputs


Example:
User: What is machine learning?
Output:
[
   "what is machine ? ",
   "what is learning ? ",
   "what is machine learning ? "
]

now bassed on the ueser input generate the sub prompts
user input : ${question}
"""
print ("\n🧠 LLM thinking ... \n")

cot_prompts = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "system", "content": sys_prompt}]
)

llm_promts_str=cot_prompts.choices[0].message.content
llm_promts = ast.literal_eval(llm_promts_str) 
print("\nCOT Prompts generated by LLm : > ")
for p in llm_promts:
    print(p)

relevant_docs=[]

for q in llm_promts:
    docs= retriever.similarity_search(query=q)
    relevant_docs.extend(docs)

#  if you want to print relevant docs

# for i, d in enumerate(relevant_docs, 1):
#     print(f"\n📄 Result {i}:\n")
#     print(d.page_content)  

context = "\n\n".join([doc.page_content for doc in relevant_docs])

final_prompt = f"""
You are a knowledgeable AI assistant. Use the provided context below to answer the user's question accurately and helpfully.

Context:
{context}

User question: {question}

Answer:
"""
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": final_prompt}
    ]
)

answer = response.choices[0].message.content
print("\n🤖 Answer:\n")
print(answer.replace("*","").replace("#",""))
