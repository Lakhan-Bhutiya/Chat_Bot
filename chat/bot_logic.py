import re
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.conf import settings
from .models import QuestionAnswer

# Ensure NLTK data is available
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

class ChatBot:
    def __init__(self):
        self.vectorizer = None
        self.question_vectors = None
        self.df = None
        self.stop_words = set(stopwords.words("english"))
        self.lemmatizer = WordNetLemmatizer()
        self.HIGH_THRESHOLD = 0.60
        self.MEDIUM_THRESHOLD = 0.40
        self.is_loaded = False

    def clean_text(self, text: str) -> str:
        if not isinstance(text, str):
            return ""
        text = text.lower()
        text = re.sub(r"[^a-z\s]", "", text)
        tokens = nltk.word_tokenize(text)
        cleaned = [
            self.lemmatizer.lemmatize(token)
            for token in tokens
            if token not in self.stop_words
        ]
        return " ".join(cleaned)

    def load_data(self):
        print("Loading ChatBot data...")
        # Load from Database
        qas = list(QuestionAnswer.objects.all().values('question', 'answer'))
        if not qas:
            print("No data found in QuestionAnswer model.")
            self.df = pd.DataFrame(columns=['question', 'answer', 'clean_question'])
            self.is_loaded = True
            return

        self.df = pd.DataFrame(qas)
        self.df["clean_question"] = self.df["question"].apply(self.clean_text)
        
        self.vectorizer = TfidfVectorizer()
        self.question_vectors = self.vectorizer.fit_transform(self.df["clean_question"])
        self.is_loaded = True
        print("ChatBot data loaded successfully.")

    def get_response(self, user_input):
        if not self.is_loaded or self.df is None or self.df.empty:
            self.load_data()
            if self.df is None or self.df.empty:
                return "I have no knowledge yet. Please add questions in the Admin Panel."

        cleaned_input = self.clean_text(user_input)
        
        # Handle empty input or stopwords only
        if not cleaned_input.strip():
             return "Please ask a specific question."

        user_vector = self.vectorizer.transform([cleaned_input])

        similarity_scores = cosine_similarity(user_vector, self.question_vectors)[0]
        
        best_index = np.argmax(similarity_scores)
        best_score = similarity_scores[best_index]

        if best_score >= self.HIGH_THRESHOLD:
            return self.df.iloc[best_index]["answer"]
        
        elif best_score >= self.MEDIUM_THRESHOLD:
            top_3 = similarity_scores.argsort()[-3:][::-1]
            suggestions = [self.df.iloc[idx]['question'] for idx in top_3]
            return "Did you mean one of these questions?\n" + "\n".join([f"- {s}" for s in suggestions])
        
        else:
            return "I'm not sure about that. Please check the question and try again."

# Global instance
chatbot = ChatBot()
