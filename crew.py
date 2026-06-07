from agents.router import classify_query
from agents.retriever_agent import fetch_context
from agents.answer_agent import generate_answer
from agents.escalation_agent import check_escalation

def run_crew(query: str) -> dict:
    print(f"\n🔍 Query: {query}")

    # Agent 1 — Router
    category = classify_query(query)
    print(f"📂 Router Agent → Category: {category}")

    # Agent 2 — Retriever
    context = fetch_context(query, category)
    print(f"📄 Retriever Agent → {len(context)} chunks fetched")

    # Agent 3 — Answer
    result = generate_answer(query, context)
    print(f"💬 Answer Agent → Confidence: {result['confidence']:.3f}")

    # Agent 4 — Escalation
    escalation = check_escalation(result['confidence'], category)
    print(f"🚨 Escalation Agent → Needed: {escalation['needs_escalation']}")

    return {
        "query": query,
        "category": category,
        "answer": result['answer'],
        "confidence": result['confidence'],
        "sources": result['sources'],
        "escalation": escalation
    }

if __name__ == "__main__":
    response = run_crew("How can I Scale my GitLab infrastructure to prevent incidents?")
    print("\n" + "="*50)
    print(f"CATEGORY : {response['category']}")
    print(f"ANSWER   : {response['answer']}")
    print(f"SOURCES  : {response['sources']}")
    if response['escalation']['needs_escalation']:
        print(f"ESCALATE : {response['escalation']['message']}")