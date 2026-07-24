from transformers import pipeline

generator = pipeline("text-generation", model="gpt2")

zero_shot = """
Write a product description for a Smart Fitness Watch.
Highlight its features, battery life, health tracking, and stylish design.
"""

one_shot = """
Example

Product: Wireless Earbuds

Description:
Experience crystal-clear sound with Wireless Earbuds featuring noise cancellation,
long battery life, and a comfortable design.

Now write a product description for a Smart Fitness Watch.
"""

few_shot = """
Example 1

Product: Wireless Earbuds

Description:
Crystal-clear sound with long battery life.

Example 2

Product: Smart Water Bottle

Description:
Tracks water intake and reminds users to stay hydrated.

Example 3

Product: Portable Charger

Description:
Fast charging with compact design.

Now write a product description for a Smart Fitness Watch.
"""

print("\n===== ZERO SHOT =====")
print(generator(zero_shot, max_new_tokens=120)[0]["generated_text"])

print("\n===== ONE SHOT =====")
print(generator(one_shot, max_new_tokens=120)[0]["generated_text"])

print("\n===== FEW SHOT =====")
print(generator(few_shot, max_new_tokens=120)[0]["generated_text"])