import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download required NLTK data if missing
try:
    stop_words = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords')
    nltk.download('punkt')
    stop_words = set(stopwords.words('english'))


def clean_text(text):
    text = text.lower()

    # Remove special characters
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)

    # Tokenize text
    try:
        words = word_tokenize(text)
    except LookupError:
        nltk.download('punkt')
        words = word_tokenize(text)

    # Remove stopwords and short words
    filtered_words = [
        word for word in words
        if word not in stop_words and len(word) > 2
    ]

    return filtered_words