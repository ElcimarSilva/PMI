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


#Rota formulario de teste
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
        return redirect ('/painel')
    return render_template ('cadEmpresa.html', field=field)

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

#########################################################################################################
#CADASTRAR USUARIO
@app.route('/users', methods=['POST'])
def create_user():
    #Recebendo dados
    username = request.json['username'] # 
    password = request.json['password'] #
    email = request.json['email']

    if username and email and password:
        hashed_password = generate_password_hash(password)
        id = mongo.db.users.insert(
            {'username': username, 'email': email, 'password': hashed_password}
        )                            #INSERÇÃO DE USUARIO
        response = {
            'id': str(id),
            'username': username,
            'password': hashed_password,
            'email': email 
        }
        return response
    else:     
        return not_found()

    #print (request.json)
    return {'mensagem': 'recebido'}

#LISTAR USUARIOS
@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype='application/json')

#LISTAR USUARIO COM ID
@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(user)
    return Response (response, mimetype="application/json")

#DELETAR USUARIOS
@app.route('/users/<id>', methods=['DELETE'])
def detele_user(id):
    mongo.db.users.delete_one({'_id': ObjectId(id)})
    response = jsonify({'mensagem': 'Usuario' + id + 'foi deletado com sucesso!'})
    return response

#ATUALIZAR USUARIO
@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    if username and email and password:
        hashed_password = generate_password_hash(password)
        mongo.db.users.update_one({'_id': ObjectId(id)}, {'$set': {
            'username': username,
            'password': hashed_password,
            'email': email
        
        }})
        response = jsonify({'mensagem': 'Usuario ' + id + 'foi atualizado com sucesso!'})
        return response

#TRATAMENTO DE ERRO
@app.errorhandler (404)
def not_found(error=None):
    response = jsonify({
        'message': 'Recurso não encontrado!' + request.url,
        'status': 404    
    })
    response.status_code = 404
    return response

###################################################################################

#CADASTRAR EMPRESA
@app.route('/empresas', methods=['POST'])
def create_empresa():
    #Recebendo dados
    empresa = request.json['empresa'] # 
    descricao = request.json['descricao']

    if empresa and descricao :
        id = mongo.db.empresas.insert(
            {'empresa': empresa, 'descricao': descricao, }
        )                            #INSERÇÃO DE EMPRESA
        response = {
            'id': str(id),
            'empresa': empresa,
            'descricao': descricao 
        }
        return response
    else:     
        return not_found()

    #print (request.json)
    return {'mensagem': 'recebido'}

#LISTAR EMPRESAS
@app.route('/empresas', methods=['GET'])
def get_empresas():
    empresas = mongo.db.empresas.find()
    response = json_util.dumps(empresas)
    return Response(response, mimetype='application/json')

#LISTAR USUARIO COM ID
@app.route('/empresas/<id>', methods=['GET'])
def get_empresa(id):
    empresa = mongo.db.empresas.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(empresa)
    return Response (response, mimetype="application/json")

#DELETAR EMPRESA
#@app.route('/empresas/<id>', methods=['DELETE'])
#def detele_empresa(id):
#    mongo.db.empresas.delete_one({'_id': ObjectId(id)})
#    response = jsonify({'mensagem': 'Empresa' + id + 'foi deletada com sucesso!'})
#    return response

#ATUALIZAR EMPRESA
@app.route('/empresas/<id>', methods=['PUT'])
def update_empresa(id):
    empresa = request.json['empresa']
    descricao = request.json['descricao']
    
    if empresa and descricao:
        mongo.db.empresas.update_one({'_id': ObjectId(id)}, {'$set': {
            'empresa': empresa,
            'descricao': descricao
        
        }})
        response = jsonify({'mensagem': 'Empresa ' + id + 'foi atualizada com sucesso!'})
        return response

###################################################################################
#CADASTRAR FASES
@app.route('/fases', methods=['POST'])
def create_fase():
    #Recebendo dados
    fase = request.json['fase'] # 
    descricao = request.json['descricao']

    if fase and descricao :
        id = mongo.db.fases.insert(
            {'fase': fase, 'descricao': descricao, }
        )                            #INSERÇÃO DE FASE
        response = {
            'id': str(id),
            'fase': fase,
            'descricao': descricao 
        }
        return response
    else:     
        return not_found()

    #print (request.json)
    return {'mensagem': 'recebido'}

#LISTAR FASES
@app.route('/fases', methods=['GET'])
def get_fases():
    fases = mongo.db.fases.find()
    response = json_util.dumps(fases)
    return Response(response, mimetype='application/json')

#LISTAR FASES COM ID
@app.route('/fases/<id>', methods=['GET'])
def get_fase(id):
    fase = mongo.db.fases.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(fase)
    return Response (response, mimetype="application/json")

