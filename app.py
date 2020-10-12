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
#PAINEL
@app.route ("/painel", methods=['GET'])
def painel():
    #teste = 'texto da variavel na rota painel do app.py'
    return render_template('painel.html')#, teste=teste
##################################################################################
#CADASTRO USUARIO
@app.route ("/usuario", methods=['GET', 'POST'])
def usuario():
    field=form(request.form)

    if request.method == 'POST' and field.validate():
        nome=request.form['nome']
        email=request.form['email']
        sexo=request.form['sexo']
        json={'nome':nome, 'email':email, 'sexo':sexo}
        

        mongo.db.users.insert_one(json)
        flash('Cadastro efetuado!')
        return redirect ('/')
    return render_template ('usuario.html', field=field)
##################################################################################

#CADASTRO ATIVIDADES
@app.route ("/cadAtividade", methods=['GET', 'POST'])
def cadAtividade():

    field=atvdd(request.form) 

    if request.method == 'POST' and field.validate():
        atividade=request.form['atividade']
        descricao=request.form['descricao']
        json={'atividade':atividade, 'descricao':descricao}
        

        mongo.db.atividades.insert_one(json)
        flash('Cadastro efetuado!')
        return redirect ('/pagAtividades')
    return render_template ('cadAtividade.html', field=field)

#LISTAR ATIVIDADES
@app.route ("/pagAtividades", methods=['GET'])
def pagAtividades():
    itens = mongo.db.atividades.find()
    print (itens)
    return render_template ('pagAtividades.html', itens=itens)

#DELETAR ATIVIDADES
@app.route('/deletar_atividade/<_id>', methods=['GET','DELETE'])
def deleta_atividade(_id):
    mongo.db.atividades.delete_one({'_id': ObjectId(_id)})

    return redirect (url_for('pagAtividades'))

#ALTERAR ATIVIDADES
@app.route('/alterar_atividade/<_id>', methods=['GET', 'POST'])
def alterar_atividade(_id):
    aux = mongo.db.atividades.find_one(({'_id': ObjectId(_id)}))

    field = atvdd(request.form)
    if request.method == 'POST' and field.validate():
        atividade=request.form['atividade']
        descricao=request.form['descricao']
        json={'atividade':atividade, 'descricao':descricao}

        mongo.db.atividades.delete_one({'_id': ObjectId(_id)})
        mongo.db.atividades.insert_one(json)
        
        return redirect (url_for('pagAtividades'))
    return render_template('alterarAtividade.html', itens= aux, field=field)

####################################################################################
#CADASTRO FASES
@app.route ("/cadFase", methods=['GET', 'POST'])
def cadFase():
    field=classefase(request.form) 

    if request.method == 'POST' and field.validate():
        fase=request.form['fase']
        descricao=request.form['descricao']
        json={'fase':fase, 'descricao':descricao}
        

        mongo.db.fases.insert_one(json)
        flash('Cadastro efetuado!')
        return redirect ('/pagFases')
    return render_template ('cadFase.html', field=field)

#LISTAR FASES
@app.route ("/pagFases", methods=['GET'])
def pagFases():
    itens = mongo.db.fases.find()
    print (itens)
    return render_template ('pagFases.html', itens=itens)

#DELETAR FASES
@app.route('/deletar_fase/<_id>', methods=['GET','DELETE'])
def deleta_fase(_id):
    mongo.db.fases.delete_one({'_id': ObjectId(_id)})

    return redirect (url_for('pagFases'))

#ALTERAR FASES
@app.route('/alterar_fase/<_id>', methods=['GET', 'POST'])
def alterar_fase(_id):
    aux = mongo.db.fases.find_one(({'_id': ObjectId(_id)}))

    field = classefase(request.form)
    if request.method == 'POST' and field.validate():
        fase=request.form['fase']
        descricao=request.form['descricao']
        json={'fase':fase, 'descricao':descricao}

        mongo.db.fases.delete_one({'_id': ObjectId(_id)})
        mongo.db.fases.insert_one(json)
        
        return redirect (url_for('pagFases'))
    return render_template('alterarFase.html', itens= aux, field=field)

##################################################################################
#CADASTRO EIXOS
@app.route ("/cadEixo", methods=['GET', 'POST'])
def cadEixo():
    field=classeeixo(request.form) 

    if request.method == 'POST' and field.validate():
        eixo=request.form['eixo']
        descricao=request.form['descricao']
        json={'eixo':eixo, 'descricao':descricao}
        

        mongo.db.eixos.insert_one(json)
        flash('Cadastro efetuado!')
        return redirect ('/pagEixos')
    return render_template ('cadEixo.html', field=field)

#LISTAR EIXOS                   
@app.route ("/pagEixos", methods=['GET'])
def pagEixos():
    itens = mongo.db.eixos.find()
    print (itens)
    return render_template ('pagEixos.html', itens=itens)

#DELETAR EIXOS
@app.route('/deletar_eixo/<_id>', methods=['GET','DELETE'])
def deleta_eixo(_id):
    mongo.db.eixos.delete_one({'_id': ObjectId(_id)})

    return redirect (url_for('pagEixos'))

#ALTERAR EIXOS
@app.route('/alterar_eixo/<_id>', methods=['GET', 'POST'])
def alterar_eixo(_id):
    aux = mongo.db.eixos.find_one(({'_id': ObjectId(_id)}))

    field = classeeixo(request.form)
    if request.method == 'POST' and field.validate():
        eixo=request.form['eixo']
        descricao=request.form['descricao']
        json={'eixo':eixo, 'descricao':descricao}

        mongo.db.eixos.delete_one({'_id': ObjectId(_id)})
        mongo.db.eixos.insert_one(json)
        
        return redirect (url_for('pagEixos'))
    return render_template('alterarEixo.html', itens= aux, field=field)

####################################################################################
#CADASTRO EMPRESAS
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

#LISTAR EMPRESAS                   
@app.route ("/pagEmpresa", methods=['GET'])
def pagEmpresa():
    itens = mongo.db.empresas.find()
    print (itens)
    return render_template ('pagEmpresa.html', itens=itens)

#DELETAR EMPRESA
@app.route('/deletar_empresa/<_id>', methods=['GET','DELETE'])
def deleta_empresa(_id):
    mongo.db.empresas.delete_one({'_id': ObjectId(_id)})

    return redirect (url_for('pagEmpresa'))

#ALTERAR EMPRESA
@app.route('/alterar_empresa/<_id>', methods=['GET', 'POST'])
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

####################################################################################

if __name__ == "__main__":
    app.run(debug=True)