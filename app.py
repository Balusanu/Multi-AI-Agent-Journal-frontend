import streamlit as st
import requests
import json
import time

# ==============================
# CONFIG
# ==============================

BACKEND_URL = "https://multi-agent-ai-journal.onrender.com/generate"

st.set_page_config(
    page_title="AI Academic Journal Generator",
    page_icon="📚",
    layout="wide"
)

# ==============================
# HEADER
# ==============================

st.title("📚 Multi-Agent Academic Journal Generator")
st.markdown(
    "Generate structured academic journals using **Agentic AI + LangGraph**"
)

# ==============================
# BACKEND HEALTH CHECK
# ==============================

def check_backend():
    try:
        r = requests.get(
            "https://multi-agent-ai-journal.onrender.com/",
            timeout=10
        )
        if r.status_code == 200:
            return True
    except:
        return False


if check_backend():
    st.success("🟢 Backend Connected")
else:
    st.warning("🟡 Backend waking up (Render cold start)...")

# ==============================
# INPUT
# ==============================

topic = st.text_input(
    "Enter Academic Topic",
    placeholder="Example: Impact of Generative AI in Higher Education"
)

generate_btn = st.button("🚀 Generate Journal")

# ==============================
# STREAMING FUNCTION
# ==============================

def stream_journal(topic):
    try:
        response = requests.post(
            BACKEND_URL,
            json={"topic": topic},
            stream=True,
            timeout=300  # important for Render
        )

        status_placeholder = st.empty()
        journal_placeholder = st.empty()

        final_journal = ""

        for line in response.iter_lines():

            if line:
                decoded = line.decode("utf-8")

                try:
                    data = json.loads(decoded)

                    # Agent status updates
                    if "status" in data:
                        status_placeholder.info(data["status"])

                    # Final journal output
                    if "journal" in data:
                        final_journal = data["journal"]
                        journal_placeholder.markdown(final_journal)

                except json.JSONDecodeError:
                    continue

        return final_journal

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return None


# ==============================
# GENERATE
# ==============================

if generate_btn and topic:

    with st.spinner("Multi-agent system generating journal..."):
        journal_text = stream_journal(topic)

    if journal_text:
        st.success("✅ Journal Generated Successfully")

        # ==============================
        # DOWNLOAD OPTION
        # ==============================
        st.download_button(
            label="📄 Download Journal",
            data=journal_text,
            file_name="academic_journal.txt",
            mime="text/plain"
        )

elif generate_btn:
    st.warning("Please enter a topic.")