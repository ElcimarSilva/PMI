from flask import Flask, request, jsonify, Response, redirect, render_template, flash, url_for
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash #biblioteca para criptografar senhas
from bson import json_util
from bson.objectid import ObjectId
from forms import *
from flask_wtf import CSRFProtect
from functools import wraps

app = Flask (__name__)
app.config['MONGO_URI']='mongodb://localhost/pythonmongodb' #Base de dados
mongo = PyMongo(app)
app.secret_key='chavesecreta'
csrf=CSRFProtect(app) #Função do Flask para proteger Form
##################################################################################
#PAINEL
@app.route ("/painel", methods=['GET'])
def painel():
    #teste = 'texto da variavel na rota painel do app.py'
    itens = mongo.db.empresas.find()
    return render_template('painel.html',itens=itens)#, teste=teste
##################################################################################

@app.route("/pagdastartup/<_id>", methods=['GET'])
def pagdastartup(_id):
    itens = mongo.db.empresas.find_one(ObjectId(_id))
    fases = mongo.db.fases.find()
    eixos = mongo.db.eixos.find()
    return render_template ('PagDaStartup.html', itens=itens, fases=fases, eixos=eixos)

@app.route("/atividades_startup/<_id>/<fase>/<eixo>", methods=['GET'])
def atividades_startup(_id, fase=None, eixo=None):
    atividades = mongo.db.atividades.find()

    return render_template ('AtividadesStartup.html', atividades=atividades)

##################################################################################
#Controle de sessão do usuario
def login_required(run):
	@wraps(run)
	def wrap(*args, **kwargs):
		if 'usuario' in session:
			return run(*args, **kwargs)
		else:
			flash('Por favor! Efetue o login primeiro!')
			return redirect(url_for('login'))
	return wrap

@app.route ("/login", methods=['GET', 'POST'])
def login():
    field=login(request.form)

    if request.method == 'POST' and field.validate():
        usuario = request.form['usuario']
        senha = request.form['senha']
        json = {'username': usuario, 'password': senha}
        validacao = mongo.db.users.find_one(json)

        if validacao is None:
            flash ("Usuario ou senha invalido!")
            return redirect (url_for('login'))
        else:
            flash('Bem vindo!')
            return redirect(url_for('base'))
    
    return render_template ('login.html', field=field)

@app.route('/logout')
@login_required
def logout():  #encerra sessão do usuário
    if 'usuario' in session:
        session.pop('usuario')
    return redirect(url_for('login'))
    

#CADASTRO USUARIO
@app.route ("/usuario", methods=['GET', 'POST'])
def usuario():
    field=user(request.form)

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
        
        json={'atividade':atividade, 'descricao':descricao, 'status':False}
        
        mongo.db.atividades.insert_one(json)
        cad_atividades(mongo.db.atividades.find_one({'atividade':atividade}))
        flash('Cadastro efetuado!')
        return redirect ('/pagAtividades')
    return render_template ('cadAtividade.html', field=field)

def cad_atividades(atividade):
    empresas = mongo.db.empresas.find()
    for empresa in empresas:
        for fase in empresa['fases']:
            for eixo in fase['eixos']:
                eixo['atividades'].append(atividade)
        mongo.db.empresas.update({'_id':ObjectId(empresa['_id'])}, empresa)


#LISTAR ATIVIDADES
@app.route ("/pagAtividades", methods=['GET'])
def pagAtividades():
    itens = mongo.db.atividades.find()
    return render_template ('pagAtividades.html', itens=itens)

#DELETAR ATIVIDADES (collection)
@app.route('/deletar_atividade/<_id>', methods=['GET','DELETE'])
def deleta_atividade(_id):
    #deleta_atividades(_id)
    mongo.db.atividades.delete_one({'_id': ObjectId(_id)})

    return redirect (url_for('pagAtividades'))
#deleta dentro dos arrays
@app.route('/deletar_atividades/<_id>', methods=['GET','DELETE'])
def deleta_atividades(_id):
    empresas = mongo.db.empresas.find()
    
    for empresa in empresas:
        for fase in empresa['fases']:
            for eixo in fase['eixos']:
                for at in eixo['atividades']:
                    if ObjectId(at['_id']) == ObjectId(_id):
                    
                        #mongo.db.atividades.delete_one({'_id': ObjectId(_id)})
                        #del at['_id']
                        mongo.db.empresas.update({'_id' :empresa['_id']}, empresa)
                        #mongo.db.empresa.update({}, {'$pull': {'fases':{'$elemMatch': {'eixos': {'$elemMatch':{'atividades': {'_id': ObjectId(_id)}}}}} }})
    return redirect (url_for('pagAtividades'))
 
def set_atividades():
    empresas = mongo.db.empresas.find_one({'_id': ObjectId('5fb46b17c81485997ba8e802')})
    
    for fase in empresas['fases']:
        for eixo in fase['eixos']:
            for at in eixo['atividades']: 
                mongo.db.atividades.insert_one(at)
    
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
        json={'fase':fase, 'descricao':descricao, 'status':False, 'eixos':[]}
        

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
        json={'eixo':eixo, 'descricao':descricao, 'status':False, 'atividades': []}
        

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
    itensfase = mongo.db.fases.find()
    itenseixo = mongo.db.eixos.find()
    itensatividade = mongo.db.atividades.find()

    if request.method == 'POST' and field.validate():
        empresa=request.form['empresa']
        descricao=request.form['descricao']
        valorF=request.form['valorF']
        
                    
        json={'empresa':empresa, 'descricao':descricao, 'valorF':valorF, 'fases':[], 'finalizado':False}
        json=setatividades(seteixos(setfases(json)))
        
        mongo.db.empresas.insert_one(json)
        flash('Cadastro efetuado!')
        return redirect ('/pagEmpresa')
    return render_template ('cadEmpresa.html', field=field)


def setfases(empresa:dict):
    itensfase = mongo.db.fases.find()
    for fase in itensfase:
        empresa['fases'].append(fase)
    return empresa

def seteixos(empresa:dict):
    itenseixo = mongo.db.eixos.find()
    for fase in empresa['fases']:
        for eixo in itenseixo:
            fase['eixos'].append(eixo)
    return empresa

def setatividades(empresa:dict):
    itensatividade = mongo.db.atividades.find()
    for fase in empresa['fases']:
        for eixo in fase['eixos']:
            for atividade in itensatividade:
                eixo['atividades'].append(atividade)
    return empresa


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
    print (request.method)
    if request.method == 'POST' and field.validate():
        print ('============================================')
        empresa=request.form['empresa']
        descricao=request.form['descricao']
        valorF=request.form['valorF']
        json={'empresa': empresa, 'descricao' : descricao, 'valorF': valorF, 'fases':aux['fases']}
        mongo.db.empresas.update({'_id':ObjectId(_id)}, json)

        #mongo.db.empresas.delete_one({'_id': ObjectId(_id)})
        #mongo.db.empresas.insert_one(aux)

        return redirect (url_for('pagEmpresa'))
    return render_template('alterarEmpresa.html', itens= aux, field=field)

####################################################################################

if __name__ == "__main__":
    #set_atividades()
    app.run(debug=True)