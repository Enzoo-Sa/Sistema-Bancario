import socket
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox

ip = '10.180.43.139'
port = 3000
addr = (ip, port)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect(addr)
except:
    print("\nNão foi possível conectar ao servidor!\n")
    exit()

class Login():
    login_user = None

login1 = Login()

def fazer_login():
    usuario = login.lineEdit.text()
    senha = login.lineEdit_2.text()
    if(usuario == "" or senha == ""):
        QMessageBox.information(None, "Alerta!", "Preencha todos os campos!")
    else:
        client_socket.send('2'.encode())
        lista_dados = [usuario,senha]
        dados = ','.join(lista_dados)
        client_socket.send(dados.encode())
        retorno = client_socket.recv(1024).decode()

        if(retorno != 0):
            login1.login_user = retorno
            login.close()
            dashboard.show()
            QMessageBox.information(None, "Alerta!", "Login realizado com sucesso!")

        elif(retorno == 0):
            QMessageBox.information(None, "Alerta!", "Usuário ou senha incorreta!")

def chama_logout():

        login1.login_user = None
        dashboard.close()
        login.show()
        QMessageBox.information(None, "Aviso!", "Logout realizado com sucesso!")


def chama_tela_cadastro():
    login.close()
    cadastro.show()

def cadastrar():
    nome = cadastro.lineEdit.text()
    cpf = cadastro.lineEdit_2.text()
    numConta = cadastro.lineEdit_3.text()
    usuario = cadastro.lineEdit_5.text()
    senha = cadastro.lineEdit_6.text()

    if(nome == "" or cpf == "" or numConta == "" or usuario == "" or senha == ""):
        QMessageBox.information(None, "Alerta!", "Preencha todos os campos!")
    else:
        client_socket.send('1'.encode())
        lista_dados = [nome,cpf,numConta,usuario,senha]
        dados = ','.join(lista_dados)
        client_socket.send(dados.encode())

        retorno = int(client_socket.recv(1024).decode())
        
        if(retorno == 1):
            cadastro.close()
            login.show()
            QMessageBox.information(None, "Aviso!", "Cadastro realizado com sucesso!")

        elif(retorno == 0):
            QMessageBox.information(None, "Aviso!", "CPF ou Número da conta já cadastrado!")

def chama_tela_saque():
    dashboard.close()
    saque.show()

def sacar():
    valor = str(saque.lineEdit.text())
    if(valor == '0'):
        QMessageBox.information(None, "Aviso!", "Valor inválido!")
    else:
        client_socket.send('4'.encode())
        lista_saque = [login1.login_user,valor]
        aux = ','.join(lista_saque)
        client_socket.send(aux.encode())

        retorno = int(client_socket.recv(1024).decode())
            
        if(retorno == 1):
            saque.close()
            dashboard.show()
            QMessageBox.information(None, "Aviso!", "Saque realizado com sucesso!")

        elif(retorno == 0):
            QMessageBox.information(None, "Aviso!", "Saldo insuficiente!")
        
def chama_tela_dashboard():
    saque.close()
    dashboard.show()

def chama_tela_deposito():
    dashboard.close()
    deposito.show()

def chama_deposito():
    valor = str(deposito.lineEdit.text())
    if(valor == '0'):
        QMessageBox.information(None, "Aviso!", "Valor inválido!")
    else:
        client_socket.send('5'.encode())
        aux = [login1.login_user,valor]
        lista_deposito = ','.join(aux)
        client_socket.send(lista_deposito.encode())

        retorno = int(client_socket.recv(1024).decode())
            
        if(retorno == 1):
            deposito.close()
            dashboard.show()
            QMessageBox.information(None, "Aviso!", "Depósito realizado com sucesso!")
        elif(retorno == 0):
            QMessageBox.information(None, "Aviso!", "Erro ao realizar depósito!")
    

def chama_tela_transferencia():
    dashboard.close()
    transferencia.show()

