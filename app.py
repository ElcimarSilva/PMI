from flask import Flask, request, jsonify, Response, redirect, render_template, flash, url_for
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash #biblioteca para criptografar senhas
from bson import json_util
from bson.objectid import ObjectId
from forms import *
from flask_wtf import CSRFProtect

app = Flask (__name__)
app.config['MONGO_URI']='mongodb://localhost/pythonmongodb' #Base de dados
mongo = PyMongo(app)
app.secret_key='chavesecreta'
csrf=CSRFProtect(app) #Função do Flask para proteget Form

#Rota home de teste
@app.route ("/", methods=['GET'])
def base():
    
    return render_template('base.html')
    
@app.route ("/painel", methods=['GET'])
def painel():
    #teste = 'texto da variavel na rota painel do app.py'
    return render_template('painel.html')#, teste=teste


#Rota formulario de teste (usuario)
@app.route ("/formulario", methods=['GET', 'POST'])
def formulario():
    field=form(request.form)

    if request.method == 'POST' and field.validate():
        nome=request.form['nome']
        email=request.form['email']
        sexo=request.form['sexo']
        json={'nome':nome, 'email':email, 'sexo':sexo}
        

        mongo.db.users.insert_one(json)
        flash('Cadastro efetuado!')
        return redirect ('/')
    return render_template ('formulario.html', field=field)

#CADASTRO DE ATIVIDADES VIA FORM
@app.route ("/cadAtividade", methods=['GET', 'POST'])
def cadAtividade():
    field=atvdd(request.form) 

    if request.method == 'POST' and field.validate():
        atividade=request.form['atividade']
        descricao=request.form['descricao']
        json={'atividade':atividade, 'descricao':descricao}
        

        mongo.db.atividades.insert_one(json)
        flash('Cadastro efetuado!')
        return redirect ('/painel')
    return render_template ('cadAtividade.html', field=field)

#CADASTRO DE FASES VIA FORM
@app.route ("/cadFase", methods=['GET', 'POST'])
def cadFase():
    field=classefase(request.form) 

    if request.method == 'POST' and field.validate():
        fase=request.form['fase']
        descricao=request.form['descricao']
        json={'fase':fase, 'descricao':descricao}
        

        mongo.db.fases.insert_one(json)
        flash('Cadastro efetuado!')
        return redirect ('/painel')
    return render_template ('cadFase.html', field=field)

#CADASTRO DE EIXOS VIA FORM
@app.route ("/cadEixo", methods=['GET', 'POST'])
def cadEixo():
    field=classeeixo(request.form) 

    if request.method == 'POST' and field.validate():
        eixo=request.form['eixo']
        descricao=request.form['descricao']
        json={'eixo':eixo, 'descricao':descricao}
        

        mongo.db.eixos.insert_one(json)
        flash('Cadastro efetuado!')
        return redirect ('/painel')
    return render_template ('cadEixo.html', field=field)


#CADASTRO DE EMPRESAS VIA FORM
@app.route ("/cadEmpresa", methods=['GET', 'POST'])
def cadEmpresa():
    field=startup(request.form) 

    if request.method == 'POST' and field.validate():
        empresa=request.form['empresa']
        descricao=request.form['descricao']
        json={'empresa':empresa, 'descricao':descricao}
        

        mongo.db.empresas.insert_one(json)
        flash('Cadastro efetuado!')
        return redirect ('/pagEmpresa')
    return render_template ('cadEmpresa.html', field=field)

#LISTAR EMPRESAS VIA FORM                   
@app.route ("/pagEmpresa", methods=['GET'])
def pagEmpresa():
    itens = mongo.db.empresas.find()
    print (itens)
    return render_template ('pagEmpresa.html', itens=itens)

#ROTA DELETAR DA PAGINA EMPRESA
@app.route('/deletar/<_id>', methods=['GET','DELETE'])
def deleta_empresa(_id):
    mongo.db.empresas.delete_one({'_id': ObjectId(_id)})

    return redirect (url_for('pagEmpresa'))

#ROTA ALTERAR DA PAGINA EMPRESA
@app.route('/alterar/<_id>', methods=['GET', 'POST'])
def alterar_empresa(_id):
    aux = mongo.db.empresas.find_one(({'_id': ObjectId(_id)}))

    field = startup(request.form)
    if request.method == 'POST' and field.validate():
        empresa=request.form['empresa']
        descricao=request.form['descricao']
        json={'empresa':empresa, 'descricao':descricao}

        mongo.db.empresas.delete_one({'_id': ObjectId(_id)})
        mongo.db.empresas.insert_one(json)
        
        return redirect (url_for('pagEmpresa'))
    return render_template('alterarEmpresa.html', itens= aux, field=field)


if __name__ == "__main__":
    app.run(debug=True)