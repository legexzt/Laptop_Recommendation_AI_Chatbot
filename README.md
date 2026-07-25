# Laptop Recommendation AI Chatbot

An intelligent conversational AI assistant built with Streamlit and Groq LLM API to guide users in choosing the ideal laptop based on budget, usage requirements (gaming, coding, video editing, daily tasks), brand preference, and specifications.

## 🚀 Features
- **AI-Powered Recommendation**: Powered by Groq Llama-3 / LLM models for fast, contextual responses.
- **Interactive Chat Interface**: Sleek Streamlit chat UI with conversation history.
- **Tailored Buying Advice**: Recommends exact laptop models with CPU, GPU, RAM, and price estimates.

## 📂 Project Structure
```text
├── laptop_chatbot_app.py      # Streamlit AI chatbot application
├── .env.example               # Environment variables template
├── laptop_bg.png              # UI background asset
└── run_laptop_chatbot_app.bat # Windows batch launcher script
```

## 🛠️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/legexzt/Laptop_Recommendation_AI_Chatbot.git
   cd Laptop_Recommendation_AI_Chatbot
   ```

2. **Install dependencies**:
   ```bash
   pip install streamlit groq python-dotenv pillow
   ```

3. **Configure API Key**:
   Create a `.env` file in the project directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. **Run the application**:
   ```bash
   streamlit run laptop_chatbot_app.py
   ```
   Or run `run_laptop_chatbot_app.bat` on Windows.
