import time
from flask import Flask, redirect, render_template, request, jsonify, session, url_for, flash
import joblib
import os
from sklearn.exceptions import InconsistentVersionWarning
import warnings
from flask_mysqldb import MySQL
import pymysql
import requests

warnings.filterwarnings("ignore", category=InconsistentVersionWarning)

base_path = os.path.abspath(os.path.dirname(__file__))
models_path = os.path.join(base_path, 'models')

app = Flask(__name__, template_folder='templates')

app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'user_gamer'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

while True:
    try:
        connection = pymysql.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            db=app.config['MYSQL_DB']
        )
        cursor = connection.cursor()
        print("Conexão com o servidor MySQL estabelecida com sucesso!")
        break
    except pymysql.MySQLError as e:
        print("Não foi possível estabelecer conexão com o servidor MySQL:", str(e))
        print("Tentando novamente em 5 segundos...")
        time.sleep(5)

def load_model():
    model_path = os.path.join(models_path, 'sentiment_analysis_model.pkl')
    vectorizer_path = os.path.join(models_path, 'tfidf_vectorizer.pkl')

    model = joblib.load(open(model_path, 'rb'))
    vectorizer = joblib.load(open(vectorizer_path, 'rb'))

    return model, vectorizer

model, vectorizer = load_model()

@app.route('/')
def home():
    return redirect(url_for('index'))

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/mural')
def mural():
    return render_template('mural.html')

@app.route('/ratings')
def ratings():
    game_ranking = get_game_ranking()

    if game_ranking:
        return render_template('ratings.html', game_ranking=game_ranking)
    else:
        return render_template('ratings.html', game_ranking=[])

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/cadastro', methods=['POST'])
def cadastrar_usuario():
    try:
        nome = request.form['username']
        email = request.form['email']
        senha = request.form['password']

        if not nome or not email or not senha:
            flash('Por favor, preencha todos os campos.', 'danger')
            return redirect(url_for('register'))

        cursor = connection.cursor()
        cursor.execute("INSERT INTO cadastrar (nome, email, senha) VALUES (%s, %s, %s)", (nome, email, senha))
        connection.commit()
        cursor.close()

        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('login'))

    except Exception as e:
        app.logger.error("Erro durante o cadastro: %s", str(e))
        flash('Erro durante o cadastro. Tente novamente mais tarde.', 'danger')
        return redirect(url_for('register'))

@app.route('/autenticacao', methods=['GET', 'POST'])
def login():
    email = None
    senha = None

    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('password')

        cur = connection.cursor()
        cur.execute("SELECT * FROM cadastrar WHERE email = %s AND senha = %s", (email, senha))
        user = cur.fetchone()
        cur.close()

        if user:
            return redirect(url_for('mural'))

    return render_template('login.html')

@app.route('/get_game_data_by_slug/<slug>', methods=['GET'])
def get_game_data_by_slug(slug):
    game_data = get_game_data_by_slug(slug)

    if game_data:
        return jsonify(game_data)
    else:
        return jsonify({'error': 'Jogo não encontrado'}), 404

def get_game_data_by_slug(slug):
    api_key = '94a728c53f63486e98e4a6a65385649d'
    url = f'https://api.rawg.io/api/games/{slug}?key={api_key}'

    try:
        response = requests.get(url)
        response.raise_for_status()

        game_data = response.json()

        if game_data:
            name = game_data.get('name', 'Nome do Jogo não disponível')
            background_image = game_data.get('background_image', 'caminho/para/a/imagem.jpg')
            description = game_data.get('description', 'Descrição do jogo.')
            slug = game_data.get('slug', 'Slug.')

            return {
                'name': name,
                'background_image': background_image,
                'description': description,
                'slug': slug
            }
        else:
            return None

    except requests.exceptions.RequestException as e:
        print(f'Erro ao obter dados da API: {e}')
        return None

def get_comments_by_slug(slug):
    try:
        connection = mysql.connection
        cursor = connection.cursor()
        query = "SELECT id_game, slug, comment, rating, sentiment FROM games WHERE slug = %s"
        cursor.execute(query, (slug,))
        comments = cursor.fetchall()
        return comments
    except Exception as e:
        print(f"Erro ao obter comentários: {str(e)}")
        return []
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()

@app.route('/games/<slug>')
def games(slug):
    try:
        game_data = get_game_data_by_slug(slug)
        comments = get_comments_by_slug(slug)

        if game_data:
            return render_template('games.html', game_slug=slug, game_data=game_data, comments=comments)
        else:
            return render_template('games.html', game_slug=None)

    except Exception as e:
        print(f"Erro na rota /games/{slug}: {str(e)}")
        return render_template('error.html', error_message=str(e))

@app.route('/save_comment_and_rating', methods=['POST'])
def save_comment_and_rating():
    try:
        slug = request.form.get('gameSlug')
        comment = request.form.get('comment')  
        rating = request.form.get('rating')

        cursor = connection.cursor()

        cursor.execute("INSERT INTO games (slug, comment, rating, sentiment) VALUES (%s, %s, %s, %s)",
                       (slug, comment, rating, None))

        data_vectorized = vectorizer.transform([comment])
        prediction = model.predict(data_vectorized)[0]

        cursor.execute("UPDATE games SET sentiment = %s WHERE slug = %s", (prediction, slug))

        connection.commit()
        cursor.close()

        print(f"Prediction for comment '{comment}': {prediction}")

        return redirect(url_for('games', slug=slug))

    except Exception as e:
        app.logger.error("Erro durante o cadastro: %s", str(e))
        return redirect(url_for('mural'))

def get_game_ranking(limit=10):
    try:
        connection = mysql.connection
        cursor = connection.cursor()
        query = """
        SELECT slug, COUNT(*) as frequency, AVG(rating) as average_rating
        FROM games
        GROUP BY slug
        ORDER BY frequency DESC, average_rating DESC
        LIMIT %s
        """
        cursor.execute(query, (limit,))
        ranking = cursor.fetchall()
        return ranking
    except Exception as e:
        print(f"Erro ao obter o ranking de jogos: {str(e)}")
        return []
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()

if __name__ == '__main__':
    app.run(debug=True)
