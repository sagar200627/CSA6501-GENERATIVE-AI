import requests
import chromadb

# =========================================================
# EXPERIMENT 9
# LOCAL RETRIEVAL-AUGMENTED GENERATION (RAG) SYSTEM
# USING ENGINEERING DOCUMENTS, VECTOR DATABASE AND OLLAMA
# =========================================================

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:latest"

DOCUMENT_FILE = "engineering_document.txt"


# =========================================================
# 1. READ ENGINEERING DOCUMENT
# =========================================================

print("=" * 70)
print("LOCAL RAG SYSTEM USING ENGINEERING DOCUMENTS AND OLLAMA")
print("=" * 70)

try:

    with open(DOCUMENT_FILE, "r", encoding="utf-8") as file:
        document = file.read()

except FileNotFoundError:

    print("\nERROR: engineering_document.txt was not found.")
    print("Place the document in the same folder as experiment9.py.")
    exit()


# =========================================================
# 2. SPLIT DOCUMENT INTO CHUNKS
# =========================================================

def create_chunks(text, chunk_size=500):

    words = text.split()

    chunks = []

    for i in range(0, len(words), chunk_size):

        chunk = " ".join(
            words[i:i + chunk_size]
        )

        chunks.append(chunk)

    return chunks


chunks = create_chunks(document)

print("\nNumber of document chunks:", len(chunks))


# =========================================================
# 3. CREATE VECTOR DATABASE
# =========================================================

client = chromadb.PersistentClient(
    path="./rag_database"
)

collection = client.get_or_create_collection(
    name="engineering_documents"
)


# =========================================================
# 4. STORE DOCUMENT CHUNKS
# =========================================================

for i, chunk in enumerate(chunks):

    collection.upsert(
        ids=[f"chunk_{i}"],
        documents=[chunk]
    )

print("Engineering document stored in vector database.")


# =========================================================
# 5. ASK USER QUESTION
# =========================================================

question = input(
    "\nEnter your engineering question: "
)


# =========================================================
# 6. RETRIEVE RELEVANT DOCUMENT INFORMATION
# =========================================================

results = collection.query(
    query_texts=[question],
    n_results=min(3, len(chunks))
)

retrieved_documents = results["documents"][0]


print("\n" + "=" * 70)
print("RETRIEVED INFORMATION")
print("=" * 70)

for i, doc in enumerate(retrieved_documents):

    print(f"\nChunk {i + 1}:")
    print(doc)


# =========================================================
# 7. CREATE CONTEXT
# =========================================================

context = "\n\n".join(
    retrieved_documents
)


# =========================================================
# 8. CREATE RAG PROMPT
# =========================================================

prompt = f"""
You are an engineering question-answering assistant.

Answer the user's question using ONLY the information
provided in the retrieved engineering document.

If the answer is not available in the retrieved information,
say:

"The answer is not available in the provided document."

Do not invent information.

RETRIEVED ENGINEERING INFORMATION:
{context}

USER QUESTION:
{question}

ANSWER:
"""


# =========================================================
# 9. SEND CONTEXT + QUESTION TO OLLAMA
# =========================================================

try:

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    if response.status_code == 200:

        result = response.json()

        answer = result["response"]

        print("\n" + "=" * 70)
        print("RAG GENERATED ANSWER")
        print("=" * 70)

        print(answer)

    else:

        print("\nOllama Error:")
        print(response.text)


except requests.exceptions.ConnectionError:

    print("\nERROR: Cannot connect to Ollama.")
    print("Make sure Ollama is running.")

except Exception as e:

    print("\nError occurred:")
    print(e)
