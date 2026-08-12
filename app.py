import streamlit as st
import time
import os
from dotenv import load_dotenv
from openai import OpenAI

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Responsible AI Chatbot Project",
    page_icon="🤖",
    layout="centered"
)

# =========================================================
# LOAD API KEY
# =========================================================

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

# =========================================================
# CHECK API KEY
# =========================================================

if not API_KEY:
    st.error("❌ OpenRouter API key not found.")
    st.info(
        "Create a .env file in the same folder as app.py "
        "and add: OPENROUTER_API_KEY=your_key"
    )
    st.stop()

# =========================================================
# OPENROUTER CLIENT
# =========================================================

client = OpenAI(
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

MODEL = "openai/gpt-4o-mini"

# =========================================================
# BASIC SAFETY CHECK
# =========================================================

def is_safe(prompt):

    unsafe_words = [
        "kill myself",
        "suicide",
        "self harm",
        "hurt myself",
        "make a bomb",
        "build a bomb",
        "hack someone's account",
        "steal password"
    ]

    prompt_lower = prompt.lower()

    for word in unsafe_words:
        if word in prompt_lower:
            return False

    return True


# =========================================================
# RESPONSE EVALUATION
# =========================================================

def evaluate_response(response):

    if not response:
        return "❌ No Response"

    if response.startswith("❌"):
        return "❌ Error"

    if len(response.strip()) < 20:
        return "⚠️ Short Response"

    return "✅ Good Response"


# =========================================================
# LOGGING
# =========================================================

def log_interaction(user_input, response, quality, elapsed):

    with open("chat_log.txt", "a", encoding="utf-8") as file:

        file.write(
            "\n----------------------------------------\n"
        )

        file.write(
            f"User: {user_input}\n"
        )

        file.write(
            f"AI: {response}\n"
        )

        file.write(
            f"Quality: {quality}\n"
        )

        file.write(
            f"Response Time: {elapsed:.2f} seconds\n"
        )


# =========================================================
# AI MODEL FUNCTION
# =========================================================

def query_model(messages):

    response = client.chat.completions.create(

        model=MODEL,

        messages=messages,

        temperature=0.7,

        max_tokens=500
    )

    return response.choices[0].message.content


# =========================================================
# CUSTOM UI
# =========================================================

# =========================================================
# CUSTOM UI - BACKGROUND COLOR AND DESIGN
# =========================================================

st.markdown("""
<style>

    /* Main application background */
    .stApp {
        background-color: liteblue;
    }

    /* Main content area */
    .main {
        background-color: lavender;
    }
    .st.markdown{
        background-color: lavender;
    }

    /* Title */
    .title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        color: #123B63;
        margin-bottom: 5px;
    }

    /* Subtitle */
    .subtitle {
        text-align: center;
        color: #4A6175;
        font-size: 17px;
        margin-bottom: 25px;
    }

    /* Information box */
    .info {
        padding: 15px;
        border-radius: 12px;
        background-color: #D6EBFF;
        border: 1px solid #B8D9F5;
        margin-bottom: 20px;
        text-align: center;
        color: #123B63;
        font-weight: 500;
    }

    /* Sidebar background */
    section[data-testid="stSidebar"] {
        background-color: gray;
    }

    /* Sidebar text */
    section[data-testid="stSidebar"] * {
        color: black;
    }

    /* Chat input */
    .stChatInput {
        background-color: black;
    }

    /* Buttons */
    .stButton > button {
        background-color: lavender;
        color: black;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
    }

    .stButton > button:hover {
        background-color: black;
        color: lightblue;
    }
    

</style>
""", unsafe_allow_html=True)



# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="title">🤖 Responsible AI Chatbot Project</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'A safe, responsible and intelligent AI assistant'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="info">
    🛡️ Safe &nbsp;&nbsp;|&nbsp;&nbsp;
    🤖 AI Powered &nbsp;&nbsp;|&nbsp;&nbsp;
    ⭐ Evaluated &nbsp;&nbsp;|&nbsp;&nbsp;
    📝 Logged
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "system",
            "content": """
            You are Responsible AI Chatbot.

            You are a helpful, respectful, safe and responsible
            AI assistant.

            Answer questions clearly and accurately.
            If you do not know something, say so instead of
            making up information.

            Do not provide dangerous instructions or help
            someone harm themselves or others.
            """
        }
    ]


# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    if message["role"] == "user":

        with st.chat_message("user"):
            st.write(message["content"])

    elif message["role"] == "assistant":

        with st.chat_message("assistant"):
            st.write(message["content"])


# =========================================================
# USER INPUT
# =========================================================

user_input = st.chat_input(
    "💬 Ask Responsible AI Chatbot anything..."
)


# =========================================================
# PROCESS USER QUESTION
# =========================================================

if user_input:

    # ---------------------------------------------
    # Display user message
    # ---------------------------------------------

    with st.chat_message("user"):
        st.write(user_input)

    # ---------------------------------------------
    # Safety check
    # ---------------------------------------------

    if not is_safe(user_input):

        response = (
            "I’m sorry, but I can’t help with that request. "
            "I can help with safe and constructive alternatives."
        )

        quality = "🛡️ Safety Protected"
        elapsed = 0.0

        with st.chat_message("assistant"):
            st.warning(response)

        log_interaction(
            user_input,
            response,
            quality,
            elapsed
        )

    else:

        # -----------------------------------------
        # Add user message
        # -----------------------------------------

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        # -----------------------------------------
        # Generate AI response
        # -----------------------------------------

        start_time = time.time()

        with st.chat_message("assistant"):

            with st.spinner("🤖 Responsible AI is thinking..."):

                try:

                    response = query_model(
                        st.session_state.messages
                    )

                    st.write(response)

                except Exception as e:

                    response = (
                        "❌ Sorry, I couldn't connect to the AI service."
                    )

                    st.error(response)

                    st.code(str(e))

        end_time = time.time()

        elapsed = end_time - start_time

        # -----------------------------------------
        # Evaluate response
        # -----------------------------------------

        quality = evaluate_response(response)

        # -----------------------------------------
        # Save AI response
        # -----------------------------------------

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )

        # -----------------------------------------
        # Log interaction
        # -----------------------------------------

        log_interaction(
            user_input,
            response,
            quality,
            elapsed
        )


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🤖 Responsible AI")

    st.write(
        "Welcome to the Responsible AI Chatbot."
    )

    st.divider()

    st.subheader("✨ Features")

    st.write("🤖 AI Conversation")
    st.write("💬 Chat History")
    st.write("🛡️ Safety Protection")
    st.write("⭐ Response Evaluation")
    st.write("📝 Interaction Logging")
    st.write("⏱️ Response Time")

    st.divider()

    st.subheader("⚙️ Model")

    st.write(MODEL)

    st.divider()

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = [
            {
                "role": "system",
                "content": """
                You are Responsible AI Chatbot.
                Be helpful, safe, respectful and responsible.
                """
            }
        ]

        st.rerun()

    st.divider()

    st.caption(
        "Responsible AI Chatbot"
    )

    st.caption(
        "Powered by Streamlit + OpenRouter"
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🛡️ Responsible AI • 🤖 AI Powered • ⭐ Evaluated • 📝 Logged"
)