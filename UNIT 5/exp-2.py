import streamlit as st
import requests

st.set_page_config(
    page_title="Local LLM Text Summarizer",
    page_icon="📝"
)

st.title("📝 Local LLM Text Summarizer")
st.write("Summarize lengthy text using a locally running Large Language Model.")

text = st.text_area(
    "Enter the text to summarize:",
    height=300,
    placeholder="Enter or paste your engineering-related text here..."
)

if st.button("Summarize Text"):

    if not text.strip():
        st.warning("Please enter some text to summarize.")

    else:
        prompt = f"""
Summarize the following text clearly and concisely.
Keep the important points and remove unnecessary details.
Write the summary in simple English.

TEXT:
{text}

SUMMARY:
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

                st.subheader("Generated Summary")
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
