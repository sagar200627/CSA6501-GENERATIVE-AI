from transformers import GPT2Tokenizer, GPT2LMHeadModel

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

input_ids = tokenizer.encode("Deep Learning", return_tensors="pt")

output = model.generate(input_ids, max_length=30)

print(tokenizer.decode(output[0], skip_special_tokens=True))
