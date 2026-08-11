# 🛍️ E-Commerce Recommendation App + AI Shopping Chatbot

Built by me as a personal project combining a Streamlit UI with an LLM-powered shopping assistant.

## What it does
- **Preference-Based Recommender** — pick your category, brand, budget, and rating to get product suggestions.
- **AI Shopping Chatbot** — powered by Groq's Llama 3.3 70B via LangChain, ask natural-language shopping questions (e.g. "Suggest Nike T-shirts under ₹2000") and get structured, bullet-point recommendations with memory of the conversation.

## Tech stack
- Streamlit (UI)
- LangChain + langchain-groq (LLM orchestration)
- Groq API (Llama 3.3 70B Versatile)
- python-dotenv (secrets management)

## Setup
1. Clone this repo and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and add your own Groq API key:
   ```bash
   cp .env.example .env
   ```
   Get a free key at https://console.groq.com/keys
3. Run the app:
   ```bash
   streamlit run app.py
   ```

## Notes
- Chat history is stored in memory per session and resets when the app restarts.
- Never commit your real `.env` file — it's already excluded via `.gitignore`.
