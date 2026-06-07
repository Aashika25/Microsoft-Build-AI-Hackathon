# 🧠 OnBoardIQ — AI-Powered Employee Onboarding Assistant

> Microsoft AI Build Hackathon 2026 Submission  
> 🚀 Live Demo: [huggingface.co/spaces/Aashika25/OnBoardIQ](https://huggingface.co/spaces/Aashika25/OnBoardIQ)

---

## 📌 Project Description

### Problem
Every new employee faces the same overwhelming first week:
- Knowledge is scattered across wikis, handbooks, and Slack channels
- HR and engineering teams spend 30% of their time answering repetitive onboarding questions
- No single place to ask "who do I contact for X?" or "how do I set up my dev environment?"

### Solution
**OnBoardIQ** is a multi-agent AI onboarding assistant that answers any employee question instantly — grounded in your company's actual documentation.

### Key Features
- 🔀 **Intelligent Routing** — classifies questions by domain (engineering, HR, operations, communication)
- 🔍 **RAG Pipeline** — retrieves answers from real company documentation
- 📊 **Confidence Scoring** — color-coded confidence bar on every answer
- 🚨 **Smart Escalation** — routes to the right human when confidence < 75%
- 👁 **Agent Transparency** — users see exactly which agents processed their query
- 💬 **Suggested Questions** — pre-built templates guide new employees

---

## ⚙️ Setup Instructions

### Prerequisites
- Python 3.10+
- GitHub account (for GitHub Models API)
- Pinecone account (free tier)

### 1. Clone the repository
```bash
git clone https://github.com/Aashika25/Microsoft-Build-AI-Hackathon.git
cd Microsoft-Build-AI-Hackathon
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
Create a `.env` file in the root directory:
GITHUB_TOKEN=your_github_token_here
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX=onboarding-assistant

### 4. Get your API keys
- **GitHub Token** → [github.com/settings/tokens](https://github.com/settings/tokens) → Generate new token (classic)
- **Pinecone API Key** → [pinecone.io](https://pinecone.io) → Sign up free → API Keys

### 5. Set up Pinecone Index
- Index name: `onboarding-assistant`
- Model: `multilingual-e5-large`
- Metric: `cosine`
- Dimension: `1024`

### 6. Scrape and index knowledge base
```bash
python data_extractor.py
python -m rag_modules.embedder
```

### 7. Run the app locally
```bash
streamlit run app.py
```

### 8. Deploy to Hugging Face Spaces
- Create a new Space at [huggingface.co/new-space](https://huggingface.co/new-space)
- Select Docker → Streamlit template
- Add secrets: `GITHUB_TOKEN`, `PINECONE_API_KEY`, `PINECONE_INDEX`
- Push code to Space repository

---

## 🏗 Architecture Overview
User Question
│
▼
┌─────────────────────┐
│   Streamlit UI      │  Chat interface with agent visibility
└──────────┬──────────┘
│
▼
┌─────────────────────┐
│   Router Agent      │  Classifies query domain
│   Phi-4-mini        │  (engineering/HR/ops/communication)
└──────────┬──────────┘
│
▼
┌─────────────────────┐     ┌────────────────────────┐
│   Retriever Agent   │────▶│   Pinecone Vector DB   │
│   RAG Pipeline      │     │  multilingual-e5-large  │
└──────────┬──────────┘     └────────────────────────┘
│
▼
┌─────────────────────┐
│   Answer Agent      │  Synthesizes grounded response
│   Phi-4-mini        │  with source attribution
└──────────┬──────────┘
│
▼
┌─────────────────────┐
│   Escalation Agent  │  Routes to human if confidence < 75%
└──────────┬──────────┘
│
▼
Final Response
(Answer + Sources + Confidence + Contact)

### Knowledge Base
- **Source:** GitLab Public Handbook (handbook.gitlab.com)
- **Domains:** Engineering, HR, Communication, Operations
- **Pipeline:** Scrape → Chunk (500 words, 50 overlap) → Embed → Index

### Project Structure
Microsoft-Build-AI-Hackathon/
├── app.py                  ← Streamlit UI
├── crew.py                 ← Agent orchestrator
├── data_extractor.py       ← Web scraper
├── requirements.txt
├── Dockerfile
├── agents/
│   ├── router.py           ← Domain classifier agent
│   ├── retriever_agent.py  ← RAG retriever agent
│   ├── answer_agent.py     ← Answer synthesizer agent
│   └── escalation_agent.py ← Escalation agent
└── rag_modules/
├── chunker.py          ← Text chunker
├── embedder.py         ← Pinecone indexer
└── retriever.py        ← Semantic search

---

## 🤖 AI Tools Used

| Component | Tool | Provider |
|---|---|---|
| LLM | Phi-4-mini-instruct | Microsoft (GitHub Models) |
| Inference Endpoint | Azure AI Inference API | Microsoft Azure |
| Embeddings | multilingual-e5-large | Microsoft (Pinecone hosted) |
| Vector Database | Pinecone | Pinecone |
| Agent Orchestration | CrewAI | Open Source |
| UI Framework | Streamlit | Open Source |
| Deployment | Hugging Face Spaces | Hugging Face |
| Knowledge Base | GitLab Handbook | GitLab (Public) |

### Why Microsoft AI Stack?
- **Phi-4-mini-instruct** — Microsoft's own SLM, outperforms larger models on instruction following
- **multilingual-e5-large** — Microsoft's multilingual embedding model, supports 100+ languages
- **GitHub Models** — Microsoft-hosted model inference via Azure AI endpoint
- All LLM calls go through `models.inference.ai.azure.com` — Azure infrastructure

---

## 👤 Team

| | |
|---|---|
| **Name** | Aashika B S |
| **Role** | Data Scientist |
| **Organization** | Trane Technologies |
| **GitHub** | [github.com/Aashika25](https://github.com/Aashika25) |
| **Hackathon** | Microsoft AI Build 2026 |

---

## 📄 Open Source Credits
- [CrewAI](https://github.com/joaomdmoura/crewAI) — Multi-agent orchestration
- [Pinecone](https://pinecone.io) — Vector database
- [Streamlit](https://streamlit.io) — UI framework
- [BeautifulSoup4](https://beautiful-soup-4.readthedocs.io) — Web scraping
- [GitLab Handbook](https://handbook.gitlab.com) — Knowledge base (publicly available)

---