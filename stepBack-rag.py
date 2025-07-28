from openai import OpenAI
import requests
from dotenv import load_dotenv
import json
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()

# Get user question
question = input("Please enter your question: >  ")

# Generate step-back prompt
step_back_sys_prompt = """
You are a helpful AI assistant which is master in creating step back prompt.

Rules-
1. Follow the strict JSON output as per output schema.
2. Abstract the key concepts and principles relevant to question.
3. Use the abstraction to reason through the question

Output Format-
{{
    "prompt": "string"
}}

Example -
User prompt - Which is best framework to create REST apis in python?
Step back prompt - What is a framework, and which frameworks are available in Python?

User prompt - How to create REST apis in fastapi?
Step back prompt - What are REST APIs, and what steps are involved in creating REST APIs?

User prompt - How to do performance testing in locust?
Step back prompt - What is performance testing, and what are the requirements and steps involved in performance testing?
"""

client = OpenAI(
    api_key=os.environ['GEMINI_API_KEY'],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

msgs = [
    {"role": "system", "content": step_back_sys_prompt},
    {"role": "user", "content": question}
]

step_back_resp = client.chat.completions.create(
    model="models/gemini-1.5-flash-001",
    response_format={"type": "json_object"},
    messages=msgs
)

step_back_prompt = json.loads(step_back_resp.choices[0].message.content)
print("\n🧠 LLM Thinking...")
print("LLM created this step back prompt:")
print(step_back_prompt)

# Generate context using step-back prompt
context_sys_prompt = "You are an AI assistant which helps answer the question."

context_resp = client.chat.completions.create(
    model="models/gemini-1.5-flash-001",
    messages=[
        {"role": "system", "content": context_sys_prompt},
        {"role": "user", "content": step_back_prompt["prompt"]}
    ]
)

context = context_resp.choices[0].message.content

#  Use context to answer original question
answer_sys_prompt = f"""
You are an AI assistant which helps answer the question based on given context.

Refer to the following context:
{context}
"""

final_resp = client.chat.completions.create(
    model="models/gemini-1.5-flash-001",
    messages=[
        {"role": "system", "content": answer_sys_prompt},
        {"role": "user", "content": question}
    ]
)

print("\nLLM Thinking...")
print("🧠: ", final_resp.choices[0].message.content.replace("*", "").replace("`", ""))




# # Load the same embedder used during ingestion
# embedder = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# # Connect to existing Qdrant collection
# vectorstore = QdrantVectorStore.from_existing_collection(
#     collection_name="your_collection_name",  # e.g., "my_docs"
#     url="http://localhost:6333",            # or remote Qdrant URL
#     embedding=embedder
# )

# # Retrieve relevant documents based on step-back prompt
# retrieved_docs = vectorstore.similarity_search(
#     query=step_back_prompt["prompt"],
#     k=5  # Top-k matches
# )

# # Combine content from retrieved documents
# context = "\n\n".join(doc.page_content for doc in retrieved_docs)

# print("\n📄 Retrieved Context from Qdrant:\n", context[:300], "...\n")
