from transformers import pipeline

generator = pipeline("text-generation", model="gpt2")

prompts = [
    "Artificial Intelligence",
    "Machine Learning",
    "Future Technology"
]

for prompt in prompts:

    result = generator(
        prompt,
        max_length=30,
        num_return_sequences=1
    )

    print("\nPrompt:", prompt)
    print(result[0]["generated_text"])
