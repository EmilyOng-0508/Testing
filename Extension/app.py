import streamlit as st
import os
import json
import requests

# ==========================================
# 1. Basic Page Configuration
# ==========================================
st.set_page_config(page_title="Study Analyzer", layout="wide", initial_sidebar_state="collapsed")

# ==========================================
# 2. Custom CSS Styling
# ==========================================
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; color: #333333; font-family: 'Arial', sans-serif; }
    header {visibility: hidden;}
    div.stButton > button[kind="secondary"] {
        background-color: transparent; color: #333333; border: none; font-weight: bold;
    }
    div.stButton > button[kind="primary"] {
        background-color: #F4D03F; color: #333333; border: none; border-radius: 30px; 
        padding: 10px 25px; font-weight: bold;
    }
    h1 { font-size: 3rem !important; font-weight: 800 !important; }
</style>
""", unsafe_allow_html=True)

# Initialize page routing state
if 'stage' not in st.session_state:
    st.session_state.stage = 'landing'

# Your Backend Render URL
RENDER_URL = "https://snap-tutor.onrender.com"

# ==========================================
# Page Definitions
# ==========================================
def show_landing_page():
    nav_col1, nav_col2, nav_col3 = st.columns([2, 5, 1])
    with nav_col1: st.write("☕ **Snap Tutor**")
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

def show_login_page():
    st.title("Login / Sign Up")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.text_input("Username")
        st.text_input("Password", type="password")
        if st.button("Continue 🚀", type="primary", use_container_width=True):
            st.session_state.stage = 'profile'
            st.rerun()

def show_profile_page():
    st.title("Complete Your Profile")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.number_input("Age", value=20)
        st.text_input("University", value="Nanyang Technological University (NTU)")
        st.text_input("Course", value="Chemical Engineering") 
        if st.button("Enter Dashboard", type="primary", use_container_width=True):
            st.session_state.stage = 'dashboard'
            st.rerun()

def show_dashboard():
    tab1, tab2, tab3, tab4 = st.tabs([
        "📤 Upload Question", "⚙️ Analysis Setting", "ℹ️ About Us", "❓ FAQs"
    ])

    with tab1:
        st.subheader("Question Capture Area")
        if st.button("🔄 Refresh Question"): st.rerun()
        
        # 1. Display Captured Image
        img_url = f"{RENDER_URL}/uploads/question.png"
        st.image(img_url, caption="Captured Question")

        # 2. Fetch and Display AI Diagnosis JSON via URL
        json_url = f"{RENDER_URL}/uploads/question.json"
        try:
            response = requests.get(json_url)
            if response.status_code == 200:
                result = response.json()
                st.markdown("---")
                st.success(f"### 🧠 AI Diagnosis Result")
                st.write(f"**Topic:** {result.get('topic', 'Unknown')}")
                st.write(f"**Status:** {result.get('status', 'Unknown')}")
                st.info(f"**Detailed Explanation:**\n\n{result.get('explanation', 'No explanation available.')}")
            else:
                st.warning("AI analysis report is being generated, please refresh in a moment...")
        except Exception as e:
            st.error(f"Unable to retrieve diagnosis data: {e}")

# ==========================================
# Routing Control
# ==========================================
if st.session_state.stage == 'landing':
    show_landing_page()
elif st.session_state.stage == 'login':
    show_login_page()
elif st.session_state.stage == 'profile':
    show_profile_page()
elif st.session_state.stage == 'dashboard':
    show_dashboard()