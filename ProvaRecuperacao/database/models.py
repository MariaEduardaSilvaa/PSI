from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column, Session, relationship
from sqlalchemy import create_engine, ForeignKey
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str]
    email: Mapped[str]
    senha: Mapped[str]
    posts: Mapped[list['Post']] = relationship(backref='user')

    def hash_senha(self, senha):
        self.senha = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha, senha)

    @classmethod
    def cadastrar(cls, nome, email, senha):
        novo_user = User(nome=nome, email=email, senha=senha)
        db.session.add(novo_user)
        db.session.commit()


class Post(db.Model):
    __tablename__ = 'posts'
    id: Mapped[int] = mapped_column(primary_key=True)
    conteudo: Mapped[str]
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"))

    @classmethod
    def cadastrar_post(cls, conteudo, user_id):
        novo_post = Post(conteudo=conteudo, user_id=user_id)
        db.session.add(novo_post)
        db.session.commit()

    @classmethod
    def listar(cls):
        return cls.query.all()