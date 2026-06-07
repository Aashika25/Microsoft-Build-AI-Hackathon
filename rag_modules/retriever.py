from pinecone import Pinecone
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

def get_index():
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = pc.Index(os.getenv("PINECONE_INDEX"))
    return index

def retrieve(query, top_k=5, category_filter=None):
    index = get_index()

    filter_dict = None
    if category_filter:
        filter_dict = {"category": {"$eq": category_filter}}

    results = index.search(
        namespace="onboarding",
        query={
            "inputs": {"text": query},
            "top_k": top_k,
            "filter": filter_dict
        },
        fields=["text", "source", "category", "filename"]
    )

    hits = []
    for match in results.result.hits:  # direct object access
        hits.append({
            "text": match.fields.get("text", ""),
            "source": match.fields.get("source", ""),
            "category": match.fields.get("category", ""),
            "score": match.score  # direct attribute, not _score
        })

    return hits

if __name__ == "__main__":
    results = retrieve("how do I set up my dev environment?")
    for r in results:
        print(f"Score: {r['score']:.3f} | Category: {r['category']}")
        print(f"Source: {r['source']}")
        print(f"Text: {r['text'][:200]}\n")