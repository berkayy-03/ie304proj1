# IE 304 Project 1 – METU IE Summer Practice Chatbot
## Project Documentation Report

---

### System Architecture

The chatbot is built using a **Retrieval-Augmented Generation (RAG)-inspired** architecture with three core layers:

**1. Knowledge Base (`knowledge_base.py`)**  
A structured, hand-curated knowledge base derived from the official METU IE Summer Practice website (https://sp-ie.metu.edu.tr/en) covering all IE 300/400 rules, SGK insurance procedures, required documents, company opportunities, and a custom FAQ dataset. It is embedded directly into a system prompt to ensure fast, reliable, and hallucination-resistant answers without requiring a vector database.

**2. LLM Integration – Anthropic Claude API**  
The application uses the `claude-sonnet-4-20250514` model via the Anthropic Python SDK. Each user message is sent to the API along with the full conversation history and a system prompt containing the entire knowledge base. Responses are streamed token-by-token for a real-time typing effect.

**3. Frontend – Streamlit**  
The UI is built with Streamlit, providing a chat interface with custom CSS styling (METU blue color scheme), a sidebar with quick-question buttons and official links, and a message history panel. The app is fully hosted on Streamlit Community Cloud.

**Architecture Diagram:**
```
User Input
    │
    ▼
Streamlit UI (app.py)
    │  (full conversation history)
    ▼
Anthropic Claude API
    │  (system prompt = knowledge_base.py)
    ▼
Streamed Response → Displayed in Chat
```

---

### Testing Guide

Use the following sample queries to evaluate the chatbot's accuracy:

| # | Sample Query | Expected Behavior |
|---|---|---|
| 1 | *"What are the prerequisites for IE 300?"* | Lists IE 102, IE 251, IE 265, IE 241, OHS 101 + one of IE 266/252 with DD or above |
| 2 | *"Can I do my IE 300 practice at a hospital?"* | No — hospitals are service industries, not accepted for IE 300 |
| 3 | *"When should I apply for SGK insurance?"* | 2-3 weeks before start; at least 1 full week safety margin |
| 4 | *"What is the report submission deadline?"* | October 24, 2025; soft copy on ODTUClass, hard copy to Secretary Room 128 |
| 5 | *"Which companies offer paid IE 400 internships in Ankara?"* | Lists Ankara-based companies with Wage: Yes (e.g. MS Spektral, MTM Makina, Başöz Enerji, Europower Enerji) |

---

### User Instructions

**Accessing the Live Application:**

1. Open your web browser and navigate to the hosted Streamlit URL (provided in submission).
2. No login or installation is required.

**Using the Chatbot:**

1. Type your question in the text box at the bottom of the page and press **Enter**.
2. Alternatively, click any **Quick Question** button in the left sidebar to ask a common question instantly.
3. The assistant will stream a response in real time.
4. To start a new conversation, click the **🗑️ Clear Chat** button in the sidebar.

**Tips:**
- You can ask in both **English** and **Turkish**.
- For very specific or time-sensitive information, always cross-check with the official website or email ie-staj@metu.edu.tr.
- The chatbot will politely decline questions unrelated to METU IE Summer Practice.

---

*IE 304 – Project 1 | METU Industrial Engineering Department*
