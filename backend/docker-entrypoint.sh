#!/bin/sh
set -e

# 檢查基本目錄結構
mkdir -p /app/app

# 如果 main.py 不存在，則創建基本的 FastAPI 應用
if [ ! -f "/app/app/main.py" ]; then
    echo "初始化 FastAPI 專案..."
    
    # 創建主應用文件
    cat > /app/app/main.py << 'EOL'
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Fortune Grok API")

# 啟用CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Fortune Grok API"}

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}
EOL

    # 創建啟動腳本
    cat > /app/run.py << 'EOL'
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
EOL

    echo "FastAPI 專案初始化完成"
fi

# 運行開發伺服器
echo "啟動 FastAPI 開發伺服器..."
python run.py 