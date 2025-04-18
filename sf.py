import os
from dotenv import load_dotenv
from openai import OpenAI

model = 'deepseek-ai/DeepSeek-V2.5'

def llm_response(messages):
    load_dotenv()
    api_key = os.getenv("SILICONFLOW_API_KEY")

    client = OpenAI(api_key=api_key, base_url="https://api.siliconflow.com/v1")
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True
    )
    # Collect the entire response
    full_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            full_response += chunk.choices[0].delta.content
    return full_response

if __name__ == "__main__":
    print(llm_response([
                {'role': 'user', 
                'content': "1+1=？reply with one number."},
            ]))
