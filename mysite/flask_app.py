#
# Palestra
# Arduino Day 2023
#
# Autores: 
#   Arnott Ramos Caiado
#   Ayrton
#   Samantha Pimentel


from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, render_template,json,redirect
#from flask.wrappers import Response
#import git
from datetime import datetime
import os
import time


os.environ["TZ"] = "America/Recife"
time.tzset()

header_key = '*'

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://Recnplay2022:2507phph@Recnplay2022.mysql.pythonanywhere-services.com/Recnplay2022$default'
db = SQLAlchemy(app)

class votos(db.Model):
    id_voto = db.Column(db.Integer,primary_key=True)
    data = db.Column(db.String(20))
    hora = db.Column(db.Time)
    nome_modelo = db.Column(db.String(20),nullable=False)

    def to_json(self):
        return {"id": self.id_voto,"data": self.data, "hora": self.hora, "nome_modelo": self.nome_modelo }

class curtidas(db.Model):
    id_curtida = db.Column(db.Integer,primary_key=True)
    data = db.Column(db.String(20))
    hora = db.Column(db.Time)
    nome_modelo = db.Column(db.String(20),nullable=False)

    def to_json(self):
        return {"id": self.id_voto,"data": self.data, "hora": self.hora, "nome_modelo": self.nome_modelo}


###Rotas

colarStatus="OFF"
janelaStatus="OFF"
olhosStatus="OFF"

@app.route('/interacao', methods=['GET','POST'])
def interacao():
    global colarStatus
    global olhosStatus
    global janelaStatus
    if request.method == 'GET' :
        return render_template("interacao_modelo.html", valor="none")
    if request.method == 'POST' :
        valor = request.form.get('valor')
        if valor == 'colar' :
            colarStatus = 'ON'
        elif valor == 'janela':
            janelaStatus = 'ON'
        elif valor == 'olhos' :
            olhosStatus = 'ON'
        return render_template("interacao_modelo.html", valor=valor)

@app.route('/galeria')
def galeria():
    return render_template("galeria.html")

@app.route('/look1')
def look1():
    try :
        curtido = curtidas.query.filter(curtidas.nome_modelo.like("Play1"))
        return render_template("look1.html", curtida=curtido.count() )
    except :
        return render_template("look1.html", curtida=" " )



@app.route('/cardin')
def cardin():
    return render_template("cardin.html")

@app.route('/sobrenos')
def sobre():
    return render_template("sobrenos.html")

@app.route('/votacao')
def vote():
    return render_template("votacao.html")

@app.route('/arduino')
def arduino():
    return render_template("arduino.html")

@app.route('/')
def principal():
    return render_template("principal.html")


@app.route('/voto', methods = ['GET','POST'])
def inserir():
    if request.method == 'POST' :
        try:
            data, hora = takeDataHora()
            nome_modelo=str("M01")
            novo = votos(data=data,hora=hora, nome_modelo=nome_modelo)
            db.session.add(novo)
            db.session.commit()
            return render_template("votacao.html")
        except :
            return render_template("votacao.html")
    else : # se o methodo for GET ou outro
        try :
            return render_template("votacao.html")
        except :
            return render_template("votacao.html")



@app.route('/curtida', methods = ['GET','POST'])
def curtir1():
    if request.method == 'POST' :
        try:
            data, hora = takeDataHora()
            nome_modelo=str("Play1")
            novo = curtidas(data=data,hora=hora, nome_modelo=nome_modelo)
            db.session.add(novo)
            db.session.commit()
            curtido = curtidas.query.filter(curtidas.nome_modelo.like("Play1"))
            return render_template("look1.html", curtida=curtido.count() )
        except :
            return render_template("look1.html", curtida=" " )
    else : # se o methodo for GET ou outro
        try :
            curtido = curtidas.query.filter(curtidas.nome_modelo.like("Play1"))
            return render_template("look1.html", curtida=curtido.count() )
        except :
            return render_template("look1.html", curtida=" " )



def takeDataHora():
    data = str(datetime.today().strftime("%d/%m/%Y"))
    hora = str(datetime.time(datetime.now()))
    hora = hora[0:8]
    return data, hora

@app.route('/consulta', methods=['GET'])
def consulta():
    try:
        consulta = votos.query.filter(votos.nome_modelo.like("M01"))
        return str(consulta.count())
    except:
        consulta = votos.query.filter(votos.nome_modelo.like("M01"))
        return str(consulta.count())


@app.route('/busca', methods=['GET'])
def busca():
    consulta=  curtidas.query.all()
    curtir=[]
    for c in consulta:
        curtir.append({'id': c.id_voto,'data': c.data, 'hora': c.hora, 'nome do modelo': c.nome_modelo })
    return json.dumps(curtir)

###Funções Arduíno
statusModeloUm = "Null"

@app.route('/setamodelo', methods=['GET','POST'])
def setamodelo():
    dados = request.get_json()
    valor = dados["valor"]
    global statusModeloUm
    statusModeloUm = valor
    return {"Stat Modelo Um": statusModeloUm}

@app.route('/statusmodeloum', methods=['GET', 'POST'])
def testaget():
    global statusModeloUm
    valor = statusModeloUm
    statusModeloUm = "Null"
    return  str(valor)

if __name__ == '__main__':
    app.run()