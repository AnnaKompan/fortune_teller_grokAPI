FROM node:18-alpine
WORKDIR /app

# 複製 package.json 和 package-lock.json
COPY package*.json ./

# 先安裝依賴
RUN npm ci

# 複製其他項目文件
COPY . .

# 安裝 Nuxt CLI 工具
RUN npm install -g nuxi

# 構建應用（用於生產環境的 SSR）
# RUN npm run build

# 設置開發伺服器port
ENV PORT=3000
EXPOSE 3000

# 準備初始化腳本並確保使用 Unix 行結束符
COPY docker-entrypoint.sh /docker-entrypoint.sh
# 修正可能的 Windows 行結束符問題
RUN sed -i 's/\r$//' /docker-entrypoint.sh && chmod +x /docker-entrypoint.sh

# 將啟動交給入口腳本處理
ENTRYPOINT ["/docker-entrypoint.sh"]
