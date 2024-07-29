import json

import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer

from tensorflow.keras.layers import Input, Embedding, Bidirectional, LSTM, Dropout, Dense, Layer
import tensorflow.keras.backend as K

# Define Attention layer
class Attention(Layer):
    def __init__(self, **kwargs):
        super(Attention, self).__init__(**kwargs)

    def build(self, input_shape):
        self.W = self.add_weight(name='attention_weight', shape=(input_shape[-1], input_shape[-1]), initializer='random_normal', trainable=True)
        self.b = self.add_weight(name='attention_bias', shape=(input_shape[-1],), initializer='zeros', trainable=True)
        self.u = self.add_weight(name='context_vector', shape=(input_shape[-1], 1), initializer='random_normal', trainable=True)
        super(Attention, self).build(input_shape)

    def call(self, x):
        uit = K.tanh(K.dot(x, self.W) + self.b)
        ait = K.softmax(K.dot(uit, self.u), axis=1)
        weighted_input = x * ait
        output = K.sum(weighted_input, axis=1)
        return output

    def compute_output_shape(self, input_shape):
        return input_shape[0], input_shape[-1]

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
    model = load_model("/Users/aya/Desktop/pipeline/dags/c2_model_lstm_0.904.h5",
                       custom_objects={'Attention': Attention})  # Ensure to add custom_objects if Attention layer is custom

    # Faire des prédictions sur les nouvelles critiques
    predictions = model.predict(X_new)

    # Convertir les prédictions en classes (par exemple, 'positive', 'negative', 'neutral')
    predicted_classes = np.argmax(predictions, axis=1)

    # Ajouter les prédictions au DataFrame d'origine
    sample_reviews['predicted_class'] = predicted_classes

    sample_reviews = sample_reviews.drop(columns=['date'])

    records = sample_reviews.to_dict(orient='records')
    json_records = json.dumps(records)

    # Retourner les résultats sous forme de JSON avec double quotes
    return json_records