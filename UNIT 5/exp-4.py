import streamlit as st
import requests

st.set_page_config(
    page_title="Local LLM Translation and Paraphrasing",
    page_icon="🌐"
)

st.title("🌐 Local LLM Translation and Paraphrasing")
st.write(
    "Translate text into another language or paraphrase it using a "
    "locally running Large Language Model."
)

text = st.text_area(
    "Enter your text:",
    height=180,
    placeholder="Enter the text you want to translate or paraphrase..."
)

operation = st.selectbox(
    "Select operation:",
    ["Translation", "Paraphrasing"]
)

language = st.text_input(
    "Target language:",
    "Tamil"
)

if st.button("Process Text"):

    if not text.strip():
        st.warning("Please enter some text.")

    else:

        if operation == "Translation":
            prompt = f"""
Translate the following text from English to {language}.
Keep the meaning accurate and use natural language.

Text:
{text}

Translation:
"""

        else:
            prompt = f"""
Paraphrase the following text.
Rewrite it using different words while keeping the original meaning.
Do not add new information.

Text:
{text}

Paraphrased Text:
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

                if operation == "Translation":
                    st.subheader("Translated Text")
                else:
                    st.subheader("Paraphrased Text")

                st.write(result["response"])

            else:
                st.error("Ollama returned an error.")
                st.write(response.text)

        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot connect to Ollama. "
                "Please make sure Ollama is running."
            )

        except Exception as e:
            st.error(f"Error: {e}")
