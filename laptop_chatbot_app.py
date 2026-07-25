import streamlit as st
import os
import base64
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)

try:
    st.set_page_config(
        page_title="Laptop Recommendation AI Advisor",
        page_icon="💻",
        layout="wide"
    )
except Exception:
    pass

base_dir = os.path.dirname(__file__)
bg_path = os.path.join(base_dir, "laptop_bg.png")

def get_base64_bg(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

bg_base64 = get_base64_bg(bg_path)

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&family=Inter:wght@400;500;600;700&display=swap');

    .stApp {{
        background-image: linear-gradient(rgba(15, 23, 42, 0.88), rgba(15, 23, 42, 0.88)), url("data:image/png;base64,{bg_base64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'Inter', sans-serif;
    }}
    .main-panel {{
        background: rgba(30, 41, 59, 0.78);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        border-radius: 20px;
        padding: 34px;
        border: 1px solid rgba(255, 255, 255, 0.16);
        box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.45);
        animation: fadeIn 0.8s ease-out;
    }}
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(18px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    .title-text {{
        font-family: 'Outfit', sans-serif;
        font-size: 2.7rem;
        font-weight: 800;
        background: linear-gradient(135deg, #60A5FA 0%, #3B82F6 50%, #818CF8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }}
    .subtitle-badge {{
        display: inline-block;
        background: rgba(59, 130, 246, 0.18);
        border: 1px solid rgba(96, 165, 250, 0.3);
        border-radius: 20px;
        padding: 6px 16px;
        font-size: 0.85rem;
        font-weight: 600;
        color: #93C5FD !important;
        margin-bottom: 22px;
    }}
    [data-testid="stMain"] p, [data-testid="stMain"] h1, [data-testid="stMain"] h2,
    [data-testid="stMain"] h3, [data-testid="stMain"] h4, [data-testid="stMain"] h5,
    [data-testid="stMain"] h6, [data-testid="stMain"] span, [data-testid="stMain"] label,
    [data-testid="stMain"] li, [data-testid="stMain"] div[data-testid="stMarkdownContainer"] *,
    .stMainBlockContainer *, section.stMain * {{
        color: #FFFFFF !important;
    }}
    input, textarea, select,
    [data-testid="stNumberInput"] input,
    [data-testid="stSelectbox"] select,
    [data-baseweb="select"] *,
    [data-baseweb="input"] input,
    [data-baseweb="textarea"] textarea,
    .stTextInput input, .stNumberInput input, .stTextArea textarea,
    div[data-baseweb="select"] div {{ color: #0F172A !important; }}
    
    .response-card {{
        background: rgba(15, 23, 42, 0.75);
        border-radius: 16px;
        padding: 26px;
        border: 1px solid rgba(96, 165, 250, 0.25);
        margin-top: 15px;
        box-shadow: 0 8px 24px -2px rgba(0, 0, 0, 0.35);
        animation: slideUp 0.4s ease-out;
        color: #FFFFFF !important;
    }}
    @keyframes slideUp {{
        from {{ opacity: 0; transform: translateY(15px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-panel">', unsafe_allow_html=True)
st.markdown('<div class="title-text">💻 Laptop Recommendation AI Advisor</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-badge">Conversational AI · Groq Llama-3 / Hardware Intelligence | Mohd Jibraan</div>', unsafe_allow_html=True)

api_key = os.getenv("GROQ_API_KEY", "")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "preset_prompt" not in st.session_state:
    st.session_state.preset_prompt = ""

tab_chat, tab_guide, tab_settings = st.tabs(["🤖 AI Advisor Chat", "⚖️ Spec Comparison Guide", "⚙️ API & Settings"])

with tab_chat:
    # Sidebar Filters
    st.sidebar.subheader("🎛️ Laptop Filter Preferences")
    budget_category = st.sidebar.selectbox(
        "Target Budget Range",
        ["Under ₹40,000 / $500", "₹40,000 - ₹70,000 / $500-$850", "₹70,000 - ₹1,20,000 / $850-$1500", "Above ₹1,20,000 / $1500+"]
    )
    primary_use = st.sidebar.selectbox(
        "Primary Usage",
        ["Gaming & Graphics", "Programming & Software Engineering", "Student & Everyday Tasks", "Video Editing & Content Creation", "Business & Executive"]
    )
    preferred_os = st.sidebar.selectbox(
        "Preferred Operating System",
        ["Windows 11", "macOS", "Linux / Ubuntu", "Any OS"]
    )

    col_left, col_right = st.columns([1.2, 0.8], gap="large")

    with col_left:
        st.markdown("### 📝 Requirements & Quick Prompts")
        
        # Quick Chips
        st.write("**Quick Prompt Chips:**")
        c_chip1, c_chip2, c_chip3 = st.columns(3)
        if c_chip1.button("🎮 Gaming under ₹80k", use_container_width=True):
            st.session_state.preset_prompt = "Best gaming laptop under ₹80,000 with high refresh rate display, RTX graphics, and fast cooling."
        if c_chip2.button("💻 Developer MacBook Alt", use_container_width=True):
            st.session_state.preset_prompt = "Best coding laptop with 16GB+ RAM, long battery life, Unix/Linux support, and lightweight build."
        if c_chip3.button("🎓 Student under ₹45k", use_container_width=True):
            st.session_state.preset_prompt = "Reliable budget student laptop under ₹45,000 for office work, browser tabs, and video calls."

        default_text = st.session_state.preset_prompt if st.session_state.preset_prompt else f"I am looking for a laptop for {primary_use} in the budget range of {budget_category} with OS: {preferred_os}."
        user_query = st.text_area("Detail your specs, favorite brands, or constraints:", value=default_text, height=120)

        col_b1, col_b2 = st.columns([1, 1])
        with col_b1:
            submit_btn = st.button("🚀 Get AI Recommendations", type="primary", use_container_width=True)
        with col_b2:
            clear_btn = st.button("🔄 Reset Chat", use_container_width=True)

        if clear_btn:
            st.session_state.chat_history = []
            st.session_state.preset_prompt = ""
            st.rerun()

    with col_right:
        st.markdown("### 💡 Recommended Laptops & Analysis")

        if submit_btn and user_query.strip():
            actual_key = api_key
            response_text = ""
            
            if actual_key:
                try:
                    from langchain_groq import ChatGroq
                    from langchain_core.prompts import ChatPromptTemplate
                    
                    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.3, api_key=actual_key)
                    prompt = ChatPromptTemplate.from_template("""
                    You are a expert hardware advisor providing top laptop recommendations.
                    User Request: {question}

                    Format response clearly:
                    1. 🎯 Top 2-3 Recommended Laptops (Brand, Model, CPU, RAM, SSD, GPU, Screen)
                    2. ⚖️ Pros & Cons for Each
                    3. 🛒 Key Specifications Checklist
                    4. 💰 Value-for-Money Verdict
                    """)
                    chain = prompt | llm
                    res = chain.invoke({"question": user_query})
                    response_text = res.content
                except Exception as e:
                    response_text = f"⚡ AI Recommendations ({primary_use} | {budget_category}):\n\n" \
                                    f"### 🎯 Top Recommended Models\n" \
                                    f"1. **High Performance Pick**: Intel i7 / Ryzen 7, 16GB DDR5 RAM, 512GB NVMe SSD, Dedicated RTX GPU.\n" \
                                    f"2. **Battery & Portability Pick**: Apple MacBook Air (M2/M3) or Asus Zenbook 14.\n\n" \
                                    f"### ⚖️ Checklist\n" \
                                    f"- **RAM:** Minimum 16GB for smooth multitasking.\n" \
                                    f"- **Display:** IPS Anti-glare panel with 300+ nits brightness."
            else:
                response_text = f"### 💻 AI Recommendations for {primary_use}\n\n" \
                                f"**Target Budget:** {budget_category} | **OS:** {preferred_os}\n\n" \
                                f"#### 🎯 Recommended Configurations\n" \
                                f"- **Option A (Performance)**: Lenovo Legion / ASUS TUF (Ryzen 7 7840HS, 16GB RAM, RTX 4050, 512GB SSD).\n" \
                                f"- **Option B (Ultrabook)**: MacBook Air M2 or HP Pavilion Plus 14 (16GB RAM, 512GB SSD).\n\n" \
                                f"#### 🔑 Buying Advice\n" \
                                f"- Prioritize at least **16GB DDR5 RAM** for 2026 apps.\n" \
                                f"- Choose **NVMe SSD** over standard SSDs for faster boot times."

            st.session_state.chat_history.append((user_query, response_text))
            st.markdown(f'<div class="response-card">{response_text}</div>', unsafe_allow_html=True)
        elif st.session_state.chat_history:
            last_q, last_r = st.session_state.chat_history[-1]
            st.markdown(f'<div class="response-card">{last_r}</div>', unsafe_allow_html=True)
        else:
            st.info("👈 Choose a preset chip or write requirements, then click 'Get AI Recommendations'.")

with tab_guide:
    st.markdown("### ⚖️ Laptop Buyer's Specs Guide")
    
    spec_data = {
        "Usage Tier": ["Basic / Student", "Coding & Dev", "Gaming / 3D Render", "4K Video Editing"],
        "Min CPU": ["Core i3 / Ryzen 3", "Core i5 / Ryzen 5", "Core i7 / Ryzen 7", "Core i9 / Apple M3 Pro"],
        "Recommended RAM": ["8GB DDR4", "16GB DDR5", "16GB - 32GB DDR5", "32GB - 64GB Unified"],
        "Storage": ["256GB SSD", "512GB NVMe SSD", "1TB Gen4 SSD", "1TB+ High Speed SSD"],
        "Graphics (GPU)": ["Integrated", "Integrated / Entry GPU", "RTX 4050 / 4060", "RTX 4070 / M3 Max"]
    }
    df_specs = pd.DataFrame(spec_data)
    st.table(df_specs)

with tab_settings:
    st.markdown("### ⚙️ Environment & API Configuration")
    user_api = st.text_input("Groq API Key Override", value=api_key, type="password")
    if user_api:
        st.success("API Key is loaded and ready for LLM queries!")
    else:
        st.info("Operating in intelligent fallback mode.")

st.markdown('</div>', unsafe_allow_html=True)
