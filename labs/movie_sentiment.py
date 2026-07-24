# Movie Sentiment Analyzer using BERT

from transformers import pipeline

print("Loading BERT Model...")

# Load the sentiment analysis model
classifier = pipeline("sentiment-analysis")

print("Model Loaded Successfully!")

# Get movie review from the user
review = input("\nEnter a Movie Review: ")

# Predict sentiment
result = classifier(review)

# Display the result
print("\nPrediction")
print("------------------------")
print("Review      :", review)
print("Sentiment   :", result[0]["label"])
print("Confidence  :", round(result[0]["score"] * 100, 2), "%")