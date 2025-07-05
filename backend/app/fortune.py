from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
import os
import traceback

# Load .env variables
load_dotenv()

router = APIRouter()

# Environment variable for API key
XAI_API_KEY = os.getenv("XAI_API_KEY")

# Request and response schemas
class FortuneRequest(BaseModel):
    keywords: List[str]

class FortuneResponse(BaseModel):
    status: str
    fortune: str = None

@router.post("/fortune", response_model=FortuneResponse)
def get_fortune(req: FortuneRequest):
    print("💡 get_fortune called with:", req.keywords)

    if len(req.keywords) != 3:
        raise HTTPException(status_code=400, detail="Exactly 3 keywords are required.")

    try:
        # Import inside route to avoid import issues during startup
        from openai import OpenAI

        if not XAI_API_KEY:
            raise RuntimeError("XAI_API_KEY is not set in the environment.")

        # Initialize client for GrokAPI
        client = OpenAI(
            api_key=XAI_API_KEY,
            base_url="https://api.x.ai/v1",  # xAI's endpoint
        )

        # Make completion request
        completion = client.chat.completions.create(
            model="grok-3-beta",  # Update if your model is different
            messages=[
                {
                    "role": "system", 
                    "content": """You are Grok, a cheerful fortune-teller who uses lots of emojis.
                    IMPORTANT: Always respond in the same language as the keywords provided by the user.
                    For example:
                    - If keywords are in Chinese/Traditional Chinese, respond in Traditional Chinese
                    - If keywords are in English, respond in English
                    - If keywords are in Japanese, respond in Japanese
                    """
                },
                {
                    "role": "user", 
                    "content": f"""Please analyze these keywords and give a fun and lively fortune using them: {', '.join(req.keywords)}
                    Remember to:
                    1. Use lots of emojis
                    2. Respond in the same language as the keywords
                    3. Give specific predictions for each keyword
                    4. Keep the tone cheerful and optimistic
                    """
                },
            ]
        )

        fortune = completion.choices[0].message.content.strip()

        return FortuneResponse(status="success", fortune=fortune)

    except Exception as e:
        print("❌ Exception occurred in get_fortune():")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"GrokAPI error: {str(e)}")
