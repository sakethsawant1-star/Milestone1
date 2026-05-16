import os
import json
from groq import Groq

def get_recommendations(prompt):
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return {
            "error": "GROQ_API_KEY is not set. Add it to backend/.env locally or to your Railway environment variables."
        }

    try:
        client = Groq(api_key=api_key)
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful JSON-only outputting AI."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"},
            temperature=0.7,
        )
        
        response_content = chat_completion.choices[0].message.content
        return json.loads(response_content)
    except Exception as e:
        return {"error": str(e)}
