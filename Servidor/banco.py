from conta import Conta
from cliente import Cliente
from historico import Historico
import datetime
from pymongo import MongoClient
import hashlib

MONGO_URI = 'mongodb://localhost'

client = MongoClient(MONGO_URI)

db = client['sistema_bancario']
contas = db["contas"]
login = db["login"]
historicos = db["historicos"]

historico = Historico()

class Banco:

    def adciona_conta(self, conta):
        hash = hashlib.sha256(conta._senha.encode('utf-8')).hexdigest()
        contas.insert_one({"Número": conta._numero, "Nome": conta._titular._nome, "CPF": conta._titular._cpf, 
                             "Saldo": conta._saldo, "Usuário": conta._usuario, "Senha": hash, "Limite": conta._limite})
        
    def remove_conta(self, cpf):
        contas.delete_one({'CPF': cpf})

    def verifica_numero_conta(self, numero):
        aux = contas.find_one({"Número": numero})
        if(aux == None):
            return True
        else:
            return False
    
    def verifica_cpf(self, cpf):
        aux = contas.find_one({"CPF": cpf})
        if(aux == None):
            return True
        else:
            return False
    
    def verifica_conta_login(self, usuario, senha):
        hash = hashlib.sha256(senha.encode('utf-8')).hexdigest()
        aux = contas.find_one({'Usuário': usuario, 'Senha': hash})
        if(aux != None):
            return aux
        else:
            return False

    def saca(self, cpf, valor):
       aux1 = contas.find_one({'CPF': cpf})
       if(aux1.get('Saldo') >= valor):
            valor1 = aux1.get('Saldo') - valor
            contas.update_one({'CPF': cpf}, {'$set':{'Saldo': valor1}})
            self.adciona_transacao(aux1.get('CPF'), 'saque', valor)
            return True
       else:
           return False

    def deposita(self, cpf, valor):
        aux1 = contas.find_one({'CPF': cpf})
        if(aux1 != None):
            valor1 = aux1.get('Saldo') + valor
            contas.update_one({'CPF': cpf}, {'$set':{'Saldo': valor1}})
            self.adciona_transacao(aux1.get('CPF'), 'deposito', valor)
            return True
        else:
            return False

    def transfere(self, cpf, destino, valor):
        aux = self.saca(cpf, valor)
        if(aux):
            aux1 = contas.find_one({'Número': destino})
            if(aux1 != None):
                valor_dep = aux1.get('Saldo') + valor
                contas.update_one({'CPF': aux1.get('CPF')}, {'$set':{'Saldo': valor_dep}})
                self.adciona_transf(cpf, aux1.get('Número'), valor)
                return 1
            else:
                return 0
        else:
            return 2

    def extrato(self, cpf):
        aux1 = contas.find_one({'CPF': cpf})
        if(aux1 != None):
            lista = [aux1.get('Nome'),aux1.get('Número'),str(aux1.get('Saldo'))]
            dados = ','.join(lista)
            self.adciona_transacao(aux1.get('CPF'), 'extrato', aux1.get('Saldo'))
            return dados
        else:
            return False
    
    def adciona_transacao(self, user, tipo, valor):
        data = datetime.datetime.today()
        if(tipo == 'saque'):
            historicos.insert_one({'id_user': user, 'Transação': 'saque de {} - Data: {}'.format(valor, data)})
        elif(tipo == 'deposito'):
            historicos.insert_one({'id_user': user, 'Transação': 'Depósito de {} - Data: {}'.format(valor, data)})
        elif(tipo == 'extrato'):
            historicos.insert_one({'id_user': user, 'Transação': 'Tirou extrato - Saldo:{} - Data: {}'.format(valor, data)})
        
    def adciona_transf(self, origem, destino, valor):
        aux = contas.find_one({'Número': destino})
        aux1 = contas.find_one({'CPF': origem})
        data = datetime.datetime.today()
        historicos.insert_one({'id_user': origem, 'Transação': 'Transferência de {} para conta {} - Data: {}'.format(valor, destino, data)})
        historicos.insert_one({'id_user': aux.get('CPF'), 'Transação': 'Transferência de {} recebda da conta {}- Data: {}'.format(valor, aux1.get('Número'), data)})

    def retorna_historico(self, cpf):
        lista = []
        for i in historicos.find({'id_user': cpf}, {'Transação': 1}):
            lista.append(str(i))
        return lista

        """""lista = ",".join(self.transacoes)
        lista = lista.replace(",","\n")
        return lista"""