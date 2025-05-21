import nltk
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download required NLTK data files
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

# Sample corpus for chatbot to answer from
corpus = """
Hi there! I am your AI chatbot. I can answer questions about Python, AI, and general topics.
Python is a high-level programming language.
Natural Language Processing enables machines to understand human language.
NLTK stands for Natural Language Toolkit.
Spacy is another powerful NLP library in Python.
AI stands for Artificial Intelligence.
You can use Python for web development, data science, and automation.
"""

# Preprocess corpus
sent_tokens = nltk.sent_tokenize(corpus)
lemmer = nltk.stem.WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token.lower()) for token in tokens if token not in string.punctuation]

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text))

# Greetings
greeting_inputs = ("hello", "hi", "greetings", "hey")
greeting_responses = ["Hi there!", "Hello! How can I help you?", "Hey! What's up?", "Hi! Ask me anything."]

def greet(sentence):
    for word in sentence.split():
        if word.lower() in greeting_inputs:
            return random.choice(greeting_responses)
    return None

# Response generator
def generate_response(user_input):
    robo_response = ''
    temp_tokens = sent_tokens[:]
    temp_tokens.append(user_input)

    vectorizer = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = vectorizer.fit_transform(temp_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf[:-1])

    idx = vals.argsort()[0][-1]
    req_tfidf = vals[0][idx]

    if req_tfidf == 0:
        robo_response = "I'm sorry, I didn't understand that."
    else:
        robo_response = sent_tokens[idx]

    return robo_response

# Chatbot loop
print("BOT: Hello! I am an AI chatbot. Type 'bye' to exit.")

while True:
    user_input = input("YOU: ").lower()
    if user_input == 'bye':
        print("BOT: Goodbye! Have a great day.")
        break
    elif user_input in ('thanks', 'thank you'):
        print("BOT: You're welcome!")
    else:
        greeting = greet(user_input)
        if greeting is not None:
            print(f"BOT: {greeting}")
        else:
            print(f"BOT: {generate_response(user_input)}")
