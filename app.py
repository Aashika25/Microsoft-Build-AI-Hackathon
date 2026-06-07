import streamlit as st
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from crew import run_crew

# ── Page Config ────────────────────────────────────────────
st.set_page_config(
    page_title="OnboardIQ — AI Onboarding Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* Base */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0a0a0f;
    color: #e8e8f0;
}

/* Hide streamlit defaults */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2rem 2rem 2rem; }

/* Hero header */
.hero {
    background: linear-gradient(135deg, #0f0f1a 0%, #1a1030 50%, #0f1a20 100%);
    border: 1px solid rgba(120, 80, 255, 0.2);
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at 30% 40%, rgba(120, 80, 255, 0.08) 0%, transparent 60%),
                radial-gradient(circle at 70% 60%, rgba(0, 200, 180, 0.06) 0%, transparent 60%);
    pointer-events: none;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a78bfa, #34d399, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    line-height: 1.1;
}
.hero-sub {
    font-size: 1rem;
    color: #8888aa;
    margin-top: 0.5rem;
    font-weight: 300;
    letter-spacing: 0.02em;
}
.hero-badge {
    display: inline-block;
    background: rgba(120, 80, 255, 0.15);
    border: 1px solid rgba(120, 80, 255, 0.3);
    color: #a78bfa;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    margin-bottom: 1rem;
}

/* Chat messages */
.msg-user {
    background: linear-gradient(135deg, rgba(120, 80, 255, 0.15), rgba(120, 80, 255, 0.05));
    border: 1px solid rgba(120, 80, 255, 0.25);
    border-radius: 16px 16px 4px 16px;
    padding: 1rem 1.2rem;
    margin: 1rem 0 1rem 3rem;
    color: #e8e8f0;
    font-size: 0.95rem;
}
.msg-bot {
    background: linear-gradient(135deg, rgba(30, 30, 50, 0.8), rgba(20, 30, 40, 0.8));
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 16px 16px 16px 4px;
    padding: 1.2rem 1.5rem;
    margin: 1rem 3rem 1rem 0;
    color: #e8e8f0;
    font-size: 0.95rem;
    line-height: 1.7;
}

