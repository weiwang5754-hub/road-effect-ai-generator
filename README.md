# 🛤️ 市政横断面道路效果图 AI 生成器

基于 **Tabbit AI（豆包 Seedream 5.0）** 的市政道路效果图在线生成工具。

上传横断面草图 → 输入描述 → 一键生成专业效果图

## ✨ 特性

- 🌟 **Tabbit AI 豆包大模型** — 首选生图模型，效果出色
- 📐 多种分辨率支持（1024~2048，多种比例）
- 🖼️ 图图对比滑块（原图 vs 生成图）
- 📋 历史记录自动保存（IndexedDB）
- ⚡ 无需本地安装，浏览器直接使用

## 🚀 在线访问

**GitHub Pages 前端**: [部署后自动生成链接]

## 📦 部署指南

### 方式一：快速部署（推荐）

#### 1. 部署 API 后端（任选一个平台）

**Railway（免费额度）:**
```bash
# 点击下方按钮一键部署
# 或手动：
git clone <本仓库>
cd road-effect-api
railway up
# 设置环境变量 SILICONFLOW_API_KEY=你的密钥
```

**Render（免费）:**
```bash
# 在 render.com 创建 Web Service
# Build Command: pip install -r requirements.txt
# Start Command: python api/server.py
# 环境变量: SILICONFLOW_API_KEY=你的密钥
```

#### 2. 获取 SiliconFlow API Key（免费）

1. 注册 [SiliconFlow](https://cloud.siliconflow.cn/)
2. 进入 [API Keys](https://cloud.siliconflow.cn/account/ak) 页面
3. 创建新的 API Key（免费用户有额度）

#### 3. 配置前端 API 地址

编辑 `road-effect-generator.html` 中的 `API_BASE_URL`：

```javascript
// 将下面的地址改为你的 API 后端地址
const API_BASE_URL = 'https://your-api-domain.com';
```

### 方式二：本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 启动 API 后端（端口 8192）
python api/server.py

# 另开终端，启动前端（端口 8899）
python -m http.server 8899

# 浏览器打开 http://localhost:8899
```

## 🔧 配置说明

| 环境变量 | 说明 | 必填 |
|---------|------|------|
| `SILICONFLOW_API_KEY` | SiliconFlow API 密钥 | 是 |
| `PORT` | 服务端口（默认 8192） | 否 |

## 📁 项目结构

```
├── road-effect-generator.html   # 前端页面（GitHub Pages 托管）
├── api/
│   └── server.py                # API 后端（Flask）
├── requirements.txt             # Python 依赖
├── vercel.json                  # Vercel 部署配置
└── README.md                    # 本文件
```

## 🤝 技术栈

- **前端**: 原生 HTML/CSS/JavaScript（无框架依赖）
- **后端**: Python Flask + SiliconFlow API
- **模型**: Doubao Seedream 5.0 / FLUX.1-schnell / SDXL
- **托管**: GitHub Pages + Railway/Render/Vercel

## 📄 License

MIT
