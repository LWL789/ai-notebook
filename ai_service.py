from openai import OpenAI
from config import API_KEY, BASE_URL, MODEL_NAME
import json
import re

# 新版 OpenAI 客户端初始化方式
client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)

def analyze_question(question_text: str):
    """
    调用大模型分析错题，返回标准答案、错因分析、知识点、变式题
    """
    prompt = f"""
你是一位资深K12全科教师。请分析以下错题，输出JSON格式结果，包含字段：
- standard_answer: 标准答案
- error_analysis: 错因分析（学生为什么会错）
- knowledge_points: 核心知识点（1-3个，用逗号分隔）
- practice_questions: 2-3道同类型巩固练习题（数组）

题目内容：
{question_text}

输出要求：只返回JSON，不要有其他内容。
"""
    try:
        # 新版 API 调用方式：client.chat.completions.create
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "你是资深教育专家，擅长分析错题并给出针对性建议。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            timeout=30
        )
        # 新版返回对象访问方式：response.choices[0].message.content
        content = response.choices[0].message.content
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        else:
            return {"error": "无法解析AI返回内容"}
    except Exception as e:
        return {"error": f"大模型调用失败: {str(e)}"}