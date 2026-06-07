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
```
GITHUB_TOKEN=your_github_token_here
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX=onboarding-assistant
```

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

### System Flow Diagram
```
┌────────────────────────────────────────────────────────────────────────┐
│                         USER INTERACTION                           │
│                      (Streamlit Chat UI)                           │
└──────────────────────────┬─────────────────────────────────────────────┘
                           │ User Question
                           ▼
┌────────────────────────────────────────────────────────────────────────┐
│                       ROUTER AGENT                                 │
│           (Phi-4-mini-instruct via GitHub Models)                  │
│                                                                    │
│  • Classifies query into domain:                                  │
│    - Engineering (dev setup, architecture, tools)                │
│    - HR (benefits, policies, leave, onboarding)                  │
│    - Operations (processes, workflows, systems)                  │
│    - Communication (culture, teams, meeting norms)               │
│                                                                    │
│  • Extracts key entities from user question                       │
│  • Routes to appropriate domain-specific pipeline                 │
└──────────────────────────┬─────────────────────────────────────────────┘
                           │ Domain + Keywords
                           ▼
         ┌──────────────────────────────────────┐
         │      RETRIEVAL AGENT (RAG)           │
         │                                      │
         │  1. Generate embedding from query    │
         │  2. Query Pinecone vector DB         │
         │  3. Retrieve top-K relevant docs     │
         │  4. Rank by relevance score          │
         └──────────┬───────────────────────────┘
                    │ Retrieved Docs + Scores
                    ▼
     ┌──────────────────────────────────────────┐
     │    PINECONE VECTOR DATABASE              │
     │  (multilingual-e5-large embeddings)      │
     │                                          │
     │  • ~500 chunked documents                │
     │  • GitLab Handbook content indexed       │
     │  • 1024-dimensional vectors              │
     │  • Cosine similarity metric              │
     └──────────────────────────────────────────┘
                    │ Top-K Relevant Chunks
                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      ANSWER AGENT                                  │
│           (Phi-4-mini-instruct via GitHub Models)                  │
│                                                                    │
│  • Synthesizes coherent answer from retrieved docs                │
│  • Calculates confidence score (0-100%)                           │
│  • Performs citation mapping to sources                           │
│  • Generates suggested follow-up questions                        │
│  • Structures output with metadata                                │
└──────────────────────────┬─────────────────────────────────────────────┘
                           │ Answer + Confidence
                           ▼
┌────────────────────────────────────────────────────────────────────────┐
│                    ESCALATION AGENT                                │
│                                                                    │
│  IF confidence >= 75%:                                            │
│    ✓ Show answer to user                                          │
│    ✓ Display sources & confidence                                 │
│                                                                    │
│  IF confidence < 75%:                                             │
│    → Escalate to human support                                    │
│    → Suggest appropriate contact person                           │
│    → Queue for manual review                                      │
└──────────────────────────┬─────────────────────────────────────────────┘
                           │
                           ▼
         ┌────────────────────────────────────┐
         │   FINAL RESPONSE (UI Rendering)    │
         │                                    │
         │  • Answer text                     │
         │  • Confidence bar (color-coded)    │
         │  • Source citations                │
         │  • Agent transparency log          │
         │  • Suggested next questions        │
         │  • Escalation info (if needed)     │
         └────────────────────────────────────┘
```

### Component Details

#### 1. **Streamlit UI Layer**
- Interactive chat interface
- Real-time agent processing visibility
- Confidence score visualization
- Source citation links
- Suggested question templates
- Mobile-responsive design

#### 2. **Router Agent**
- **Model:** Phi-4-mini-instruct (Microsoft)
- **Purpose:** Domain classification
- **Categories:** Engineering, HR, Operations, Communication
- **Input:** Raw user question
- **Output:** Domain label + extracted keywords

#### 3. **Retrieval Agent (RAG)**
- **Embedding Model:** multilingual-e5-large
- **Vector DB:** Pinecone (serverless)
- **Chunk Size:** 500 words with 50-word overlap
- **Search Type:** Semantic similarity search
- **Top-K Retrieval:** Returns 5-10 most relevant chunks
- **Pre-processing:** Text cleaning, normalization

#### 4. **Answer Agent**
- **Model:** Phi-4-mini-instruct (Microsoft)
- **Purpose:** Answer synthesis & grounding
- **Process:**
  - Combines retrieved context with user query
  - Generates coherent, grounded response
  - Calculates confidence score
  - Maps answers to source documents
  - Extracts follow-up questions
- **Output:** Structured answer JSON with metadata

