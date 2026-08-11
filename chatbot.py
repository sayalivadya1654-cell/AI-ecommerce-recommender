import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# setup
load_dotenv(override=True)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

st.set_page_config(page_title="E-Commerce Recommender + AI Chat", page_icon="🛍️", layout="wide")

st.title("🛍️ E-Commerce Recommendation App")
st.markdown("Find products based on your preferences, or ask our AI shopping assistant directly.")

# Two tabs: your original form-based recommender, and the new LLM chatbot
tab1, tab2 = st.tabs(["🔮 Preference-Based Recommender", "💬 AI Shopping Chatbot"])

# ----------------------------------------------------------------------------
# TAB 1 — YOUR ORIGINAL RECOMMENDER UI (unchanged logic)
# ----------------------------------------------------------------------------
with tab1:
    st.subheader("👤 Customer Details")
    name = st.text_input("Enter Your Name")
    age = st.number_input("Enter Your Age", min_value=10, max_value=100, value=20)
    city = st.selectbox(
        "Select Your City",
        ["Pune", "Mumbai", "Nagpur", "Wardha", "Delhi", "Bangalore"]
    )

    st.subheader("🛒 Shopping Preferences")
    category = st.selectbox(
        "Select Product Category",
        ["Clothing", "Footwear", "Beauty", "Electronics", "Accessories"]
    )
    brand = st.selectbox(
        "Select Preferred Brand",
        ["Any Brand", "Nike", "Puma", "Adidas", "Levis", "Samsung"]
    )
    price = st.slider("Select Maximum Price (₹)", min_value=100, max_value=100000, value=5000, step=100)
    rating = st.slider("Select Minimum Rating", min_value=1, max_value=5, value=3)

    st.subheader("💳 Preferences")
    payment = st.radio("Select Payment Mode", ["UPI", "Credit Card", "Debit Card", "Cash on Delivery"])
    discount = st.checkbox("Show only discounted products")

    st.subheader("🔮 Get Recommendations")
    if st.button("🔮 Recommend Products"):
        st.success("✅ Recommendations generated!")
        st.subheader("📦 Recommended Products")

        st.write("👟 Sports Shoes")
        st.write("⭐ Rating: 4.5")
        st.write("💰 Price: ₹2,499")

        st.write("👕 Casual T-Shirt")
        st.write("⭐ Rating: 4.3")
        st.write("💰 Price: ₹999")

        st.write("🎒 Backpack")
        st.write("⭐ Rating: 4.2")
        st.write("💰 Price: ₹1,499")

# ----------------------------------------------------------------------------
# TAB 2 — LLM SHOPPING CHATBOT (Groq + LangChain, from your notebook logic)
# ----------------------------------------------------------------------------
with tab2:
    st.subheader("💬 Ask Our AI Shopping Assistant")
    st.caption("Example: \"Suggest Nike T-shirts under ₹2000\" or \"Recommend winter outfits for women.\"")

    if not GROQ_API_KEY:
        st.error(
            "⚠️ No GROQ_API_KEY found. Create a `.env` file in this project folder with:\n\n"
            "`GROQ_API_KEY=your_key_here`\n\n"
            "Get a free key at https://console.groq.com/keys"
        )
    else:
        # Cache the LLM + chain so it's only built once per session, not on every rerun
        @st.cache_resource
        def get_shopping_chain():
            llm = ChatGroq(
                model="llama-3.3-70b-versatile",
                api_key=GROQ_API_KEY,
            )

            shopping_prompt = ChatPromptTemplate.from_messages([
                (
                    "system",
                    """
You are an AI Shopping & Fashion Assistant.

Rules:
- Answer ONLY shopping and fashion related questions.
- Extract the brand, category and budget from the user's question automatically.
- If any detail is missing, make a reasonable assumption or politely ask for clarification.
- ALWAYS use Indian Rupees (₹) for every price. Never use $ or any other currency symbol, even in ranges.
- Recommend exactly 2 specific products that match the request.
- For EACH product, output a separate markdown block in this EXACT format, with no extra text before or after:

**[Product Name]**
- 💰 **Price :** ₹[amount or range]
- 🎨 **Colors :** [colors]
- 🧵 **Material :** [material]
- ✨ **Features :** [2-3 short features]
- 👟 **Best for :** [use case]
- ✅ **Why pick this :** [one short sentence]

- Leave a blank line between the two products.
- Keep every value short (a few words), never a full sentence, except "Why pick this."
- Never write long paragraphs, greetings, or sign-offs — output only the two formatted product blocks.
"""
                ),
                ("human", "{question}")
            ])

            # In-memory per-session chat history (resets when the app restarts)
            history_store = {}

            def get_history(session_id: str):
                if session_id not in history_store:
                    history_store[session_id] = InMemoryChatMessageHistory()
                return history_store[session_id]

            chain = RunnableWithMessageHistory(
                shopping_prompt | llm,
                get_history,
                input_messages_key="question",
                history_messages_key="history",
            )
            return chain

        shopping_chain = get_shopping_chain()

        # Give each browser session its own chat id and message log
        if "session_id" not in st.session_state:
            st.session_state.session_id = f"user-{os.urandom(4).hex()}"
        if "chat_messages" not in st.session_state:
            st.session_state.chat_messages = []

        # Render past messages
        for msg in st.session_state.chat_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Chat input
        user_input = st.chat_input("Ask about products, brands, or styles...")
        if user_input:
            st.session_state.chat_messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = shopping_chain.invoke(
                        {"question": user_input},
                        config={"configurable": {"session_id": st.session_state.session_id}},
                    )
                st.markdown(response.content)

            st.session_state.chat_messages.append({"role": "assistant", "content": response.content})

        if st.session_state.chat_messages:
            if st.button("🗑️ Clear Chat"):
                st.session_state.chat_messages = []
                st.rerun()
