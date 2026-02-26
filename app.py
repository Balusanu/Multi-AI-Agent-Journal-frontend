import streamlit as st
import requests
import json

# =========================
# CONFIG
# =========================

BACKEND_URL = "https://multi-agent-ai-journal.onrender.com/generate"
HEALTH_URL = "https://multi-agent-ai-journal.onrender.com/"

st.set_page_config(
    page_title="Academic Journal Generator",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Multi-Agent Academic Journal Generator")
st.caption("Agentic AI + LangGraph Academic Research System")

# =========================
# SESSION STATE
# =========================

if "running" not in st.session_state:
    st.session_state.running = False

if "journal" not in st.session_state:
    st.session_state.journal = ""

# =========================
# BACKEND STATUS
# =========================

def backend_alive():
    try:
        r = requests.get(HEALTH_URL, timeout=5)
        return r.status_code == 200
    except:
        return False


if backend_alive():
    st.success("🟢 Backend Online")
else:
    st.warning("🟡 Backend waking up (Render cold start...)")

# =========================
# INPUT
# =========================

topic = st.text_input(
    "Enter Academic Topic",
    placeholder="Example: Impact of Generative AI in Education"
)

generate = st.button(
    "🚀 Generate Journal",
    disabled=st.session_state.running
)

status_box = st.empty()
output_box = st.empty()

# =========================
# STREAM EXECUTION
# =========================

def generate_journal(topic):

    st.session_state.running = True
    st.session_state.journal = ""

    try:
        response = requests.post(
            BACKEND_URL,
            json={"topic": topic},
            stream=True,
            timeout=600
        )

        for line in response.iter_lines():

            if not line:
                continue

            try:
                data = json.loads(line.decode())

                if "status" in data:
                    status_box.info(data["status"])

                if "journal" in data:
                    st.session_state.journal = data["journal"]
                    output_box.markdown(
                        st.session_state.journal
                    )

            except:
                pass

    except Exception as e:
        status_box.error(f"Error: {e}")

    st.session_state.running = False


# =========================
# RUN
# =========================

if generate and topic:
    generate_journal(topic)

elif generate:
    st.warning("Please enter a topic.")

# =========================
# DOWNLOAD
# =========================

if st.session_state.journal:
    st.download_button(
        "📄 Download Journal",
        st.session_state.journal,
        file_name="academic_journal.txt"
    )