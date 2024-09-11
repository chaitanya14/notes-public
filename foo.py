import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from datetime import datetime

# Download necessary NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Sample training data
training_data = [
    ("How are you?", "greeting"),
    ("What's your name?", "name"),
    ("What time is it?", "time"),
    ("Goodbye", "farewell"),
    ("Tell me a joke", "joke"),
    ("What's the weather like?", "weather"),
]

# Separate texts and labels
texts, labels = zip(*training_data)

# Create a pipeline with TF-IDF vectorizer and Naive Bayes classifier
model = make_pipeline(TfidfVectorizer(), MultinomialNB())

# Train the model
model.fit(texts, labels)

def respond_greeting():
    return "Hello! How can I help you today?"

def respond_name():
    return "My name is SimpleAI. Nice to meet you!"

def respond_time():
    return f"The current time is {datetime.now().strftime('%H:%M:%S')}."

def respond_farewell():
    return "Goodbye! Have a great day!"

def respond_joke():
    return "Why don't scientists trust atoms? Because they make up everything!"

def respond_weather():
    return "I'm sorry, I don't have access to real-time weather data. You might want to check a weather app or website for accurate information."

def respond_unknown():
    return "I'm not sure how to respond to that. Can you please rephrase or ask something else?"

# Map intents to response functions
responses = {
    "greeting": respond_greeting,
    "name": respond_name,
    "time": respond_time,
    "farewell": respond_farewell,
    "joke": respond_joke,
    "weather": respond_weather
}

def preprocess_text(text):
    # Tokenize and remove stopwords
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    return ' '.join([word for word in tokens if word not in stop_words])

def chat():
    print("SimpleAI: Hello! How can I help you? (Type 'quit' to exit)")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            print("SimpleAI: Goodbye!")
            break
        
        # Preprocess and predict intent
        processed_input = preprocess_text(user_input)
        intent = model.predict([processed_input])[0]
        
        # Generate and print response
        response_func = responses.get(intent, respond_unknown)
        print("SimpleAI:", response_func())

# Start the conversation
if __name__ == "__main__":
    chat()
