from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.getenv("API_KEY")
)

def generate_answer(query: str, context_chunks: list) -> dict:
    """Generate answer from retrieved context"""

    # Build context string
    context = "\n\n---\n\n".join([
        f"Source: {c['source']}\n{c['text']}"
        for c in context_chunks
    ])

    response = client.chat.completions.create(
        model="Phi-4-mini-instruct",
        messages=[
            {
                "role": "system",
                "content": """You are a helpful employee onboarding assistant.
                Answer the employee's question using ONLY the provided context.
                Be concise, friendly and helpful.
                Always mention the source of your answer at the end."""
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {query}"
            }
        ]
    )

    answer = response.choices[0].message.content.strip()

    # Calculate average confidence from retrieval scores
    avg_score = sum(c['score'] for c in context_chunks) / len(context_chunks) if context_chunks else 0

    return {
        "answer": answer,
        "confidence": avg_score,
        "sources": list(set(c['source'] for c in context_chunks))
    }