from fastapi import APIRouter, Request, Response, HTTPException
from fastapi.responses import RedirectResponse
import os, requests
from dotenv import load_dotenv
from itsdangerous import URLSafeSerializer

load_dotenv()
router = APIRouter()
import os
print("SESSION_SECRET =", os.getenv("SESSION_SECRET"))


serializer = URLSafeSerializer(os.getenv("SESSION_SECRET"))
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

@router.get("/login")
def login():
    url = (
        f"https://accounts.google.com/o/oauth2/v2/auth"
        f"?response_type=code&client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={GOOGLE_REDIRECT_URI}"
        f"&scope=openid%20email%20profile"
    )
    return RedirectResponse(url)

@router.get("/auth/google/callback")
def callback(code: str, response: Response):
    token_res = requests.post("https://oauth2.googleapis.com/token", data={
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    })
    token_json = token_res.json()
    access_token = token_json.get("access_token")

    userinfo = requests.get("https://www.googleapis.com/oauth2/v1/userinfo", headers={
        "Authorization": f"Bearer {access_token}"
    }).json()

    user_id = userinfo.get("id")
    session = serializer.dumps({"user_id": user_id})
    response = RedirectResponse("/")  # 可改導向前端頁面
    response.set_cookie("session", session, httponly=True)
    return response

@router.get("/logout")
def logout(response: Response):
    response = RedirectResponse(url="/")  # 或改導向前端，如 http://localhost:3000/
    response.delete_cookie("session")
    return response
