from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.router import auth
from app.middleware.session import SessionMiddleware
from app import fortune
app = FastAPI(
    title="xAI Grok API",
    description="API for xAI Grok services including image generation, image understanding, and chat",
    version="0.1.0",
)

app.add_middleware(SessionMiddleware)  # 驗證 session cookie
app.include_router(auth.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(fortune.router)

@app.get("/")
def root():
    return {"message": "Hello, Fortune-Grok backend is running!"}

# ✅ 登入檢查點
@app.get("/me")
def get_me(request: Request):
    return {"user_id": request.state.user_id}

