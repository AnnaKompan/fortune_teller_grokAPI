#!/bin/sh
set -e

# 加更多調試信息
echo "開始前端容器初始化..."

# 如果沒有 package.json，則手動創建基本 Nuxt 專案
if [ ! -f "/app/package.json" ]; then
    echo "初始化 Nuxt 3 專案 (JavaScript)..."
    
    # 手動創建基本 package.json
    cat > /app/package.json << 'EOL'
{
  "name": "fortune-grok-frontend",
  "private": true,
  "type": "module",
  "scripts": {
    "build": "nuxt build",
    "dev": "nuxt dev",
    "generate": "nuxt generate",
    "preview": "nuxt preview",
    "postinstall": "nuxt prepare"
  },
  "devDependencies": {
    "nuxt": "^3.10.3"
  }
}
EOL
    
    # 創建基本的 Nuxt 配置文件 (JavaScript)
    cat > /app/nuxt.config.js << 'EOL'
// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  // 使用 JavaScript
  typescript: {
    strict: false,
    shim: false
  }
})
EOL

    # 創建基本的 app.vue
    cat > /app/app.vue << 'EOL'
<template>
  <div>
    <NuxtPage />
  </div>
</template>
EOL

    echo "創建必要目錄結構..."
    mkdir -p /app/assets /app/components /app/pages

    # 創建示例頁面 (JavaScript)
    cat > /app/pages/index.vue << 'EOL'
<template>
  <div class="container">
    <h1>Fortune Grok</h1>
    <p>運勢查詢網站</p>
    <p>這是一個使用 JavaScript 開發的 Nuxt 3 專案</p>
  </div>
</template>

<script>
export default {
  name: 'IndexPage',
  setup() {
    // 這裡可以添加頁面邏輯
    return {}
  }
}
</script>

<style>
.container {
  margin: 2rem;
  text-align: center;
}
</style>
EOL

    # 創建 README 文件
    cat > /app/README.md << 'EOL'
# Fortune Grok 前端

這是 Fortune Grok 的前端專案，使用 Nuxt 3 開發。

## 開發指南

1. 此專案已經設置為使用 JavaScript
2. 添加新套件: `npm install 套件名稱`
3. 創建新頁面: 在 `pages/` 目錄下創建 .vue 文件
4. 創建新組件: 在 `components/` 目錄下創建 .vue 文件

## 推薦套件

- UI 框架: Element Plus, Tailwind CSS, Vuetify
- 狀態管理: Pinia
- HTTP 客戶端: Axios, Fetch API
EOL

    echo "安裝基本依賴..."
    cd /app && npm install

    echo "Nuxt 3 (JavaScript) 專案初始化完成"
fi

# 運行開發伺服器
echo "啟動 Nuxt 開發伺服器..."
cd /app && exec npm run dev -- --host 0.0.0.0 