/* Agent pipeline */
.pipeline {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin: 0.8rem 0;
}
.agent-badge {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    padding: 0.25rem 0.7rem;
    border-radius: 20px;
    text-transform: uppercase;
}
.agent-router   { background: rgba(251,191,36,0.15); border: 1px solid rgba(251,191,36,0.3); color: #fbbf24; }
.agent-retriever{ background: rgba(52,211,153,0.15); border: 1px solid rgba(52,211,153,0.3); color: #34d399; }
.agent-answer   { background: rgba(96,165,250,0.15); border: 1px solid rgba(96,165,250,0.3); color: #60a5fa; }
.agent-escalate { background: rgba(248,113,113,0.15); border: 1px solid rgba(248,113,113,0.3); color: #f87171; }
.agent-ok       { background: rgba(52,211,153,0.15); border: 1px solid rgba(52,211,153,0.3); color: #34d399; }

/* Confidence bar */
.conf-bar-wrap {
    background: rgba(255,255,255,0.05);
    border-radius: 10px;
    height: 6px;
    margin: 0.3rem 0;
    overflow: hidden;
}
.conf-bar-fill {
    height: 100%;
    border-radius: 10px;
    transition: width 0.6s ease;
}

/* Sources */
.source-chip {
    display: inline-block;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 6px;
    padding: 0.2rem 0.6rem;
    font-size: 0.72rem;
    color: #8888aa;
    margin: 0.2rem 0.2rem 0 0;
    word-break: break-all;
}

/* Escalation box */
.escalation-box {
    background: rgba(248,113,113,0.08);
    border: 1px solid rgba(248,113,113,0.25);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-top: 0.8rem;
    font-size: 0.88rem;
    color: #fca5a5;
}
.escalation-box strong { color: #f87171; }

/* Input area */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    color: #e8e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.8rem 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(120, 80, 255, 0.5) !important;
    box-shadow: 0 0 0 2px rgba(120, 80, 255, 0.1) !important;
}

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.7rem 2rem !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 20px rgba(124, 58, 237, 0.4) !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0d0d18 !important;
    border-right: 1px solid rgba(255,255,255,0.05) !important;
}
.sidebar-section {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 1rem;
}
.sidebar-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #6666aa;
    margin-bottom: 0.8rem;
}
.stat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.4rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    font-size: 0.82rem;
}
.stat-val {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    color: #a78bfa;
}

/* Category pill */
.cat-pill {
    display: inline-block;
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    padding: 0.2rem 0.7rem;
    border-radius: 20px;
    margin-bottom: 0.5rem;
}
.cat-engineering  { background: rgba(96,165,250,0.15); color: #60a5fa; border: 1px solid rgba(96,165,250,0.3); }
.cat-hr           { background: rgba(251,191,36,0.15); color: #fbbf24; border: 1px solid rgba(251,191,36,0.3); }
.cat-communication{ background: rgba(52,211,153,0.15); color: #34d399; border: 1px solid rgba(52,211,153,0.3); }
.cat-operations   { background: rgba(248,113,113,0.15); color: #f87171; border: 1px solid rgba(248,113,113,0.3); }
.cat-general      { background: rgba(167,139,250,0.15); color: #a78bfa; border: 1px solid rgba(167,139,250,0.3); }

/* Divider */
.iq-divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.06);
    margin: 1.5rem 0;
}

/* Suggested questions */
.suggest-btn {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 0.6rem 0.9rem;
    font-size: 0.82rem;
    color: #9999bb;
    cursor: pointer;
    margin-bottom: 0.4rem;
    width: 100%;
    text-align: left;
    transition: all 0.2s;
}
</style>
""", unsafe_allow_html=True)

# ── Session State ──────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "total_queries" not in st.session_state:
    st.session_state.total_queries = 0
if "escalations" not in st.session_state:
    st.session_state.escalations = 0
if "selected_suggestion" not in st.session_state:
    st.session_state.selected_suggestion = ""
if "auto_send" not in st.session_state:
    st.session_state.auto_send = False

# ── Sidebar ────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0 1.5rem 0;'>
        <div style='font-family: Syne, sans-serif; font-size: 1.4rem; font-weight: 800;
                    background: linear-gradient(135deg, #a78bfa, #34d399);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            OnboardIQ
        </div>
        <div style='font-size: 0.72rem; color: #555577; letter-spacing: 0.1em; text-transform: uppercase;'>
            Powered by Phi-4-mini · Pinecone
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Stats
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">Session Stats</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="stat-row"><span>Queries asked</span><span class="stat-val">{st.session_state.total_queries}</span></div>
    <div class="stat-row"><span>Escalations</span><span class="stat-val">{st.session_state.escalations}</span></div>
    <div class="stat-row"><span>Knowledge base</span><span class="stat-val">GitLab</span></div>
    <div class="stat-row" style="border:none"><span>Agents active</span><span class="stat-val">4</span></div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Agent pipeline info
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">Agent Pipeline</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="stat-row"><span>🔀 Router Agent</span><span style="color:#fbbf24; font-size:0.75rem;">Classifies</span></div>
    <div class="stat-row"><span>🔍 Retriever Agent</span><span style="color:#34d399; font-size:0.75rem;">RAG Search</span></div>
    <div class="stat-row"><span>💬 Answer Agent</span><span style="color:#60a5fa; font-size:0.75rem;">Generates</span></div>
    <div class="stat-row" style="border:none"><span>🚨 Escalation Agent</span><span style="color:#f87171; font-size:0.75rem;">Routes</span></div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Suggested questions
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">Try asking...</div>', unsafe_allow_html=True)

    suggestions = [
        "How do I set up my dev environment?",
        "What is the leave policy?",
        "Who do I contact for IT issues?",
        "How does code review work?",
        "What are the communication norms?",
        "How do I request access to tools?"
    ]

    for s in suggestions:
        if st.button(s, key=f"sug_{s}"):
            st.session_state.selected_suggestion = s
            st.session_state.auto_send = True

    st.markdown('</div>', unsafe_allow_html=True)

    # Clear chat
    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.session_state.total_queries = 0
        st.session_state.escalations = 0
        st.rerun()

# ── Hero Header ────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">Multi-Agent AI System</div>
    <div class="hero-title">Your Smart<br>Onboarding Assistant</div>
    <div class="hero-sub">Ask anything about engineering setup, HR policies, operations, communication norms, or who to reach out to.</div>
</div>
""", unsafe_allow_html=True)

# ── Chat History ───────────────────────────────────────────
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="msg-user">🧑 &nbsp; {msg["content"]}</div>', unsafe_allow_html=True)
    else:
        data = msg["data"]
        category = data.get("category", "general")
        confidence = data.get("confidence", 0)
        conf_pct = int(confidence * 100)
        conf_color = "#34d399" if conf_pct >= 75 else "#fbbf24" if conf_pct >= 50 else "#f87171"

        # Sources
        sources_html = "".join([f'<span class="source-chip">🔗 {s}</span>' for s in data.get("sources", [])])

        # Escalation
        escalation = data.get("escalation", {})
        escalation_html = ""
        if escalation.get("needs_escalation"):
            contact = escalation.get("contact", {})
            escalation_html = f"""
            <div class="escalation-box">
                ⚠️ <strong>Low confidence — escalating to human</strong><br>
                Reach out to <strong>{contact.get('team', 'your team')}</strong>
                via {contact.get('channel', 'Slack')} or {contact.get('email', '')}
            </div>"""

        st.markdown(f"""
        <div class="msg-bot">
            <div class="pipeline">
                <span class="agent-badge agent-router">🔀 Router: {category}</span>
                <span class="agent-badge agent-retriever">🔍 Retriever: {len(data.get('sources', []))} sources</span>
                <span class="agent-badge agent-answer">💬 Answer Agent</span>
                <span class="agent-badge {'agent-escalate' if escalation.get('needs_escalation') else 'agent-ok'}">
                    🚨 Escalation: {'Yes' if escalation.get('needs_escalation') else 'No'}
                </span>
            </div>
            <hr class="iq-divider">
            <span class="cat-pill cat-{category}">{category}</span>
            <div style="margin: 0.5rem 0 1rem 0; line-height: 1.8;">
                {data.get('answer', '').replace(chr(10), '<br>')}
            </div>
            <div style="margin-bottom: 0.5rem;">
                <div style="font-size: 0.75rem; color: #6666aa; margin-bottom: 0.3rem;">
                    Confidence: {conf_pct}%
                </div>
                <div class="conf-bar-wrap">
                    <div class="conf-bar-fill" style="width:{conf_pct}%; background:{conf_color};"></div>
                </div>
            </div>
            <div style="margin-top: 0.8rem;">
                <div style="font-size: 0.72rem; color: #6666aa; margin-bottom: 0.3rem;">Sources</div>
                {sources_html}
            </div>
            {escalation_html}
        </div>
        """, unsafe_allow_html=True)

# ── Input Area ─────────────────────────────────────────────
st.markdown("<div style='height: 1.5rem'></div>", unsafe_allow_html=True)

col1, col2 = st.columns([5, 1])

with col1:
    default_val = st.session_state.selected_suggestion
    user_input = st.text_input(
        label="",
        value=default_val,
        placeholder="Ask anything — dev setup, leave policy, who to contact...",
        key="user_input",
        label_visibility="collapsed"
    )

with col2:
    send = st.button("Ask →")

# Auto send from suggestion click
if st.session_state.auto_send and st.session_state.selected_suggestion:
    query = st.session_state.selected_suggestion
    st.session_state.auto_send = False
    st.session_state.selected_suggestion = ""
    st.session_state.messages.append({"role": "user", "content": query})
    st.session_state.total_queries += 1

    with st.spinner("🤖 Agents working..."):
        start = time.time()
        result = run_crew(query)
        elapsed = time.time() - start

    if result.get("escalation", {}).get("needs_escalation"):
        st.session_state.escalations += 1

    st.session_state.messages.append({
        "role": "assistant",
        "content": result.get("answer", ""),
        "data": result
    })
    st.rerun()

# Manual send
if send and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.total_queries += 1

    with st.spinner("🤖 Agents working..."):
        start = time.time()
        result = run_crew(user_input)
        elapsed = time.time() - start

    if result.get("escalation", {}).get("needs_escalation"):
        st.session_state.escalations += 1

    st.session_state.messages.append({
        "role": "assistant",
        "content": result.get("answer", ""),
        "data": result
    })
    st.rerun()