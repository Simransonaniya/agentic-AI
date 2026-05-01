# ⚡ Agentic AI

A production-grade multi-tool autonomous agent built with **Streamlit** and the **Claude API**.

## Features
- 🤖 Autonomous agentic loop with multi-step reasoning
- 🔧 5 built-in tools: Web Search, Calculator, Text Analyzer, Code Runner, Data Formatter
- 💬 Persistent conversation history with step-by-step transparency
- 📊 Real-time agent reasoning visualization
- ⚙️ Configurable: model, temperature, max iterations
- 🎨 Dark futuristic UI with monospace aesthetic

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run locally
```bash
streamlit run app.py
```

### 3. Deploy on Streamlit Cloud
1. Push this folder to a GitHub repo
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set main file as `app.py`
5. Add `GROQ` in secrets (optional — app also accepts key via UI)

## Usage
1. Enter your Anthropic API key in the sidebar
2. Choose model and parameters
3. Type your message and click **Run Agent**
4. Watch the agent reason and use tools in real time!

## Example Prompts
- "Calculate the compound interest on $10,000 at 7% for 20 years"
- "Analyze the sentiment of this text: [paste text]"
- "Search for information about quantum computing and summarize it"
- "Run this Python code: print([x**2 for x in range(10)])"