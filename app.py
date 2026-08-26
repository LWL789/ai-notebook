import streamlit as st
import tempfile
from PIL import Image
import pandas as pd
from datetime import datetime

from auth import show_login
from database import get_db, save_wrong_note, get_notes_by_user, get_stats, update_mastery
from ocr_service import ocr_image
from ai_service import analyze_question
import json
from models import init_db
init_db()
st.set_page_config(page_title="AI智能错题本", layout="wide")

if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    show_login()
    st.stop()

st.sidebar.title(f"👤 {st.session_state['username']}")
menu = st.sidebar.radio("导航", ["📥 录入错题", "📖 错题本", "📊 数据看板", "🚪 退出"])

if menu == "🚪 退出":
    st.session_state.clear()
    st.rerun()

db = next(get_db())
user_id = st.session_state['user_id']

if menu == "📥 录入错题":
    st.header("📥 录入错题")
    
    # 选择模式：OCR 还是 存原图
    mode = st.radio(
        "选择录入方式：",
        ["📝 OCR识别文字", "🖼️ 直接存原图"],
        index=0
    )
    
    st.subheader("📷 上传错题图片")
    
    # 用 with 包裹上传和表单
    with st.form("entry_form"):
        uploaded_file = st.file_uploader("选择图片", type=['jpg', 'png', 'jpeg'])
        
        if uploaded_file:
            st.session_state['uploaded_image'] = uploaded_file.getvalue()
            col1, col2 = st.columns(2)
            with col1:
                img = Image.open(uploaded_file)
                st.image(img, caption="原图", width=300)
            
            with col2:
                if mode == "📝 OCR识别文字":
                    if st.form_submit_button("🔍 开始OCR识别"):
                        with st.spinner("OCR识别中..."):
                            ocr_text = ocr_image(uploaded_file)
                            st.session_state['ocr_text'] = ocr_text
                            if "失败" in ocr_text:
                                st.error(ocr_text)
                            else:
                                st.success("识别成功！请检查下方文本")
                                st.text_area("识别结果", ocr_text, height=150)
                                
                                with st.spinner("AI分析中..."):
                                    ai_result = analyze_question(ocr_text)
                                    st.session_state['ai_result'] = ai_result
                                    if "error" not in ai_result:
                                        st.success("AI分析完成！")
                                        st.json(ai_result)
                                    else:
                                        st.error(ai_result.get("error", "AI分析失败"))
                else:
                    st.info("🖼️ 直接存原图模式：图片将保存，不进行OCR识别")
        
        st.divider()
        
        # 🆕 根据模式动态显示题目输入框
        if mode == "📝 OCR识别文字":
            # OCR 模式：显示文本框，方便修改
            default_text = st.session_state.get('ocr_text', '')
            question = st.text_area("题目内容（可手动修改）", value=default_text, height=120)
        else:
            # 直接存原图模式：不显示题目输入框，自动填入提示
            question = "（原图模式，无文字内容）"
            st.info("💡 直接存原图模式已保存图片，无需输入题目文字。")
        
        # 标签和掌握度始终显示
        col1, col2 = st.columns(2)
        with col1:
            tags = st.text_input("标签（逗号分隔）", placeholder="例如：数学,一元二次方程")
        with col2:
            mastery = st.selectbox("掌握程度", ["未掌握", "基本掌握", "已掌握"])
        
        submitted = st.form_submit_button("💾 保存错题")
        if submitted:
            # 保存逻辑不变，但如果是存原图模式，question 自动填入提示
            if not uploaded_file:
                st.error("请至少上传一张图片")
            else:
                ai_data = st.session_state.get('ai_result', {})
                std_answer = ai_data.get('standard_answer', '')
                error_analysis = ai_data.get('error_analysis', '')
                knowledge = ai_data.get('knowledge_points', '')
                if tags:
                    knowledge = tags
                
                image_data = st.session_state.get('uploaded_image')
                image_path = None
                if image_data:
                    import base64
                    image_path = base64.b64encode(image_data).decode('utf-8')
                
                note = save_wrong_note(
                    db, user_id, question, std_answer, error_analysis,
                    knowledge, tags, image_path, mastery
                )
                st.success(f"✅ 错题已保存 (ID: {note.id})")
                st.session_state['ocr_text'] = ''
                st.session_state['ai_result'] = {}
                st.session_state['uploaded_image'] = None
                st.rerun()


                    

elif menu == "📊 数据看板":
    st.header("📊 学习数据看板")
    total, mastered, rate = get_stats(db, user_id)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("📝 总错题数", total)
    col2.metric("✅ 已掌握", mastered)
    col3.metric("🎯 掌握率", f"{rate:.1f}%")
    
    st.subheader("📈 错题趋势（近7日）")
    import random
    data = pd.DataFrame({
        "日期": pd.date_range(end=datetime.now(), periods=7).strftime("%m-%d"),
        "新增错题": [random.randint(0, 5) for _ in range(7)]
    })
    st.line_chart(data.set_index("日期"))
    
    notes = get_notes_by_user(db, user_id)
    tag_counts = {}
    for note in notes:
        if note.tags:
            for tag in note.tags.split(','):
                tag = tag.strip()
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
    
    if tag_counts:
        st.subheader("🏷️ 知识点标签分布")
        st.bar_chart(pd.DataFrame(list(tag_counts.items()), columns=["标签", "数量"]).set_index("标签"))

st.sidebar.markdown("---")
st.sidebar.caption("AI智能错题本 v1.0 | 数据本地存储")
