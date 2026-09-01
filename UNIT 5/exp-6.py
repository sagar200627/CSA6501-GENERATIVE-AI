import requests

# =========================================================
# EXPERIMENT 6
# QUESTION ANSWERING USING OLLAMA AND PYTHON
# =========================================================

print("=" * 60)
print("QUESTION ANSWERING USING OLLAMA AND PYTHON")
print("=" * 60)

question = input("\nEnter your question: ")

if not question.strip():
    print("Please enter a question.")

else:

    prompt = f"""
You are a helpful engineering assistant.

Answer the following question clearly and accurately.
Use simple English and provide a concise explanation.

Question:
{question}

Answer:
"""

    try:

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:latest",
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        if response.status_code == 200:

            result = response.json()

            print("\n" + "=" * 60)
            print("ANSWER")
            print("=" * 60)

            print(result["response"])

        else:

            print("\nOllama Error:")
            print(response.text)

    except requests.exceptions.ConnectionError:

        print("\nERROR: Cannot connect to Ollama.")
        print("Please make sure Ollama is running.")

    except Exception as e:

        print("\nError occurred:")
        print(e)
