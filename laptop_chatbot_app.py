import streamlit as st
import os
import base64
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)

try:
    st.set_page_config(
        page_title="Laptop Recommendation AI Chatbot",
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
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

bg_base64 = get_base64_bg(bg_path)

st.markdown(f"""
<style>
    .stApp {{
        background-image: linear-gradient(rgba(15, 23, 42, 0.85), rgba(15, 23, 42, 0.85)), url("data:image/png;base64,{bg_base64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .main-panel {{
        background: rgba(30, 41, 59, 0.75);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border-radius: 16px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
        animation: fadeIn 1s ease-out;
    }}
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    .title-text {{
        font-family: 'Outfit', 'Inter', sans-serif;
        font-size: 2.6rem;
        font-weight: 800;
        background: linear-gradient(135deg, #60A5FA 0%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }}
    [data-testid="stMain"] p, 
    [data-testid="stMain"] h1, 
    [data-testid="stMain"] h2, 
    [data-testid="stMain"] h3, 
    [data-testid="stMain"] h4, 
    [data-testid="stMain"] h5, 
    [data-testid="stMain"] h6, 
    [data-testid="stMain"] span, 
    [data-testid="stMain"] label, 
    [data-testid="stMain"] li,
    [data-testid="stMain"] div[data-testid="stMarkdownContainer"] *,
    .stMainBlockContainer *,
    section.stMain * {{
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
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] h4, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] .stMarkdown {{
        color: #0F172A !important;
    }}
    .response-card {{
        background-color: rgba(30, 41, 59, 0.6);
        border-radius: 12px;
        padding: 24px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-top: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
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
st.write("Day 3 E-Commerce AI Chatbot Application")
st.write("---")

st.sidebar.subheader("Laptop Finder Filters")

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

api_key = os.getenv("GROQ_API_KEY", "")
user_api_key = st.sidebar.text_input("Groq API Key (Optional)", value=api_key, type="password")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

col_left, col_right = st.columns([1.2, 0.8], gap="large")

with col_left:
    st.subheader("Describe Your Laptop Requirements")
    
    default_prompt = f"I am looking for a laptop for {primary_use} in the budget range of {budget_category} with OS: {preferred_os}."
    user_query = st.text_area("Specify specs or preferences:", value=default_prompt, height=130)
    
    c1, c2 = st.columns([1, 1])
    with c1:
        submit_btn = st.button("Get AI Recommendations", type="primary", use_container_width=True)
    with c2:
        clear_btn = st.button("Reset Chat", use_container_width=True)
        
    if clear_btn:
        st.session_state.chat_history = []
        st.rerun()

with col_right:
    st.subheader("AI Laptop Recommendations")
    
    if submit_btn and user_query.strip():
        actual_key = user_api_key or api_key
        response_text = ""
        
        if actual_key:
            try:
                from langchain_groq import ChatGroq
                from langchain_core.prompts import ChatPromptTemplate
                
                llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.3, api_key=actual_key)
                prompt = ChatPromptTemplate.from_template("""
                You are a senior hardware expert specializing in laptop recommendations.
                User Request: {question}

                Format your recommendations into:
                1. Top Recommended Laptop Models (with specs: Processor, RAM, SSD, GPU, Display)
                2. Key Pros & Cons for Each Model
                3. Essential Buyers Checklist
                4. Value for Money Analysis
                """)
                chain = prompt | llm
                res = chain.invoke({"question": user_query})
                response_text = res.content
            except Exception as e:
                response_text = f"API Error: {str(e)}\n\nFallback Recommendations for {primary_use} ({budget_category}):\n\n" \
                                f"### 1. Top Recommended Laptop Models\n" \
                                f"- **Option A (Best Performance)**: Intel i5/i7 or Ryzen 5/7, 16GB RAM, 512GB NVMe SSD, Dedicated GPU.\n" \
                                f"- **Option B (Best Portability & Battery)**: Apple MacBook Air M2 / M3 or Ultra-slim Ultrabook.\n\n" \
                                f"### 2. Key Specifications Checklist\n" \
                                f"- **Processor:** Minimum 6 cores / 12 threads.\n" \
                                f"- **RAM:** 16GB DDR5.\n" \
                                f"- **Display:** 100% sRGB IPS Panel."
        else:
            response_text = f"### 💻 AI Laptop Recommendations ({primary_use})\n\n" \
                            f"**Budget Category:** {budget_category} | **OS:** {preferred_os}\n\n" \
                            f"#### 1. Recommended Configurations\n" \
                            f"- **High Performance Laptop:** Intel Core i7-13700H / AMD Ryzen 7 7840HS, 16GB DDR5 RAM, 512GB SSD, RTX 4050 / 4060 GPU.\n" \
                            f"- **Slim Ultrabook:** Apple MacBook Air M2 or Asus Zenbook 14, 16GB RAM, 512GB SSD, 14-hour Battery Life.\n\n" \
                            f"#### 2. Key Buying Advice\n" \
                            f"- Ensure at least **16GB RAM** for future-proofing.\n" \
                            f"- Prefer **NVMe Gen4 SSD** for fast boot times and app loading."

        st.session_state.chat_history.append((user_query, response_text))
        st.markdown(f'<div class="response-card">{response_text}</div>', unsafe_allow_html=True)
    elif submit_btn:
        st.warning("Please enter your requirements.")
    elif st.session_state.chat_history:
        last_q, last_r = st.session_state.chat_history[-1]
        st.markdown(f'<div class="response-card">{last_r}</div>', unsafe_allow_html=True)
    else:
        st.info("Laptop recommendations will appear here.")

if st.session_state.chat_history:
    st.write("---")
    st.subheader("Recommendation History")
    for q, r in reversed(st.session_state.chat_history):
        with st.expander(f"Query: {q[:70]}..."):
            st.write(r)

st.markdown('</div>', unsafe_allow_html=True)
