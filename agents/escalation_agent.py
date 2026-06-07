from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.getenv("API_KEY")
)

# Contact directory per domain
CONTACT_DIRECTORY = {
    "engineering": {
        "team": "Engineering Team",
        "channel": "#engineering on Slack",
        "email": "engineering@company.com"
    },
    "hr": {
        "team": "People & HR Team",
        "channel": "#people-group on Slack",
        "email": "hr@company.com"
    },
    "communication": {
        "team": "Operations Team",
        "channel": "#operations on Slack",
        "email": "ops@company.com"
    },
    "operations": {
        "team": "Business Operations Team",
        "channel": "#business-ops on Slack",
        "email": "bizops@company.com"
    },
    "general": {
        "team": "Your Onboarding Buddy",
        "channel": "#new-joiners on Slack",
        "email": "onboarding@company.com"
    }
}

CONFIDENCE_THRESHOLD = 0.75

def check_escalation(confidence: float, category: str) -> dict:
    """Decide if escalation is needed based on confidence score"""
    
    needs_escalation = confidence < CONFIDENCE_THRESHOLD
    contact = CONTACT_DIRECTORY.get(category, CONTACT_DIRECTORY["general"])

    return {
        "needs_escalation": needs_escalation,
        "confidence": confidence,
        "contact": contact if needs_escalation else None,
        "message": (
            f"I wasn't fully confident in my answer. "
            f"Please reach out to the **{contact['team']}** "
            f"via {contact['channel']} or {contact['email']} for more help."
        ) if needs_escalation else None
    }