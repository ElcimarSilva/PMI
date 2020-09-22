from wtforms import Form, StringField, validators
from wtforms.fields.html5 import EmailField

class form(Form):
    nome=StringField('Nome: ', [validators.length(min=2, max=10, message='Nome invalido min 2 max 10')])
    email=EmailField('Email: ', [validators.length(min=2, max=20, message='Email invalido')])

class atvdd(Form):
    atividade=StringField('Atividade: ', [validators.length(min=2, max=10, message='Atividade invalida min 2 max 10')])
    descricao=StringField('Descrição: ', [validators.length(min=2, max=20, message='Descrição invalida')])

class startup(Form):
    empresa=StringField('Empresa: ', [validators.length(min=2, max=10, message='Empresa invalida min 2 max 10')])
    descricao=StringField('Descrição: ', [validators.length(min=2, max=20, message='Descrição invalida')])

class classefase(Form):
    fase=StringField('Fase: ', [validators.length(min=2, max=10, message='Fase invalida min 2 max 10')])
    descricao=StringField('Descrição: ', [validators.length(min=2, max=30, message='Fase invalida')])

class classeeixo(Form):
    eixo=StringField('Eixo: ', [validators.length(min=2, max=10, message='Fase invalida min 2 max 10')])
    descricao=StringField('Descrição: ', [validators.length(min=2, max=30, message='Fase invalida')])
