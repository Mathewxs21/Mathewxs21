from flask_login import UserMixin
import sqlite3

def obter_conexao():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

class User(UserMixin):
    id : str
    def __init__(self, email, senha, matricula):
        self.matricula = matricula
        self.email = email
        self.senha = senha

    @classmethod
    def get(cls, id):
        conexao = obter_conexao()
        SELECT = 'SELECT * FROM usuarios WHERE id=?'
        dados = conexao.execute(SELECT, (id,)).fetchone()
        user = User(dados['matricula'], dados['email'], dados['senha'])
        user.id = dados['id']
        return user
    
    @classmethod
    def exists(cls, matricula):
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE matricula = ?", (matricula,))
        user = cursor.fetchone()
        conn.close()
        return user is not None 
    
    @classmethod
    def cadastrados(cls):
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios")
        users = cursor.fetchall()
        conn.close()
        return users
    
    @classmethod
    def get_by_matricula(cls, matricula):
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE matricula = ?", (matricula,))
        user = cursor.fetchone()
        conn.close()
        return user
    
    @classmethod
    def get_dados(cls, id):
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id,))
        user = cursor.fetchone()
        conn.close()
        if user:
            usuario = User(matricula=user['matricula'] , email=user['email'], senha=user['senha'])
            usuario.id = user['id']
            return usuario
        else:
            return None