import requests #lets python senf HTTP requests (talk to APIs)
import os #lets python to read environment variables


GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions" 

def  generate_plan(system_prompt : str) -> str:

    api_key = os.getenv("GROQ_API_KEY")

    headers = {
        "Authorization" : f"bearer {api_key}",
        "content_type": "application/json"
    }

    payload = {
        "model" :"llama-3.3-70b-versatile",
        "messages":[
            {
                "role": "user",
                "content": system_prompt
            }
        ],
        "max_tokens": 2000,
        "temperature": 0.7
    }

    response = requests.post(GROQ_API_URL,json= payload,headers=headers,timeout=60)

  
    if response.status_code != 200:
        raise Exception(f"API error:{response.status_code} - {response.text}")

    result = response.json()
    return result["choices"][0]["message"]["content"]


