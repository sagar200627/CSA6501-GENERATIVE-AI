from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

text = "Artificial Intelligence is transforming the world."

tokens = tokenizer.tokenize(text)

print("Tokens:")
print(tokens)