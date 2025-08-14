import streamlit as st
import requests

# Streamlit frontend for Customer Support RAG System
st.set_page_config(page_title="Customer Support RAG Chatbot", layout="centered")
st.title("Customer Support RAG Chatbot")

if "history" not in st.session_state:
    st.session_state["history"] = []
if "chat_log" not in st.session_state:
    st.session_state["chat_log"] = []


with st.form("chat_form"):
    user_name = st.text_input("Your Name", "Customer")
    category = st.selectbox("Issue Category", ["General", "Account", "Billing", "Technical", "Subscription"])
    urgency = st.selectbox("Urgency", ["Normal", "High"])
    user_input = st.text_input("Type your message:", "")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    st.session_state["history"].append(user_input)
    payload = {
        "message": user_input,
        "history": st.session_state["history"],
        "user_name": user_name,
        "category": category,
        "urgency": urgency
    }
    try:
        resp = requests.post("http://localhost:8000/rag", json=payload)
        data = resp.json()
        # Add to chat log (no GIF)
        st.session_state["chat_log"].append({
            "user": user_name,
            "message": user_input,
            "support": data["response"],
            "sentiment": data["sentiment"],
            "escalation": data["escalation"],
            "tone": data["tone"],
            "articles": data["articles"]
        })
    except Exception as e:
        st.error(f"Error: {e}")

# Display chat history


# Professional chat bubbles, no GIFs

# Improved contrast for chat bubbles
for i, entry in enumerate(st.session_state["chat_log"]):
    st.markdown(f"<div style='background-color:#e3f2fd;color:#222;padding:12px;border-radius:10px;margin-bottom:4px;border:1px solid #90caf9'><b>{entry['user']}:</b> {entry['message']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='background-color:#fffde7;color:#222;padding:12px;border-radius:10px;margin-bottom:12px;border:1px solid #ffe082'><b>Support:</b> {entry['support']}</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='background-color:#f0f4c3;padding:10px;border-radius:8px;margin-bottom:8px;border:1px solid #dce775;display:flex;align-items:center;gap:16px;'>
        <div style='font-size:15px;color:#333'><b>Sentiment:</b> <span style='color:#1976d2'>{entry['sentiment'].capitalize()}</span></div>
        <div style='font-size:15px;color:#333'><b>Escalation:</b> <span style='color:#d32f2f'>{str(entry['escalation']).capitalize()}</span></div>
        <div style='font-size:15px;color:#333'><b>Tone:</b> <span style='color:#388e3c'>{entry['tone'].capitalize()}</span></div>
    </div>
    """, unsafe_allow_html=True)
    if entry["articles"]:
        st.markdown("<div style='font-size:13px;color:#333'><b>Relevant Articles:</b></div>", unsafe_allow_html=True)
        for a in entry["articles"]:
            st.markdown(f"<div style='font-size:13px;color:#333'>- <b>{a['title']}</b>: {a['content']}</div>", unsafe_allow_html=True)
