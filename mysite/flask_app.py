#
# Palestra
# Arduino Day 2023
#
# Autores:
#   Arnott Ramos Caiado
#   Ayrton Maia
#   Samantha Pimentel
#

from flask import Flask, request, render_template,json
import os
import time

os.environ["TZ"] = "America/Recife"
time.tzset()

header_key = '*'

app = Flask(__name__)

class Luzes():
    def __init__(self):
        self.colar=False
        self.janela=False
        self.olhos=False
        self.status=False

    def setaLuzes( self, tipo ) :
        if tipo == "colar" :
            self.colar = True
        if tipo == "janela" :
            self.janela = True
        if tipo == "olhos" :
            self.olhos = True
        if tipo == "todos" :
            self.colar = True
            self.janela = True
            self.olhos = True
        return

    def verLuzes(self) :
        if self.colar == True and self.janela == True and self.olhos == True :
            return "todos"
        elif self.colar == True :
            return 'colar'
        elif self.janela == True :
            return 'janela'
        elif self.olhos == True :
            return 'olhos'
        return 'Null'

    def apagaLuzes (self) :
        self.colar=False
        self.janela=False
        self.olhos=False
        self.status=False
        return

###Rotas
modeloUm = Luzes()

# rota para exemplificar interacao com front
#
@app.route('/interacao', methods=['GET','POST'])
def interacao():
    if request.method == 'GET' :
        return render_template("interacao_modelo.html", valor="none")
    if request.method == 'POST' :
        valor = request.form.get('valor')
        modeloUm.setaLuzes( valor )
        return render_template("interacao_modelo.html", valor=valor)

###Funções Arduíno - Lilypad --------------------
# rota para retornar ao dispositivo IOT o estado da interacao das luzes
# muda estado para apagado apos verificar estado
@app.route('/statusmodelo', methods=['GET', 'POST'])
def testaget():
    valor = modeloUm.verLuzes()
    modeloUm.apagaLuzes()
    return  str(valor)

if __name__ == '__main__':
    app.run()