from transformers import BertTokenizer, BertModel

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")

s1 = "I like AI."
s2 = "I love Artificial Intelligence."

e1 = model(**tokenizer(s1, return_tensors="pt"))
e2 = model(**tokenizer(s2, return_tensors="pt"))

print(e1.last_hidden_state.shape)
print(e2.last_hidden_state.shape)
