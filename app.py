from bson import ObjectId
from flask import Flask, jsonify
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)



# Remplacez <password> par le mot de passe réel de l'utilisateur admin
mongo_uri = "mongodb+srv://admin:admin@cluster0.kyw13ev.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(mongo_uri)
db = client['prediction']  # Remplacez par le nom de votre base de données

@app.route('/')
def getAll():
    # Exemple de requête à la base de données
    collection = db['article']  # Remplacez par le nom de votre collection
    document = collection.find_one()

    if document:
        # Convertir l'ObjectId en string et retourner le document
        document['_id'] = str(document['_id'])
        return jsonify(document)
    else:
        return jsonify({"error": "Document not found"}), 404


@app.route('/documents', methods=['GET'])
def get_all_documents():
    collection = db['article']
    documents = collection.find().limit(150)
    result = []

    for document in documents:
        document['_id'] = str(document['_id'])
        result.append(document)

    return jsonify(result)

@app.route('/positif', methods=['GET'])
def positif():
    collection = db['article']  # Remplacez par le nom de votre collection
    count = collection.count_documents({"predicted_class": 2})
    return jsonify({"count": count})


@app.route('/negatif', methods=['GET'])
def negatif():
    collection = db['article']  # Remplacez par le nom de votre collection
    count = collection.count_documents({"predicted_class": 0})
    return jsonify({"count": count})


@app.route('/neutre', methods=['GET'])
def neutre():
    collection = db['article']  # Remplacez par le nom de votre collection
    count = collection.count_documents({"predicted_class": 1})
    return jsonify({"count": count})



@app.route('/documents/<id>', methods=['GET'])
def get_by_id(id):
    collection = db['article']  # Remplacez par le nom de votre collection
    try:
        document = collection.find_one({"_id": ObjectId(id)})
    except:
        return jsonify({"error": "Invalid ObjectId"}), 400

    if document:
        document['_id'] = str(document['_id'])
        return jsonify(document)
    else:
        return jsonify({"error": "Document not found"}), 404


@app.route('/count_source_africa', methods=['GET'])
def count_source_africa():
    collection = db['article']  # Remplacez par le nom de votre collection
    count = collection.count_documents({"source": "africa"})
    return jsonify({"count": count})


@app.route('/count_source_atalayar', methods=['GET'])
def count_source_atalayara():
    collection = db['article']  # Remplacez par le nom de votre collection
    count = collection.count_documents({"source": "atalyar"})
    return jsonify({"count": count})




@app.route('/count_source_africa_and_predicted_class_positif', methods=['GET'])
def count_source_africa_and_predicted_class_positif():
    collection = db['article']  # Remplacez par le nom de votre collection
    count = collection.count_documents({"source": "africa", "predicted_class": 2})
    return jsonify({"count": count})


@app.route('/count_source_africa_and_predicted_class_negatif', methods=['GET'])
def count_source_africa_and_predicted_class_negatif():
    collection = db['article']  # Remplacez par le nom de votre collection
    count = collection.count_documents({"source": "africa", "predicted_class": 0})
    return jsonify({"count": count})


@app.route('/count_source_atalyar_and_predicted_class_positif', methods=['GET'])
def count_source_atalyar_and_predicted_class_positif():
    collection = db['article']  # Remplacez par le nom de votre collection
    count = collection.count_documents({"source": "atalyar", "predicted_class": 2})
    return jsonify({"count": count})


@app.route('/count_source_atalyar_and_predicted_class_negatif', methods=['GET'])
def count_source_atalyar_and_predicted_class_negatif():
    collection = db['article']  # Remplacez par le nom de votre collection
    count = collection.count_documents({"source": "atalyar", "predicted_class": 0})
    return jsonify({"count": count})







if __name__ == '__main__':
    app.run(debug=False)
