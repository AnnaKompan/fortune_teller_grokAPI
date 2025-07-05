FROM python:3.11-slim
WORKDIR /app

# 複製 requirements.txt
COPY requirements.txt .

# 安裝依賴
RUN pip install --no-cache-dir -r requirements.txt

# 準備初始化腳本並確保使用 Unix 行結束符
COPY docker-entrypoint.sh /docker-entrypoint.sh
# 修正可能的 Windows 行結束符問題
RUN sed -i 's/\r$//' /docker-entrypoint.sh && chmod +x /docker-entrypoint.sh

# 設置開發伺服器port
EXPOSE 8000

# 將啟動交給入口腳本處理
ENTRYPOINT ["/docker-entrypoint.sh"]
