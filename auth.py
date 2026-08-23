import streamlit as st
from database import get_db, create_user, authenticate_user

def show_login():
    st.title("📚 AI智能错题本")
    tab1, tab2 = st.tabs(["登录", "注册"])
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("用户名")
            password = st.text_input("密码", type="password")
            submitted = st.form_submit_button("登录")
            if submitted:
                db = next(get_db())
                user = authenticate_user(db, username, password)
                if user:
                    st.session_state['logged_in'] = True
                    st.session_state['user_id'] = user.id
                    st.session_state['username'] = user.username
                    st.rerun()
                else:
                    st.error("用户名或密码错误")
    
    with tab2:
        with st.form("register_form"):
            new_username = st.text_input("新用户名")
            new_password = st.text_input("新密码", type="password")
            confirm = st.text_input("确认密码", type="password")
            submitted = st.form_submit_button("注册")
            if submitted:
                if new_password != confirm:
                    st.error("两次密码不一致")
                elif len(new_password) < 6:
                    st.error("密码至少6位")
                else:
                    db = next(get_db())
                    try:
                        create_user(db, new_username, new_password)
                        st.success("注册成功，请登录")
                    except Exception:
                        st.error("用户名已存在")