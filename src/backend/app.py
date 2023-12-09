from flask import Flask, redirect, render_template, request, jsonify, url_for
import joblib
import os
from sklearn.exceptions import InconsistentVersionWarning
import warnings

warnings.filterwarnings("ignore", category=InconsistentVersionWarning)

# Obtém o caminho absoluto para o diretório do script
base_path = os.path.abspath(os.path.dirname(__file__))
models_path = os.path.join(base_path, 'models')

app = Flask(__name__, template_folder='templates')

# Função para carregar o modelo
def load_model():
    model_path = os.path.join(models_path, 'sentiment_analysis_model.pkl')
    vectorizer_path = os.path.join(models_path, 'tfidf_vectorizer.pkl')

    model = joblib.load(open(model_path, 'rb'))
    vectorizer = joblib.load(open(vectorizer_path, 'rb'))

    return model, vectorizer

# Carrega o modelo e o vetorizador
model, vectorizer = load_model()

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json['data']
    # Pré-processa e vetoriza os dados
    data_vectorized = vectorizer.transform([data])
    # Faz a predição
    prediction = model.predict(data_vectorized)
    return jsonify({'sentiment': prediction[0]})

@app.route('/')
def home():
    return redirect(url_for('index'))

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/mural')
def mural():
    return render_template('mural.html')

@app.route('/register')
def register():
    return render_template('register.html')



if __name__ == '__main__':
    app.run(debug=True)
