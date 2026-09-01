import requests

# =========================================================
# EXPERIMENT 5
# TEXT GENERATION USING OLLAMA AND PYTHON
# =========================================================

print("=" * 60)
print("TEXT GENERATION USING OLLAMA AND PYTHON")
print("=" * 60)

prompt = input("\nEnter your prompt: ")

if not prompt.strip():
    print("Please enter a prompt.")
else:

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
            print("GENERATED TEXT")
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
