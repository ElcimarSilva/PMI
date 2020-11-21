from wtforms import Form, StringField, validators, PasswordField
from wtforms.fields.html5 import EmailField

class user(Form):
    nome=StringField('Nome', [validators.length(min=2, max=10, message='Nome invalido min 2 max 10')])
    email=EmailField('Email', [validators.length(min=2, max=20, message='Email invalido')])

class login(Form):
    usuario = StringField('Usuário', [validators.length(min=3, max=15, message='Login inválido!')])
    senha = PasswordField('Senha', [validators.length(min=5, max=20, message='Senha inválida!')])

class atvdd(Form):
    atividade=StringField('Atividade', [validators.length(min=2, max=20, message='Atividade invalida min 2 max 10')])
    descricao=StringField('Descrição', [validators.length(min=2, max=50, message='Descrição invalida')])

class startup(Form):
    empresa=StringField('Empresa', [validators.length(min=2, max=15, message='Empresa invalida min 2 max 12')])
    descricao=StringField('Descrição', [validators.length(min=2, max=30, message='Descrição invalida')])
    valorF=StringField('valorF')
    
class classefase(Form):
    fase=StringField('Fase', [validators.length(min=2, max=10, message='Fase invalida min 2 max 10')])
    descricao=StringField('Descrição', [validators.length(min=2, max=30, message='Descrição invalida')])

class classeeixo(Form):
    eixo=StringField('Eixo', [validators.length(min=2, max=15, message='Eixo invalido min 2 max 10')])
    descricao=StringField('Descrição', [validators.length(min=2, max=60, message='Descrição invalida')])