def transferir():
    numConta = transferencia.lineEdit.text()
    valor = transferencia.lineEdit_2.text()
    if(valor == '0'):
        QMessageBox.information(None, "Aviso!", "Valor inválido!")
    else:
        client_socket.send('6'.encode())
        lista_dados = [login1.login_user,numConta,valor]
        dados = ','.join(lista_dados)
        client_socket.send(dados.encode())
    
        retorno = int(client_socket.recv(1024).decode())
            
        if(retorno == 1):
            transferencia.close()
            dashboard.show()
            QMessageBox.information(None, "Aviso!", "Transferência realizada com sucesso!")

        elif(retorno == 0):
            QMessageBox.information(None, "Aviso!", "Número da conta inválido!")

        elif(retorno == 2):
            QMessageBox.information(None, "Aviso!", "Saldo insuficiente!")

def chama_tela_extrato():
    client_socket.send('7'.encode())
    user = login1.login_user
    client_socket.send(user.encode())
    dashboard.close()
    extrato.show()

    retorno = client_socket.recv(1024).decode()

    if(retorno != '0'):
        lista_dados = retorno.split(',')
        extrato.lineEdit.setText(lista_dados[0])
        extrato.lineEdit_2.setText(lista_dados[1])
        extrato.lineEdit_3.setText(lista_dados[2])
    else:
        QMessageBox.information(None, "Aviso!", "Erro ao mostrar extrato!")

def voltar_extrato_dashboard():
    extrato.close()
    dashboard.show()

def deletar_conta():
    client_socket.send('8'.encode())
    user_deletar = login1.login_user
    client_socket.send(user_deletar.encode())
    retorno = int(client_socket.recv(1024).decode())
    if(retorno == 1):
        dashboard.close()
        login.show()
        QMessageBox.information(None, "Aviso!", "Conta excluída com sucesso!")

def voltar_transferencia_dashboard():
    transferencia.close()
    dashboard.show()

def voltar_deposito_dashboard():
    deposito.close()
    dashboard.show()

def voltar_cadastro_login():
    cadastro.close()
    login.show()

def chama_tela_historico():
    dashboard.close()
    historico.show()
    client_socket.send('9'.encode())
    user_historico = login1.login_user
    client_socket.send(user_historico.encode())
    retorno = client_socket.recv(1024).decode()

    lista = retorno.replace(",","\n")

    historico.label_3.setText(lista)


def voltar_historico_dashboard():
    historico.close()
    dashboard.show()

def finalizar():
    client_socket.send('0'.encode())
    client_socket.close()
    login.close()

app = QtWidgets.QApplication([])
login = uic.loadUi("login.ui")
cadastro = uic.loadUi("cadastro.ui")
dashboard = uic.loadUi("dashboard.ui")
saque = uic.loadUi("saque.ui")
deposito = uic.loadUi("deposito.ui")
transferencia = uic.loadUi("transferencia.ui")
extrato = uic.loadUi("extrato.ui")
historico = uic.loadUi("historico.ui")



login.pushButton.clicked.connect(fazer_login)
login.pushButton_2.clicked.connect(chama_tela_cadastro)
cadastro.pushButton_2.clicked.connect(cadastrar)
cadastro.pushButton_3.clicked.connect(voltar_cadastro_login)
dashboard.pushButton_2.clicked.connect(chama_tela_saque)
dashboard.pushButton_3.clicked.connect(chama_tela_deposito)
dashboard.pushButton_5.clicked.connect(chama_tela_extrato)
dashboard.pushButton_6.clicked.connect(chama_tela_historico)
dashboard.pushButton_7.clicked.connect(chama_logout)
dashboard.pushButton_4.clicked.connect(chama_tela_transferencia)
saque.pushButton_8.clicked.connect(sacar)
saque.pushButton_9.clicked.connect(chama_tela_dashboard)
deposito.pushButton_8.clicked.connect(chama_deposito)
deposito.pushButton_9.clicked.connect(voltar_deposito_dashboard)
transferencia.pushButton_8.clicked.connect(transferir)
transferencia.pushButton_9.clicked.connect(voltar_transferencia_dashboard)
extrato.pushButton_8.clicked.connect(voltar_extrato_dashboard)
dashboard.pushButton_8.clicked.connect(deletar_conta)
historico.pushButton_6.clicked.connect(voltar_historico_dashboard)
login.pushButton_3.clicked.connect(finalizar)

login.show()
app.exec()
