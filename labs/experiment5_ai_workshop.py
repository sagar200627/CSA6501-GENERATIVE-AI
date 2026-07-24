from transformers import pipeline

generator = pipeline("text-generation", model="gpt2")

prompt = """
Write a promotional social media post for an AI Workshop.
"""

result = generator(prompt, max_new_tokens=120)

print(result[0]["generated_text"])