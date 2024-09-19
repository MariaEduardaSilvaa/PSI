from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

database = 'database.db'

def obter_conexao():
    db = sqlite3.connect(database)
    db.row_factory = sqlite3.Row
    return db

#Este construtor permite a criação de instâncias de usuários
# utilizando argumentos variáveis
class User(UserMixin):
    _hash : str
    _hash2 : str
    def __init__(self, **kwargs):
        self._id = None
        if 'matricula' in kwargs.keys():
            self._matricula = kwargs['matricula']
        if 'email' in kwargs.keys():
            self._email = kwargs['email']
        if 'password' in kwargs.keys():
            self._password = kwargs['password']
        if 'hash' in kwargs.keys():
            self._hash = kwargs['hash']
        if 'hash2' in kwargs.keys():
            self._hash2 = kwargs['hash2']
        
    # 5 - sobresrever get id do UserMixin
    def get_id(self):
        return str(self._id)

    
    # usada para definir senha como uma propriedade
    @property
    def _password(self):
        return self._hash
    
    # limita o acesso a senha para atribuição de valor
    # sempre salva o hash a partir da senha
    @_password.setter
    def _password(self, password):
        self._hash = generate_password_hash(password)


    @property
    def _email(self):
        return self._hash2
    
    # limita o acesso a senha para atribuição de valor
    # sempre salva o hash a partir da senha
    @_email.setter
    def _email(self, email):
        self._hash2 = generate_password_hash(email)
    
    
    # ----------métodos para manipular o banco--------------#
    def save(self):        
        db = obter_conexao()  
        cursor = db.cursor()      
        cursor.execute("INSERT INTO users(matricula ,email, password) VALUES (?,?,?)", (self._matricula, self._hash2, self._hash))
        # salva o id no objeto recem salvo no banco
        self._id = cursor.lastrowid
        db.commit()
        db.close()
        return True
    
    #Verifica se um usuário com determinada matrícula existe no banco de dados.
    @classmethod
    def get(cls,user_id):
        db = obter_conexao()
        user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        db.close()
        if user:
            loaduser = User(matricula=user['matricula'], hash2=user['email'] , hash=user['password'])
            loaduser._id = user['id']
            return loaduser
        else:
            return None
    
    @classmethod
    def exists(cls, matricula):
        db = obter_conexao()
        user = db.execute("SELECT * FROM users WHERE matricula = ?", (matricula,)).fetchone()
        db.close()
        if user: #melhorar esse if-else
            return True
        else:
            return False

#Retorna uma lista de todos os usuários no banco de dados.
    @classmethod
    def all(cls):
        db = obter_conexao()
        users = db.execute("SELECT id, matricula FROM users").fetchall()
        db.close()
        return users
    
#Busca um usuário pela matrícula.
    @classmethod
    def get_by_matricula(cls,matricula):
        db = obter_conexao()
        user = db.execute("SELECT id, matricula, email, password FROM users WHERE matricula = ?", (matricula,)).fetchone()
        db.close()
        return user
    
        
    

    
