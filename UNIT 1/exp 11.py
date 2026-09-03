from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

sentence = "Machine Learning is interesting."

tokens = tokenizer.tokenize(sentence)

print(tokens)
