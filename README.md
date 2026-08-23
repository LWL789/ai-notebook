# AI智能错题本

## 项目简介
AI错题本，支持错题图片上传、OCR文字识别、调用大模型对错题解析、错因分析、生成同类变式练习题；错题可以保存、打标签、检索复习。

**本项目不提供大模型API密钥，请自行配置。**

## 技术栈
- 前端：Streamlit
- 后端：Python
- 数据库：SQLite
- OCR：PaddleOCR
- 大模型：OpenAI兼容接口

## 运行步骤

### 1. 安装依赖
```bash
pip install -r requirements.txt