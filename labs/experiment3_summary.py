from transformers import pipeline

generator = pipeline("text-generation", model="gpt2")

article = """
Artificial Intelligence is transforming industries by automating tasks,
improving decision-making, and increasing efficiency in healthcare,
education, finance, transportation, and manufacturing.
"""

prompt = f"""
Summarize the following article in about 50 words.

{article}
"""

result = generator(prompt, max_new_tokens=70)

print(result[0]["generated_text"])