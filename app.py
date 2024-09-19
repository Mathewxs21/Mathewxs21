from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
import sqlite3

login_manager = LoginManager()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SUPERMEGADIFICIL'
login_manager.init_app(app)

def obter_conexao():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def index():
    return render_template('pages/index.html')

@app.route('/cadastrar', methods=['POST', 'GET'])
def registrar():

    if request.method == 'POST':
        matricula = request.form['matricula']
        email = request.form['email']
        senha = request.form['senha']
        hash_senha = generate_password_hash(senha)
        hash_email = generate_password_hash(email)
        
        conn = obter_conexao()
        INSERT = 'INSERT INTO usuarios(matricula,email,senha) VALUES (?,?,?)'
        conn.execute(INSERT, (matricula, hash_email, hash_senha))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))

    return render_template('pages/register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
            matricula = request.form['matricula']
            senha = request.form['senha']
            use = User.get_by_matricula(matricula)
            if use is None:
                flash("ESSE USUÁRIO NÂO FEZ CADASTRO")
                return redirect(url_for('registrar')) 
            if check_password_hash(use['senha'], senha):
                    login_user(User.get_dados(use['id'])) 
                    return redirect(url_for('cadastrar_exc'))
            return redirect(url_for('login'))
        
    return render_template('pages/login.html')

@app.route('/cadastrar_exercicios', methods=['GET','POST'])
@login_required
def cadastrar_exc():

    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form.get('descricao')
        user = request.form['user']

        conn = obter_conexao()
        INSERT = 'INSERT INTO exercicios(nome,descricao,user) VALUES (?,?,?)'
        conn.execute(INSERT, (nome, descricao, user))
        conn.commit()
        conn.close()

    return render_template('pages/cadastrar-exercicios.html')

@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))