#DELETAR FASES
@app.route('/fases/<id>', methods=['DELETE'])
def detele_fase(id):
    mongo.db.fases.delete_one({'_id': ObjectId(id)})
    response = jsonify({'mensagem': 'Fase: ' + id + 'foi deletada com sucesso!'})
    return response

#ATUALIZAR FASES
@app.route('/fases/<id>', methods=['PUT'])
def update_fase(id):
    fase = request.json['fase']
    descricao = request.json['descricao']
    
    if fase and descricao:
        mongo.db.fases.update_one({'_id': ObjectId(id)}, {'$set': {
            'fase': fase,
            'descricao': descricao
        
        }})
        response = jsonify({'mensagem': 'Fase ' + id + 'foi atualizada com sucesso!'})
        return response


###################################################################################
#CADASTRAR EIXOS 
#Precisar de uma valor, para que possa ser mostrado no grafico, cada fase possui todos os eixos
@app.route('/eixos', methods=['POST'])
def create_eixo():
    #Recebendo dados
    eixo = request.json['eixo'] # 
    descricao = request.json['descricao']

    if eixo and descricao :
        id = mongo.db.eixos.insert(
            {'eixo': eixo, 'descricao': descricao, }
        )                            #INSERÇÃO DE EIXO
        response = {
            'id': str(id),
            'eixo': eixo,
            'descricao': descricao 
        }
        return response
    else:     
        return not_found()

    #print (request.json)
    return {'mensagem': 'recebido'}

#LISTAR EIXOS
@app.route('/eixos', methods=['GET'])
def get_eixos():
    eixos = mongo.db.eixos.find()
    response = json_util.dumps(eixos)
    return Response(response, mimetype='application/json')

#LISTAR EIXO COM ID
@app.route('/eixos/<id>', methods=['GET'])
def get_eixo(id):
    eixo = mongo.db.eixos.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(eixo)
    return Response (response, mimetype="application/json")

#DELETAR EIXOS
@app.route('/eixos/<id>', methods=['DELETE'])
def detele_eixo(id):
    mongo.db.eixos.delete_one({'_id': ObjectId(id)})
    response = jsonify({'mensagem': 'Eixo: ' + id + 'foi deletada com sucesso!'})
    return response

#ATUALIZAR EIXOS
@app.route('/eixos/<id>', methods=['PUT'])
def update_eixo(id):
    eixo = request.json['eixo']
    descricao = request.json['descricao']
    
    if eixo and descricao:
        mongo.db.eixos.update_one({'_id': ObjectId(id)}, {'$set': {
            'eixo': eixo,
            'descricao': descricao
        
        }})
        response = jsonify({'mensagem': 'Eixo: ' + id + 'foi atualizada com sucesso!'})
        return response

###################################################################################
#CADASTRAR ATIVIDADES
#Toda atividade deve estar vinculada a um eixo
@app.route('/atividades', methods=['POST'])
def create_atividade():
    #Recebendo dados
    atividade = request.json['atividade'] # 
    descricao = request.json['descricao']

    if atividade and descricao :
        id = mongo.db.atividades.insert(
            {'atividade': atividade, 'descricao': descricao, }
        )                            #INSERÇÃO DE ATIVIDADE
        response = {
            'id': str(id),
            'atividade': atividade,
            'descricao': descricao 
        }
        return response
    else:     
        return not_found()

    #print (request.json)
    return {'mensagem': 'recebido'}

#LISTAR ATIVIDADES
@app.route('/atividades', methods=['GET'])
def get_atividades():
    atividades = mongo.db.atividades.find()
    response = json_util.dumps(atividades)
    return Response(response, mimetype='application/json')

#LISTAR ATIVIDADE COM ID
@app.route('/atividades/<id>', methods=['GET'])
def get_atividade(id):
    atividade = mongo.db.atividades.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(atividade)
    return Response (response, mimetype="application/json")

#DELETAR ATIVIDADES
@app.route('/atividades/<id>', methods=['DELETE'])
def detele_atividade(id):
    mongo.db.atividades.delete_one({'_id': ObjectId(id)})
    response = jsonify({'mensagem': 'Atividade: ' + id + 'foi deletada com sucesso!'})
    return response

#ATUALIZAR ATIVIDADES
@app.route('/atividades/<id>', methods=['PUT'])
def update_atividade(id):
    atividade = request.json['atividade']
    descricao = request.json['descricao']
    
    if atividade and descricao:
        mongo.db.atividades.update_one({'_id': ObjectId(id)}, {'$set': {
            'atividade': atividade,
            'descricao': descricao
        
        }})
        response = jsonify({'mensagem': 'Atividade: ' + id + 'foi atualizada com sucesso!'})
        return response


if __name__ == "__main__":
    app.run(debug=True)