import datetime

class Historico:

    __slots__ = ['data_abertura']

    def __init__(self):
        self.data_abertura = datetime.datetime.today()
    
    """def adciona_transacao(self, user, tipo, valor):
        if(tipo == 'saque'):
            historicos.insert_one({'id_user': user, 'Transação': 'saque de {}'.format(valor)})
        elif(tipo == 'deposito'):
            historicos.insert_one({'id_user': user, 'Transação': 'Depósito de {}'.format(valor)})
        elif(tipo == 'extrato'):
            historicos.insert_one({'id_user': user, 'Transação': 'Tirou extrato - Saldo:{}'.format(valor)})

    def retorna_historico(self):
        user = banco.retorna_user()
        aux = historicos.find({'CPF': user.get('CPF')}, {'Transação': 1})
        print(aux)

        lista = ",".join(self.transacoes)
        lista = lista.replace(",","\n")
        return lista"""