#### 5. **Escalation Agent**
- **Threshold:** 75% confidence minimum
- **Low Confidence Action:** Routes to human support queue
- **Logic:** Identifies appropriate department contact
- **Fallback:** Generic support escalation
- **Output:** Escalation ticket with context

#### 6. **Vector Database (Pinecone)**
- **Index Name:** `onboarding-assistant`
- **Embedding Dimension:** 1024
- **Metric:** Cosine similarity
- **Namespace:** Organized by domain
- **Metadata:** Source URL, document type, domain, timestamp

---

## 📁 Project Structure

```
Microsoft-Build-AI-Hackathon/
│
├── 📄 README.md                    ← Project documentation (this file)
├── 📄 requirements.txt             ← Python dependencies
├── 📄 Dockerfile                   ← Container configuration
├── 📄 .env.example                 ← Environment template
│
├── 🚀 app.py                       ← MAIN: Streamlit UI application
│                                      - Chat interface
│                                      - Agent response rendering
│                                      - Confidence visualization
│                                      - Source citation display
│
├── 🔧 crew.py                      ← Agent orchestration
│                                      - Creates and manages all agents
│                                      - Defines agent roles & responsibilities
│                                      - Configures LLM settings
│                                      - Manages task execution flow
│
├── 📥 data_extractor.py            ← Knowledge base scraper
│                                      - Scrapes GitLab Handbook
│                                      - Extracts structured content
│                                      - Saves to local storage
│                                      - Handles pagination & errors
│
├── 📁 agents/                      ← Multi-agent system modules
│   │
│   ├── router.py                   ← Domain Classification Agent
│   │                                  - Analyzes user question
│   │                                  - Classifies into domain
│   │                                  - Extracts intent & entities
│   │                                  - Returns routing decision
│   │
│   ├── retriever_agent.py          ← RAG Retrieval Agent
│   │                                  - Queries Pinecone
│   │                                  - Scores retrieved chunks
│   │                                  - Formats context window
│   │                                  - Provides source metadata
│   │
│   ├── answer_agent.py             ← Answer Synthesis Agent
│   │                                  - Generates grounded response
│   │                                  - Calculates confidence score
│   │                                  - Maps to source documents
│   │                                  - Creates follow-up suggestions
│   │
│   └── escalation_agent.py         ← Escalation Management Agent
│                                      - Evaluates confidence threshold
│                                      - Identifies escalation path
│                                      - Routes to support team
│                                      - Logs escalation context
│
├── 📁 rag_modules/                 ← RAG Pipeline Components
│   │
│   ├── chunker.py                  ← Text Chunking Utility
│   │                                  - Splits documents into chunks
│   │                                  - Configurable chunk size (500 words)
│   │                                  - Sliding window overlap (50 words)
│   │                                  - Preserves semantic boundaries
│   │
│   ├── embedder.py                 ← Vector Embedding & Indexing
│   │                                  - Encodes chunks to embeddings
│   │                                  - Uploads to Pinecone
│   │                                  - Manages index metadata
│   │                                  - Handles batch operations
│   │
│   └── retriever.py                ← Semantic Search Engine
│                                      - Queries Pinecone index
│                                      - Performs similarity search
│                                      - Re-ranks results
│                                      - Formats retrieved context
│
└── 📁 .github/                     ← GitHub configuration
    └── workflows/                  ← CI/CD pipelines (optional)
```

### Key File Responsibilities

| File | Purpose | Dependencies |
|------|---------|--------------|
| `app.py` | Streamlit UI & state management | `crew.py`, `rag_modules/` |
| `crew.py` | Agent initialization & orchestration | `agents/`, `rag_modules/` |
| `data_extractor.py` | Knowledge base population | `rag_modules/chunker.py` |
| `agents/router.py` | Query routing | Phi-4-mini LLM |
| `agents/retriever_agent.py` | Document retrieval | `rag_modules/retriever.py` |
| `agents/answer_agent.py` | Response synthesis | Phi-4-mini LLM |
| `agents/escalation_agent.py` | Confidence-based routing | LLM |
| `rag_modules/chunker.py` | Text segmentation | - |
| `rag_modules/embedder.py` | Vector embedding | Pinecone, e5-large |
| `rag_modules/retriever.py` | Semantic search | Pinecone |

### Data Flow Path

```
Raw Handbook Content
         ↓
    data_extractor.py
         ↓
    rag_modules/chunker.py (500-word chunks)
         ↓
    rag_modules/embedder.py (e5-large embeddings)
         ↓
    Pinecone Vector DB
         ↓
User Query → app.py → crew.py → agents/router.py
         ↓
    agents/retriever_agent.py → rag_modules/retriever.py
         ↓
    Pinecone Query Results
         ↓
    agents/answer_agent.py (Synthesize)
         ↓
    agents/escalation_agent.py (Check confidence)
         ↓
    app.py (Render response)
         ↓
    User sees answer with sources & confidence
```

