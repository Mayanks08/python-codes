from dotenv import load_dotenv
from openai import OpenAI
import os
import subprocess
import json
import requests

load_dotenv()

client =OpenAI(api_key=os.getenv("OPEN-KEY"))
# client = OpenAI(api_key="sk-1234567890abcdef")  # Replace with your API 

# def run_command(command):
#     try:
#         result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
#         return result
#     except subprocess.CalledProcessError as e:
#         return f"Command failed:\n{e.output}"

def run_command(command):
    git_bash_path = r"C:\Program Files\Git\bin\bash.exe"  # Update if installed elsewhere
    try:
        result = subprocess.check_output(
            [git_bash_path, "-c", command],  # Pass command to Git Bash
            stderr=subprocess.STDOUT,
            text=True
        )
        return result
    except subprocess.CalledProcessError as e:
        return f"Command failed:\n{e.output}"


available_tools={
  
    "run_command":{
        "fn":run_command,
        "description":"Takes a command as input to execut one system  and returns  output",
    }
}

system_prompt = f"""
  You are an helpful AI Assitant Who is specialized in resloving user query 
  you work on start ,plan, action ,observe mode .
  For the give user query and available tools, planing the step by step execution , basesd on the planning,
  select the relvant tool from the available tool . and on the based of the selection you perform an action to called to wait for the observation and based on the observation from the  tool call resove the user query.


  Rules:
  1. Follow the strict JSON output as per Output schema.
  2. Always perform one step at a time and wait for next input.
  3. Carefully analyse the user input before proceeding to the next step.

  output JSON Format:
  {{
    "step":"string",
    "content":"string ",
    "function":"The name of the function if the step is action"
    "input":"The input parameter for the function",   
  }}

  Available Tools:
  -run_command:Takes a command as input to execut one system  and returns  output.
  
  Example:
  User Query: what is the weather in New York?
  Output:{{"step":"plan", "content":"The user is interseted in the weeather data of new york" }}
  Output:{{"step":"plan", "content":"Form the available "tools I should call  get_weather"}}
  Output:{{"step":"action", "function":"get_weather , "input" : "new york" }}
  Output:{{"step":"observe ", "output":"12 Degree Cel" }}
  Output :{{"step":"output","content":"The weather in New York seem to be 12 degree celcius"}}

    """
messages=[
    {"role": "system", "content": system_prompt},
]

while True:
    user_query =input(">")
    messages.append({"role": "user", "content":user_query})
    # if user_query.lower() == "exit":
    break

while True:
    response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=150,
        response_format={"type":"json_object"},
        messages=messages
    )
    parsed_output =json.loads(response.choices[0].message.content)
    messages.append({"role": "assistant", "content": json.dumps(parsed_output)})
    # print(parsed_output)

    if parsed_output.get("step") == "plan":
        print(f"🧠:{parsed_output.get("content")}")
        continue
    
    if parsed_output.get("step") == "action":
        tool_name=parsed_output.get("function")
        tool_input=parsed_output.get("input")

        if available_tools.get(tool_name,False) !=False:
            output=available_tools[tool_name].get("fn")(tool_input)
            messages.append({"role":"assistant","content":json.dumps({"step":"observe","output":output})})
            continue
    
    if parsed_output.get("step") == "output":
        print(f"🤖:{parsed_output.get('content')}")
        break

