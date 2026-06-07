from rag_modules.retriever import retrieve

def fetch_context(query: str, category: str) -> list:
    """Retrieve relevant chunks from Pinecone based on query and category"""
    
    # Map category to folder filter
    category_map = {
        "engineering": "handbook",
        "hr": "handbook",
        "communication": "handbook",
        "operations": "handbook",
        "general": None
    }

    filter_cat = category_map.get(category, None)
    results = retrieve(query, top_k=5, category_filter=filter_cat)
    return results