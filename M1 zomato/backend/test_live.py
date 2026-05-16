import os
import json
from dotenv import load_dotenv

load_dotenv()

from phase3 import build_prompt
from phase4 import get_recommendations

payload = {
    "staticContext": {
        "location": "Koramangala",
        "budget": "medium",
        "cuisine": "Any"
    },
    "nuanceContext": "family lunch, looking for top 5 restaurants with 4.0+ rating"
}

prompt, error, candidates = build_prompt(payload)

if error:
    print(f"Error in Phase 3: {error}")
else:
    print("--- Generated Prompt from Phase 3 ---")
    print(prompt)
    print("--------------------------------------\n")
    print("Calling Groq (Phase 4)... please wait...")
    
    result = get_recommendations(prompt)
    
    print("\n--- Final Output from Groq ---")
    print(json.dumps(result, indent=2))
    print("------------------------------")
