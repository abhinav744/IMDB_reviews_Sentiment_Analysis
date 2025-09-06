import streamlit as st
import pandas as pd
from zipfile import ZipFile
import os
import json
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load tokenizer and model
@st.cache_resource
def load_trained_objects():
    tokenizer = Tokenizer(num_words=5000)
    
    # Load dataset to fit tokenizer (or you can save/load tokenizer separately)
    data = pd.read_csv('IMDB Dataset.csv')
    tokenizer.fit_on_texts(data["review"])
    
    model = load_model('trained_model.h5')
    return tokenizer, model

tokenizer, model = load_trained_objects()

def predict_sentiment(review):
    sequence = tokenizer.texts_to_sequences([review])
    padded_sequence = pad_sequences(sequence, maxlen=200)
    prediction = model.predict(padded_sequence)
    return "Positive 😊" if prediction[0][0] > 0.5 else "Negative 😞"

# Streamlit UI
st.title("🎥 IMDb Movie Review Sentiment Analyzer")

st.write(
    "Enter a movie review below, and the model will predict if the sentiment is Positive or Negative."
)

review_input = st.text_area("Write your movie review here...", height=150)

if st.button("Predict Sentiment"):
    if not review_input.strip():
        st.warning("⚠️ Please enter a valid movie review.")
    else:
        result = predict_sentiment(review_input)
        st.success(f"Predicted Sentiment: {result}")
