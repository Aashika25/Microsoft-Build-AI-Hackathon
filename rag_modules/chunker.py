import os

def chunk_text(text, chunk_size=500, overlap=50):
    """Split text into overlapping chunks"""
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = ' '.join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks

def load_and_chunk_all(data_dir="data/gitlab_handbook_data"):
    """Walk through all folders and chunk every txt file"""
    all_chunks = []

    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith(".txt"):
                filepath = os.path.join(root, file)

                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extract source URL from first line
                lines = content.split('\n')
                source_url = lines[0].replace("SOURCE: ", "").strip()
                
                # Get category from folder path
                rel_path = os.path.relpath(filepath, data_dir)
                category = rel_path.split(os.sep)[0]

                # Skip header lines (SOURCE + === line)
                main_content = '\n'.join(lines[3:])

                chunks = chunk_text(main_content)

                for i, chunk in enumerate(chunks):
                    if len(chunk.strip()) > 100:  # skip tiny chunks
                        all_chunks.append({
                            "text": chunk,
                            "source": source_url,
                            "category": category,
                            "filename": file,
                            "chunk_id": f"{category}_{file}_{i}"
                        })

    print(f"✅ Total chunks created: {len(all_chunks)}")
    return all_chunks