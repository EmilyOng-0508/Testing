import streamlit as st
import os  # 必须引入，用来检查图片文件是否存在

# ==========================================
# 1. 网页基本设置
# ==========================================
st.set_page_config(page_title="Study Analyzer", layout="wide", initial_sidebar_state="collapsed")

# ==========================================
# 2. 自定义 CSS (明亮极简 + 胶囊按钮)
# ==========================================
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; color: #333333; font-family: 'Arial', sans-serif; }
    header {visibility: hidden;}

    /* 顶部导航栏按钮样式 */
    div.stButton > button[kind="secondary"] {
        background-color: transparent; color: #333333; border: none; font-weight: bold;
    }
    /* 黄色主按钮样式 */
    div.stButton > button[kind="primary"] {
        background-color: #F4D03F; color: #333333; border: none; border-radius: 30px; 
        padding: 10px 25px; font-weight: bold;
    }
    h1 { font-size: 3rem !important; font-weight: 800 !important; }
</style>
""", unsafe_allow_html=True)

# 初始化页面路由状态
if 'stage' not in st.session_state:
    st.session_state.stage = 'landing'

# ==========================================
# 页面 1: Landing Page (落地页)
# ==========================================
def show_landing_page():
    nav_col1, nav_col2, nav_col3 = st.columns([2, 5, 1])
    with nav_col1: st.write("☕ **Study Analyzer**")
    with nav_col3:
        if st.button("LOGIN", use_container_width=True):
            st.session_state.stage = 'login'
            st.rerun()
    st.write("---")
    
    left, right = st.columns([4, 5])
    with left:
        st.markdown("<h1>Smart Learning Platform</h1>", unsafe_allow_html=True)
        st.write("Your all-in-one place to analyze questions with AI assistance.")
        if st.button("GET STARTED", type="primary"):
            st.session_state.stage = 'login'
            st.rerun()
    with right:
        st.info("插画位置 (Illustration Placeholder)")

# ==========================================
# 页面 2: Login 界面
# ==========================================
def show_login_page():
    st.title("Login / Sign Up")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.text_input("Username")
        st.text_input("Password", type="password")
        if st.button("Continue 🚀", type="primary", use_container_width=True):
            st.session_state.stage = 'profile'
            st.rerun()

# ==========================================
# 页面 3: Profile 界面 (对应你的个人背景)
# ==========================================
def show_profile_page():
    st.title("Complete Your Profile")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.number_input("Age", value=20)
        # 预填你的大学和专业
        st.text_input("University", value="Nanyang Technological University (NTU)")
        st.text_input("Course", value="Chemical Engineering")
        if st.button("Enter Dashboard", type="primary", use_container_width=True):
            st.session_state.stage = 'dashboard'
            st.rerun()

# ==========================================
# 页面 4: Dashboard (核心分析区)
# ==========================================
def show_dashboard():
    # 顶部导航栏 (你要求的那些 Button)
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📤 Upload Question", "📤 Upload Solution", "⚙️ Analysis Setting", "ℹ️ About Us", "❓ FAQs"
    ])

    # --- 1. 题目抓取区 (这里就是读取 Extension 截图的地方) ---
    with tab1:
        st.subheader("Question Capture Area")
        if st.button("🔄 Refresh Question"): st.rerun()
        
        # 检查 api.py 是否已经帮你存好了图片
        if os.path.exists("uploads/question.png"):
            st.image("uploads/question.png", caption="Captured from Extension")
        else:
            st.info("Waiting for screenshot from Chrome Extension...")

    # --- 2. 答案展示区 ---
    with tab2:
        st.subheader("Solution Reference Area")
        if st.button("🔄 Refresh Solution"): st.rerun()
        if os.path.exists("uploads/solution.png"):
            st.image("uploads/solution.png", caption="Solution Screenshot")
        else:
            st.success("Your solution screenshot will appear here.")

    # 其他 Tab 暂时放简单的文字
    with tab3: st.write("AI Settings...")
    with tab4: st.write("About Study Analyzer Team...")
    with tab5: st.write("How to use the extension...")

    if st.sidebar.button("Logout"):
        st.session_state.stage = 'landing'
        st.rerun()

# ==========================================
# 路由控制 (核心逻辑)
# ==========================================
if st.session_state.stage == 'landing':
    show_landing_page()
elif st.session_state.stage == 'login':
    show_login_page()
elif st.session_state.stage == 'profile':
    show_profile_page()
elif st.session_state.stage == 'dashboard':
    show_dashboard()