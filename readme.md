# AI智能错题本

## 项目简介
AI智能错题本是一个基于Streamlit开发的智能错题管理工具。通过OCR识别和AI分析，帮助学生高效整理错题、标注知识点、追踪学习进度。

**核心功能**：
- 📝 拍照识别：上传图片，OCR自动识别题目文字
- 🤖 AI分析：自动生成标准答案、错因分析、知识点
- 🖼️ 直接存图：复杂公式/图形题目直接保存原图
- 📚 错题本管理：标签分类、掌握度追踪、筛选检索
- 📊 数据看板：错题统计、趋势图、知识点分布

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端/后端 | Python + Streamlit |
| 数据库 | Supabase PostgreSQL |
| ORM | SQLAlchemy |
| OCR | EasyOCR |
| 大模型 | 硅基流动 API |
| 部署 | Streamlit Cloud |

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置环境变量
在项目根目录创建 `.env` 文件：
```
DATABASE_URL = "你的数据库连接地址"
API_KEY = "你的API密钥"
BASE_URL = "https://api.siliconflow.cn/v1"
MODEL_NAME = "Qwen/Qwen2.5-72B-Instruct"
```

### 3. 启动项目
```bash
streamlit run app.py
```

### 4. 访问
浏览器打开 `http://localhost:8501`

## 项目结构

```
ai-notebook/
├── app.py              # 主程序
├── auth.py             # 用户认证
├── database.py         # 数据库操作
├── models.py           # 数据模型
├── ocr_service.py      # OCR识别
├── ai_service.py       # AI分析
├── config.py           # 环境配置
├── requirements.txt    # 依赖清单
├── README.md           # 项目说明
├── PRD.md              # 产品需求文档
├── 开发规划文档.md      # 开发规划文档
└── 产品设计文档.md      # 产品设计文档
```

## 核心功能说明

### 错题录入
- **OCR识别模式**：上传图片 → 识别文字 → AI分析 → 保存
- **直接存原图模式**：上传图片 → 直接保存（适用公式/图形题）

### 错题本管理
- 按标签筛选、按掌握度筛选
- 修改标签、更新掌握度、删除错题
- 图片放大查看

### 数据看板
- 总错题数、已掌握数、掌握率
- 近7日新增错题趋势图
- 各标签错题数量分布图

## 在线访问

项目已部署在Streamlit Cloud：

**https://ai-notebook-ak8fnwcjiee4tpjyexsazp.streamlit.app**

## 验收标准

| 编号 | 验收项 | 预期结果 |
|------|--------|----------|
| AC-01 | 用户注册登录 | 登录成功，跳转至错题本首页 |
| AC-02 | OCR识别 | 上传图片后正确返回识别文本 |
| AC-03 | AI分析 | 识别后自动生成答案、错因、知识点 |
| AC-04 | 手动录入 | 错题卡片出现在错题本列表中 |
| AC-05 | 标签筛选 | 输入关键词后只显示匹配的错题 |
| AC-06 | 掌握度筛选 | 选择后只显示对应程度的错题 |
| AC-07 | 修改标签 | 修改后自动保存 |
| AC-08 | 更新掌握度 | 更新后自动保存 |
| AC-09 | 删除错题 | 错题从列表中移除 |
| AC-10 | 数据看板 | 统计指标随操作同步变化 |