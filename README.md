# METU IE Summer Practice Chatbot

IE 304 – Project 1 | Intelligent Chatbot Application

## Setup & Local Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Add your Anthropic API key to .streamlit/secrets.toml
#    ANTHROPIC_API_KEY = "sk-ant-..."

# 3. Run the app
streamlit run app.py
```

## Deploying to Streamlit Community Cloud

1. Push this repository to GitHub.
2. Go to https://share.streamlit.io and click **New app**.
3. Select your repo, branch (`main`), and set `app.py` as the main file.
4. Under **Advanced settings → Secrets**, add:
   ```
   ANTHROPIC_API_KEY = "sk-ant-your-key-here"
   ```
5. Click **Deploy**. Your app will be live at a public URL.

## Project Structure

```
metu_ie_chatbot/
├── app.py              # Streamlit UI + Claude API integration
├── knowledge_base.py   # Curated KB + system prompt
├── requirements.txt    # Python dependencies
├── documentation.md    # Project report (System Architecture, Testing Guide, User Instructions)
└── .streamlit/
    └── secrets.toml    # API key (local only, do NOT commit)
```

## Features
- Real-time streaming responses
- Full conversation history
- Sidebar quick-question shortcuts
- Bilingual support (English & Turkish)
- Out-of-scope query handling
- METU blue-themed UI
