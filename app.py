import streamlit as st
import requests
import json

# ==============================
# CONFIG
# ==============================

API_URL = "https://multi-agent-ai-journal.onrender.com/generate-journal-stream"
HEALTH_URL = "https://multi-agent-ai-journal.onrender.com"

st.set_page_config(
    page_title="Academic Journal Generator",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Multi-Agent Academic Journal Generator")
st.caption("Agentic AI + LangGraph Academic Research System")

# ==============================
# BACKEND STATUS
# ==============================

def backend_status():
    try:
        requests.get(HEALTH_URL, timeout=5)
        return True
    except:
        return False


if backend_status():
    st.success("🟢 Backend Online")
else:
    st.warning("🟡 Backend waking up (Render cold start...)")

# ==============================
# INPUT
# ==============================

topic = st.text_input(
    "Enter Academic Topic",
    placeholder="Example: Ozone Layer Recovery"
)

generate = st.button("🚀 Generate Journal")

status_box = st.empty()
journal_box = st.empty()

# ==============================
# STREAM HANDLER
# ==============================

def stream_journal(topic):

    try:
        response = requests.post(
            API_URL,
            json={"topic": topic},
            stream=True,
            timeout=600
        )

        journal_text = ""

        for line in response.iter_lines():

            if not line:
                continue

            decoded = line.decode("utf-8")

            try:
                data = json.loads(decoded)

                # STATUS UPDATE
                if "status" in data:
                    status_box.info(data["status"])

                # FINAL JOURNAL
                if "journal" in data:
                    journal_text = data["journal"]
                    journal_box.markdown(journal_text)

            except Exception:
                pass

        return journal_text

    except Exception as e:
        st.error(f"Connection error: {e}")
        return None


# ==============================
# EXECUTION
# ==============================

if generate:

    if not topic:
        st.warning("Please enter a topic")
    else:
        journal = stream_journal(topic)

        if journal:
            st.download_button(
                "📄 Download Journal",
                journal,
                file_name="academic_journal.txt"
            )