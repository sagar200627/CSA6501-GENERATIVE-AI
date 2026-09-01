import requests

# =========================================================
# EXPERIMENT 7
# HALLUCINATION ANALYSIS USING A LOCAL LLM
# =========================================================

print("=" * 65)
print("HALLUCINATION ANALYSIS USING OLLAMA")
print("=" * 65)

# ---------------------------------------------------------
# REFERENCE INFORMATION
# ---------------------------------------------------------

reference = """
The Eiffel Tower is located in Paris, France.
It was completed in 1889.
It was designed by Gustave Eiffel's engineering company.
"""

# ---------------------------------------------------------
# TEST PROMPT
# ---------------------------------------------------------

question = """
Who designed the Eiffel Tower and in which year was it
completed? Also explain where it is located.
"""

prompt = f"""
Answer the following question using ONLY the reference
information provided below.

REFERENCE INFORMATION:
{reference}

QUESTION:
{question}

If the reference does not contain the answer, clearly say:
"The reference information does not provide this information."

Do not invent or assume facts.

Answer:
"""

# ---------------------------------------------------------
# SEND REQUEST TO OLLAMA
# ---------------------------------------------------------

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

        answer = result["response"]

        # -------------------------------------------------
        # DISPLAY REFERENCE
        # -------------------------------------------------

        print("\n" + "=" * 65)
        print("REFERENCE INFORMATION")
        print("=" * 65)

        print(reference)

        # -------------------------------------------------
        # DISPLAY QUESTION
        # -------------------------------------------------

        print("\n" + "=" * 65)
        print("QUESTION")
        print("=" * 65)

        print(question)

        # -------------------------------------------------
        # DISPLAY ANSWER
        # -------------------------------------------------

        print("\n" + "=" * 65)
        print("MODEL RESPONSE")
        print("=" * 65)

        print(answer)

        # -------------------------------------------------
        # ANALYSIS
        # -------------------------------------------------

        print("\n" + "=" * 65)
        print("HALLUCINATION ANALYSIS")
        print("=" * 65)

        print("""
The model response should be compared with the reference
information.

Reference facts:
1. Location: Paris, France
2. Completion year: 1889
3. Designer: Gustave Eiffel's engineering company

If the model provides information that is not supported
by the reference, that information can be considered
potential hallucination.

OBSERVATION:
The reference information acts as the ground truth.
The model should avoid generating unsupported facts.
""")

    else:

        print("Ollama Error:")
        print(response.text)

except requests.exceptions.ConnectionError:

    print("\nERROR: Cannot connect to Ollama.")
    print("Please make sure Ollama is running.")

except Exception as e:

    print("\nError occurred:")
    print(e)