---

## 🤖 AI Tools & Technologies Used

| Component | Tool | Provider | Version |
|-----------|------|----------|---------|
| **LLM** | Phi-4-mini-instruct | Microsoft | Latest |
| **Inference** | Azure AI Inference API | Microsoft Azure | - |
| **Embeddings** | multilingual-e5-large | Microsoft | Latest |
| **Vector DB** | Pinecone | Pinecone | Serverless |
| **Agent Orchestration** | CrewAI | Open Source | v0.x |
| **UI Framework** | Streamlit | Open Source | v1.x |
| **Deployment** | Hugging Face Spaces | Hugging Face | - |
| **Knowledge Base** | GitLab Handbook | GitLab (Public) | Live |
| **Web Scraping** | BeautifulSoup4 | Open Source | v4.x |
| **API Calls** | Requests | Open Source | v2.x |

### Why Microsoft AI Stack?

✅ **Phi-4-mini-instruct**
- Microsoft's specialized Small Language Model
- Outperforms larger models on instruction-following tasks
- Low latency, optimized for edge & cloud deployment
- Free tier via GitHub Models

✅ **multilingual-e5-large**
- Microsoft's multilingual embedding model
- Supports 100+ languages
- Superior semantic understanding
- Integrates seamlessly with Pinecone

✅ **GitHub Models & Azure AI**
- Free inference endpoint via GitHub Models
- All LLM calls routed through `models.inference.ai.azure.com`
- Enterprise-grade reliability & compliance
- Part of Microsoft's unified AI platform

---

## 🔄 Workflow & Execution Flow

### Single Query Lifecycle

```
1. USER SUBMITS QUESTION
   ├─ Input: "How do I set up my development environment?"
   └─ Timestamp: Recorded for logging

2. ROUTER AGENT CLASSIFIES
   ├─ Domain: "Engineering"
   ├─ Confidence: 0.98
   └─ Keywords: ["dev setup", "environment", "onboarding"]

3. RETRIEVER AGENT SEARCHES
   ├─ Query embedding: Generated via e5-large
   ├─ Pinecone search: Top 8 chunks retrieved
   ├─ Similarity scores: 0.92, 0.88, 0.85, ...
   └─ Retrieved docs: 3,847 tokens of context

4. ANSWER AGENT SYNTHESIZES
   ├─ LLM processing: Phi-4-mini with context
   ├─ Generation: Coherent 150-word response
   ├─ Confidence: 0.87 (87%)
   └─ Sources: 3 documents cited

5. ESCALATION AGENT DECIDES
   ├─ Confidence check: 0.87 > 0.75 ✓
   ├─ Action: SHOW TO USER
   └─ Route: Direct response

6. UI RENDERS RESPONSE
   ├─ Answer text displayed
   ├─ Confidence bar: 87% (green)
   ├─ Sources listed with links
   ├─ Suggested questions shown
   └─ Agent log visible to user
```

---

## 👤 Team

| Attribute | Value |
|-----------|-------|
| **Name** | Aashika B S |
| **Role** | Data Scientist |
| **Organization** | Trane Technologies |
| **GitHub** | [github.com/Aashika25](https://github.com/Aashika25) |
| **Hackathon** | Microsoft AI Build 2026 |

---

## 📄 Open Source Credits

- [CrewAI](https://github.com/joaomdmoura/crewAI) — Multi-agent orchestration framework
- [Pinecone](https://pinecone.io) — Serverless vector database
- [Streamlit](https://streamlit.io) — Rapid UI development framework
- [BeautifulSoup4](https://beautiful-soup-4.readthedocs.io) — HTML/XML parsing & web scraping
- [GitLab Handbook](https://handbook.gitlab.com) — Knowledge base (publicly available)

---

## 📝 License

This project is submitted for the Microsoft AI Build Hackathon 2026. Check repository for license details.

---

## 🔗 Repository & Demo Links

- **Repository:** https://github.com/Aashika25/Microsoft-Build-AI-Hackathon/tree/main
- **YouTube Demo:** https://www.youtube.com/watch?v=QlVB-aX9CLc

---

**Last Updated:** June 2026  
**Status:** Active Development  
**Deployment:** [Live on Hugging Face Spaces](https://huggingface.co/spaces/Aashika25/OnBoardIQ)
