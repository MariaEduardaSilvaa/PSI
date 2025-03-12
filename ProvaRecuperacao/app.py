from flask import Flask, render_template, url_for, redirect, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from database import db
from database.models import User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'muitodificil'

db.init_app(app)

#Cria o banco
with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user



@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        confirmar_senha = request.form['confirmar_senha']

        if senha != confirmar_senha:
            flash ("As senhas não são equivalentes")
        else:
            if User.query.filter_by(email=email).first():
                flash("Email já cadastrado!")

            else:
                User.cadastrar(nome, email, senha)
                return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        user = User.query.filter_by(email=email).first()
        if user and User.verificar_senha(senha):
            login_user(user)
            return redirect(url_for('inicial'))
        else:
            flash('Email ou senha inválidos')
    return render_template('login.html')

@app.route('/inicial')
def inicial():
    posts = Post.listar()
    return render_template("inicial.html", posts=posts)

@app.route('/criar_post', methods=['POST', 'GET'])
@login_required
def criar_post():
    if request.method == 'POST':
        conteudo = request.form['conteudo']
        user_id = current_user.get_id()
        Post.cadastrar_post(conteudo,user_id)
    return render_template('criar_post.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))