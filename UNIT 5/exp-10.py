import requests
import chromadb

# =========================================================
# EXPERIMENT 10
# LOCAL RAG-BASED ENGINEERING TROUBLESHOOTING SYSTEM
# =========================================================

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:latest"

DOCUMENT_FILE = "troubleshooting_document.txt"


print("=" * 70)
print("LOCAL RAG ENGINEERING TROUBLESHOOTING SYSTEM")
print("=" * 70)


# =========================================================
# 1. READ TECHNICAL DOCUMENT
# =========================================================

try:

    with open(DOCUMENT_FILE, "r", encoding="utf-8") as file:
        document = file.read()

except FileNotFoundError:

    print("\nERROR: troubleshooting_document.txt not found.")
    print("Place it in the same folder as experiment10.py.")
    exit()


# =========================================================
# 2. SPLIT DOCUMENT INTO CHUNKS
# =========================================================

def create_chunks(text, chunk_size=100):

    words = text.split()

    chunks = []

    for i in range(0, len(words), chunk_size):

        chunk = " ".join(
            words[i:i + chunk_size]
        )

        chunks.append(chunk)

    return chunks


chunks = create_chunks(document)

print("\nTechnical document loaded.")
print("Number of document chunks:", len(chunks))


# =========================================================
# 3. CREATE VECTOR DATABASE
# =========================================================

db_client = chromadb.PersistentClient(
    path="./troubleshooting_database"
)

collection = db_client.get_or_create_collection(
    name="engineering_troubleshooting"
)


# =========================================================
# 4. STORE DOCUMENT CHUNKS
# =========================================================

for i, chunk in enumerate(chunks):

    collection.upsert(
        ids=[f"trouble_chunk_{i}"],
        documents=[chunk]
    )

print("Technical information stored in vector database.")


# =========================================================
# 5. GET USER PROBLEM
# =========================================================

problem = input(
    "\nDescribe the engineering problem:\n"
)


if not problem.strip():

    print("Please enter an engineering problem.")
    exit()


# =========================================================
# 6. RETRIEVE RELEVANT INFORMATION
# =========================================================

results = collection.query(
    query_texts=[problem],
    n_results=min(3, len(chunks))
)

retrieved_documents = results["documents"][0]


print("\n" + "=" * 70)
print("RETRIEVED TROUBLESHOOTING INFORMATION")
print("=" * 70)

for i, document_part in enumerate(retrieved_documents):

    print(f"\nInformation {i + 1}:")
    print(document_part)


# =========================================================
# 7. CREATE CONTEXT
# =========================================================

context = "\n\n".join(
    retrieved_documents
)


# =========================================================
# 8. CREATE TROUBLESHOOTING PROMPT
# =========================================================

prompt = f"""
You are an engineering troubleshooting assistant.

Use ONLY the retrieved technical information provided below.

Analyze the user's problem and provide step-by-step
troubleshooting recommendations.

Rules:
1. Do not invent technical information.
2. Use only information available in the retrieved document.
3. Give the steps in a clear numbered format.
4. Mention relevant safety precautions.
5. If the required information is not available, say:
   "The required troubleshooting information is not available
   in the provided technical document."

RETRIEVED TECHNICAL INFORMATION:
{context}

USER PROBLEM:
{problem}

TROUBLESHOOTING RECOMMENDATIONS:
"""


# =========================================================
# 9. SEND TO OLLAMA
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
        print("STEP-BY-STEP TROUBLESHOOTING RECOMMENDATIONS")
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
