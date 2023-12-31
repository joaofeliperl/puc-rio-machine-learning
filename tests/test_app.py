import re
import pytest
import nltk
from backend.app import app, load_model
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sklearn.preprocessing import LabelEncoder

# Download dos stopwords
nltk.download('stopwords')

# Função para pré-processamento de texto
def preprocess_text(text):
    # Remove pontuações e caracteres especiais
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Converte para minúsculas
    text = text.lower()
    # Remove stopwords em português
    stop_words = set(nltk.corpus.stopwords.words('portuguese'))
    text = ' '.join([word for word in text.split() if word not in stop_words])
    return text

# Use 'client' do Flask para simular requisições HTTP
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Use 'model' e 'vectorizer' para carregar o modelo e vetorizador
model, vectorizer = load_model()

# Função de teste para verificar se o modelo atende aos requisitos de desempenho
def test_model_performance(client):
    # Dados de teste (substitua por dados reais do seu domínio)
    test_comments = ["This is a positive comment.", "This is a negative comment."]
    true_labels = [1, 0]  # 1 para positivo, 0 para negativo

    # Pré-processa e vetoriza os dados
    data_vectorized = vectorizer.transform([preprocess_text(comment) for comment in test_comments])

    # Faz as predições usando o modelo
    predictions_prob = model.predict_proba(data_vectorized)
    predictions = model.classes_[np.argmax(predictions_prob, axis=1)]

    # Use LabelEncoder para converter as classes para inteiros
    label_encoder = LabelEncoder()
    predictions_binary = label_encoder.fit_transform(predictions)

    # Threshold de acurácia (substitua por threshold real)
    accuracy = np.mean(predictions_binary == true_labels)

    # Verifica se a acurácia atende ao threshold
    accuracy_threshold = 0.8
    
    assert accuracy >= accuracy_threshold, f"Model accuracy ({accuracy}) abaixo do threshold ({accuracy_threshold})"

# Função de teste para verificar se o modelo atende aos requisitos de desempenho para frases positivas
def test_model_performance_positive(client):
    # Dados de teste para frases positivas
    test_comments = ["This is a positive comment.", "I love this product!"]
    true_labels = [1, 1]  # 1 para positivo

    # Pré-processa e vetoriza os dados
    data_vectorized = vectorizer.transform([preprocess_text(comment) for comment in test_comments])

    # Faz as predições usando o modelo
    predictions_prob = model.predict_proba(data_vectorized)
    predictions = model.classes_[np.argmax(predictions_prob, axis=1)]

    # Use LabelEncoder para converter as classes para inteiros
    label_encoder = LabelEncoder()
    predictions_binary = label_encoder.fit_transform(predictions)

    # Threshold de acurácia (substitua por threshold real)
    accuracy = np.mean(predictions_binary == true_labels)

    # Verifica se a acurácia atende ao threshold
    accuracy_threshold = 0.8
    assert accuracy >= accuracy_threshold, f"Model accuracy ({accuracy}) abaixo do threshold ({accuracy_threshold}) para frases positivas"


# Função de teste para verificar se o modelo atende aos requisitos de desempenho para frases negativas
def test_model_performance_negative(client):
    # Dados de teste para frases negativas
    test_comments = ["This is a negative comment.", "I do not like this product."]
    true_labels = [0, 0]  # 0 para negativo

    # Pré-processa e vetoriza os dados
    data_vectorized = vectorizer.transform([preprocess_text(comment) for comment in test_comments])

    # Faz as predições usando o modelo
    predictions_prob = model.predict_proba(data_vectorized)
    predictions = model.classes_[np.argmax(predictions_prob, axis=1)]

    # Use LabelEncoder para converter as classes para inteiros
    label_encoder = LabelEncoder()
    predictions_binary = label_encoder.fit_transform(predictions)

    # Threshold de acurácia (substitua por threshold real)
    accuracy = np.mean(predictions_binary == true_labels)

    # Verifica se a acurácia atende ao threshold
    accuracy_threshold = 0.8
    assert accuracy >= accuracy_threshold, f"Model accuracy ({accuracy}) abaixo do threshold ({accuracy_threshold}) para frases negativas"
