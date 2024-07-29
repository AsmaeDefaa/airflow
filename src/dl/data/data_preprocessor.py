import json
import re
import nltk
import spacy
from nltk.corpus import stopwords
from bs4 import BeautifulSoup

def process_data(path):

    # Télécharger les listes de mots vides pour le français et l'anglais
    nltk.download('stopwords')
    stop_words_fr = set(stopwords.words('french'))
    stop_words_en = set(stopwords.words('english'))

    # Charger le modèle spaCy pour le français
    nlp_fr = spacy.load("fr_core_news_sm")

    # Charger le contenu JSON en tant que chaîne de caractères
    with open('/Users/aya/Desktop/pipeline/data/raw/'+ path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Fonction pour la lemmatisation en français
    def lemmatize_fr(text):
        doc = nlp_fr(text)
        return ' '.join([token.lemma_ for token in doc])

    # Filtrer les articles ayant des champs null ou vides
    filtered_data = []
    for item in data:
        if all(key in item and item[key] not in [None, ""] for key in ["title", "url", "date", "content"]):
            filtered_data.append(item)

    # Parcourir les éléments filtrés du JSON
    for item in filtered_data:
        for key, value in item.items():
            if key != "url" and value != "":  # Vérifier si le champ n'est pas "url" et n'est pas une chaîne vide
                # Supprimer les balises HTML
                cleaned_text = BeautifulSoup(value, "html.parser").get_text()
                # Normaliser le texte
                normalized_text = cleaned_text.lower()  # Convertir en minuscules
                # Supprimer les caractères spéciaux pour le français et l'anglais
                normalized_text = re.sub(r'[^a-zA-Z0-9\s]', '', normalized_text)
                # Supprimer les mots vides pour le français et l'anglais
                words = normalized_text.split()
                filtered_words_fr = [word for word in words if word not in stop_words_fr]
                filtered_words_en = [word for word in filtered_words_fr if word not in stop_words_en]
                # Lemmatisation pour l'anglais
                lemmatizer = nltk.WordNetLemmatizer()
                lemmatized_words_en = [lemmatizer.lemmatize(word) for word in filtered_words_en]
                # Lemmatisation pour le français
                lemmatized_text_fr = lemmatize_fr(' '.join(filtered_words_fr))
                # Reconstruire le texte lemmatisé
                lemmatized_text = ' '.join(lemmatized_words_en + lemmatized_text_fr.split())
                # Nettoyer le champ de date et supprimer les caractères spéciaux
                if key == "date":
                    cleaned_date = re.sub(r'[^a-zA-Z0-9\s]', '', value)  # Supprimer les caractères spéciaux
                    item[key] = cleaned_date
                else:
                    # Remplacer la valeur par le texte nettoyé, filtré et lemmatisé
                    item[key] = lemmatized_text

    # Enregistrer les articles filtrés et modifiés dans un nouveau fichier JSON
    with open('/Users/aya/Desktop/pipeline/data/preprocessed/'+path, 'w') as f:
        json.dump(filtered_data, f, indent=4)












