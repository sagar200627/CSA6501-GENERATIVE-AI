import streamlit as st
import requests

st.set_page_config(
    page_title="Local LLM Text Generator",
    page_icon="🤖"
)

st.title("🤖 Local LLM Text Generator")
st.write("Generate text using a locally running Large Language Model.")

prompt = st.text_area(
    "Enter your prompt:",
    "Explain artificial intelligence in simple words."
)

if st.button("Generate Text"):

    if not prompt.strip():
        st.warning("Please enter a prompt.")
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

                st.subheader("Generated Output")
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
