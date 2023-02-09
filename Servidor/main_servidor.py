import socket, threading
from conta import Conta
from banco import Banco
from historico import Historico
from cliente import Cliente

banco = Banco()

host = '10.180.43.139'
port = 3000
addr = (host, port)


def menu(con, cliente):
    connect = True
    while(connect):

        ret = con.recv(1024).decode()

        msg = int(ret)

        if(msg == 0):
            pass
        
        elif(msg == 1):
            dados = con.recv(4096).decode()
            lista_dados = dados.split(',')

            aux = banco.verifica_numero_conta(lista_dados[2])
            if(aux):    
                aux1 = banco.verifica_cpf(lista_dados[1])
                if(aux1):
                    cliente = Cliente(lista_dados[0], lista_dados[1])
                    conta = Conta(lista_dados[2], cliente, lista_dados[3], lista_dados[4])
                    banco.adciona_conta(conta)
                    con.send('1'.encode())
                else:
                    con.send('0'.encode())
            else:
                con.send('0'.encode())

        elif(msg == 2):
            dados = con.recv(4096).decode()
            lista_login = dados.split(',')

            user = banco.verifica_conta_login(lista_login[0], lista_login[1])
            if(user != False):
                user_login = user.get('CPF')
                con.send(user_login.encode())
            else:
                con.send('0'.encode())
            
        elif(msg == 4):
            dados = con.recv(4096).decode()
            lista_saque = dados.split(',')
            valor_saque = float(lista_saque[1])

            aux_saq = banco.saca(lista_saque[0], valor_saque)

            if(aux_saq):
                con.send('1'.encode())
            else:
                con.send('0'.encode())
        
        elif(msg == 5):
            dados = con.recv(4096).decode()
            lista_depo = dados.split(',')
            valor_deposito = float(lista_depo[1])

            aux_dep = banco.deposita(lista_depo[0], valor_deposito)

            if(aux_dep):
                con.send('1'.encode())
            else:
                con.send('0'.encode())

        elif(msg == 6):
            dados = con.recv(4096).decode()
            lista_deposito = dados.split(',')
            valor_trans = float(lista_deposito[2])
            aux_trans = banco.transfere(lista_deposito[0], lista_deposito[1], valor_trans)
            
            if(aux_trans == 1):
                con.send('1'.encode())

            elif(aux_trans == 0):
                con.send('0'.encode())

            else:
                con.send('2'.encode())
        
        elif(msg == 7):
            user_extrato = con.recv(4096).decode()
            dados_extrato = banco.extrato(user_extrato)
            if(dados_extrato != False):
                con.send(dados_extrato.encode())
            else:
                con.send('0'.encode())
        
        elif(msg == 8):
            user_remover = con.recv(4096).decode()
            banco.remove_conta(user_remover)
            banco.deslogar()
            con.send('1'.encode())
        
        elif(msg == 9):
            user_historico = con.recv(4096).decode()
            lista_hist = banco.retorna_historico(user_historico)
            lista_hist1 = ','.join(lista_hist)
            con.send(lista_hist1.encode())

def main():
    print("Aguardando conexão...")
    serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv_socket.bind(addr)
    serv_socket.listen()

    while True:
        con, cliente = serv_socket.accept()
        print(cliente,"Conectado!")
        thread = threading.Thread(target=menu, args=(con, cliente))
        thread.start()

if __name__ == "__main__":
    main()