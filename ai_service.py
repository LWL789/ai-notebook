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
你是一位资深K12全科教师。请分析以下错题，输出严格的JSON格式结果，包含字段：
- standard_answer: 字符串，标准答案
- error_analysis: 字符串，错因分析
- knowledge_points: 字符串，核心知识点（1-3个，用逗号分隔）
- practice_questions: 数组，包含2-3道同类型巩固练习题（每个元素是一个字符串）

题目内容：
{question_text}

输出要求：
1. 只返回JSON，不要有其他内容
2. practice_questions 必须是字符串数组，例如 ["题目1", "题目2"]
3. 所有字段值必须是字符串或字符串数组，不要嵌套对象
"""
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "你是资深教育专家，擅长分析错题并给出针对性建议。请始终输出严格的JSON格式。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            timeout=30
        )
        content = response.choices[0].message.content
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            # 确保 practice_questions 是数组格式
            if "practice_questions" in result and not isinstance(result["practice_questions"], list):
                result["practice_questions"] = []
            return result
        else:
            return {"error": "无法解析AI返回内容"}
    except Exception as e:
        return {"error": f"大模型调用失败: {str(e)}"}
            return {"error": "无法解析AI返回内容"}
    except Exception as e:
        return {"error": f"大模型调用失败: {str(e)}"}
