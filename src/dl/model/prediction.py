import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.python.keras.layers.dense_attention import Attention


def predict(path):
    # Lire le fichier JSON dans un DataFrame
    sample_reviews = pd.read_json(path)

    # Afficher les premières lignes du DataFrame
    print(sample_reviews.head(6))

    # Supposons que les critiques sont dans une colonne appelée 'review'
    reviews = sample_reviews['content'].values

    # Prétraitement des critiques pour la prédiction (par exemple, tokenization et padding)
    # Note: Vous devez avoir un tokenizer préalablement formé pour convertir les critiques en séquences
    # Voici un exemple hypothétique de tokenizer

    # Initialiser un tokenizer avec un vocabulaire maximum de 5000 mots
    tokenizer = Tokenizer(num_words=5000)

    # Mettre à jour le tokenizer avec les textes de vos critiques
    tokenizer.fit_on_texts(reviews)

    # Convertir les critiques en séquences de tokens
    sequences = tokenizer.texts_to_sequences(reviews)

    # Padding des séquences pour qu'elles aient toutes la même longueur que l'entrée du modèle
    X_new = pad_sequences(sequences, maxlen=200)

    # Load the saved model
    model = load_model("c1_model_lstm_0.903.h5",
                       custom_objects={'Attention': Attention})  # Ensure to add custom_objects if Attention layer is custom

    # Faire des prédictions sur les nouvelles critiques
    predictions = model.predict(X_new)

    # Convertir les prédictions en classes (par exemple, 'positive', 'negative', 'neutral')
    predicted_classes = np.argmax(predictions, axis=1)

    # Ajouter les prédictions au DataFrame d'origine
    sample_reviews['predicted_class'] = predicted_classes

    # Afficher les résultats
    return sample_reviews['predicted_class']
