from pinecone import Pinecone
from dotenv import load_dotenv
import os
import time
from rag_modules.chunker import load_and_chunk_all

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))


def get_index():
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = pc.Index(os.getenv("PINECONE_INDEX"))
    return index

def upsert_chunks(chunks, batch_size=50):
    index = get_index()
    total = len(chunks)
    
    for i in range(0, total, batch_size):
        batch = chunks[i:i + batch_size]
        
        records = [
            {
                "id": chunk["chunk_id"],
                "text": chunk["text"],
                "source": chunk["source"],
                "category": chunk["category"],
                "filename": chunk["filename"]
            }
            for chunk in batch
        ]

        index.upsert_records(
            namespace="onboarding",
            records=records
        )

        print(f"✅ Upserted batch {i//batch_size + 1} — {min(i+batch_size, total)}/{total} chunks")
        time.sleep(0.5)  # avoid rate limiting

    print(f"\n✅ All {total} chunks indexed in Pinecone!")

if __name__ == "__main__":
    chunks = load_and_chunk_all()
    upsert_chunks(chunks)