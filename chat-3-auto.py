import json
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()


client =OpenAI(api_key=os.getenv("OPEN-KEY"))

system_prompt="""
You are an AI assistant, You are an Ai assistant who is expert in breaking down complex problem and then reslove them.

For the given user input analyse the input and breakdown the input and breakdown the problem step by step .
Atleast think 5-6 steps on how to solve the problem before soving it down.

The steps are you get a user input, you analyse, you think , you again thik for serveral times, you then come up with a result.

follow these step in sequence that "analyse", "think, "output", "valdate" and finally "result" .

Rules:
1. Follow the strict JSON output as per Output schema.
2. Always perform one step at a time and wait for next input.
3. Carefully analyse the user input before proceeding to the next step.

output Format:
{{step:"string" , content:"string"}}

Example :
Input:what is 2+8.
Output: {{"step":"analyse" ,"content" :"Alright! The user is intersted in maths and user asking the basic maths "}}
Output:{{"step":"think" ,"content" :" To perform th addition i must go from left to right and add the numbers"}}
Output:{{"step":"output" ,"content" :"10"}}
Output:{{"step":"validate" ,"content" :"Its look like the answer 10  is correct for 8+2"}}
Output:{{"step":"result" ,"content" :"The final answer is 10"}}

"""
#chain of thought prompting model
messages =[
     {"role":"system", "content":system_prompt},
]

query = input(">")
messages.append({"role":"user","content":query})

while True:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=300,
        response_format={"type":"json_object"},
        messages=messages

    )

    parsed_reponse = json.loads(response.choices[0].message.content)
    messages.append({"role":"assistant","content":json.dumps(parsed_reponse) })

    if parsed_reponse.get("step") !="output":
        print(f"🧠:{parsed_reponse.get("content")}")
        continue
    print(f"🤖:{parsed_reponse.get("content")}")
    break

# completion = client.chat.completions.create(
#     model="gpt-4o-mini",
#     response_format={"type":"json_object"},
#     max_tokens=250,
#     messages=[
#         {"role":"system", "content":system_prompt},
#         {
#             "role": "user", "content":"What is 3*8+6 "
#         }
#     ]
# )

# print(completion.choices[0].message.content)