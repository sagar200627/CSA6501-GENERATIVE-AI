from transformers import BertTokenizer, BertModel

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")

sentence = "Deep Learning is powerful."

inputs = tokenizer(sentence, return_tensors="pt")

outputs = model(**inputs)

print(outputs.last_hidden_state.shape)
