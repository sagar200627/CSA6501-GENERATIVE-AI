from transformers import pipeline

qa = pipeline("question-answering")

context = """
Python is a programming language.
It was developed by Guido van Rossum.
"""

question = "Who developed Python?"

answer = qa(question=question, context=context)

print(answer)
