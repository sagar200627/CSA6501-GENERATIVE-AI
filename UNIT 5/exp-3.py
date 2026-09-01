import streamlit as st
import requests

st.set_page_config(
    page_title="Local LLM Question Answering",
    page_icon="❓"
)

st.title("❓ Local LLM Question Answering")
st.write(
    "Ask questions and get answers using a locally running Large Language Model."
)

question = st.text_area(
    "Enter your question:",
    height=150,
    placeholder="Enter an engineering-related question..."
)

if st.button("Get Answer"):

    if not question.strip():
        st.warning("Please enter a question.")

    else:
        prompt = f"""
You are an engineering-support assistant.

Answer the following question clearly and accurately.
Give a concise explanation in simple English.

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

                st.subheader("Answer")
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
