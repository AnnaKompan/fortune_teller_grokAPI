此資料夾用於存放 FastAPI 專案代碼。

---

## 🚀 本地開發指引

1️⃣ 進入 backend 資料夾：

```bash
cd backend

安裝依賴：
pip install -r requirements.txt

啟動 FastAPI 開發伺服器（支援熱重載）：
uvicorn main:app --reload --host 0.0.0.0 --port 8000


環境變數
請參考根目錄的 .env.example 檔案，包含：
	•	DB 連線資訊
	•	Google OAuth 金鑰
	•	Session 密鑰
	•	Grok API 金鑰

開發時可自行建立 .env 檔案。


🐳 Docker

本資料夾已包含 Dockerfile。

開發時可直接使用根目錄的 docker-compose.yml：
docker compose up backend

⚠️ 注意：本地開發建議使用 uvicorn 直接跑，docker 主要供部署用。