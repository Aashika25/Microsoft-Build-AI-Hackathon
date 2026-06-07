from crewai import Agent
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.getenv("API_KEY")
)

def classify_query(query: str) -> str:
    """Classify query into domain category"""
    response = client.chat.completions.create(
        model="Phi-4-mini-instruct",
        messages=[
            {
                "role": "system",
                "content": """You are a query classifier for an employee onboarding assistant.
                Classify the user query into exactly one of these categories:
                - engineering: dev setup, infrastructure, code, repositories, tools
                - hr: leave, benefits, policies, performance, hiring, onboarding
                - communication: how to communicate, meetings, async work, remote work
                - operations: business ops, tools, workflows, processes

                Respond with only the category name, nothing else."""
            },
            {"role": "user", "content": query}
        ]
    )
    category = response.choices[0].message.content.strip().lower()
    valid = ["engineering", "hr", "communication", "operations"]
    return category if category in valid else "general"