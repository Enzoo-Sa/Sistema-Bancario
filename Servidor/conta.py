from cliente import Cliente
from historico import Historico
import datetime


class Conta:

    __slots__ = ['_numero', '_titular', '_saldo', '_usuario', '_senha', '_limite', 'historico', 'data_transacao']

    def __init__(self, numero, cliente, usuario, senha, limite=10000, saldo = 0):
        self._numero = numero
        self._titular = cliente
        self._saldo = saldo
        self._limite = limite
        self._usuario = usuario
        self._senha = senha
        self.historico = Historico()
        self.data_transacao = datetime.datetime.today()

    @property
    def numero(self):
        return self._numero

    @numero.setter
    def numero(self, numero):
        self._numero = numero
    
    @property
    def usuario(self):
        return self._usuario

    @usuario.setter
    def usuario(self, usuario):
        self._usuario = usuario

    @property
    def senha(self):
        return self._senha

    @senha.setter
    def senha(self, senha):
        self._senha = senha