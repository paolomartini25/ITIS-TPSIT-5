#identifico l'utente grazie a un nome univoco: il nikname
"""
server:
ip address
deve avere un dizionario con chiave il nik e valore l'ip
Messaggio Hello: f"Nickname:{nick-name}"

Messaggio normale: f"Sender:{nik-name},Recever:{nik-ricevente},{messaggio}"
"""

import sqlite3

PORTA = 5000
con = sqlite3.connect("d:\\AA_Paolo_Martini\\scuolapaolo\\TPSIT\\2021-2022\\chat_di_classe\\datadase.db")#aprire un database = connettersi
dizionario = {}
def inserimento(nick, addr):
    dizionario[nick] = addr[0]
    

def richiestaADDR(nick):
    cur = con.cursor()
    ip = ""
    porta = ""
    trovato = True
    for row in cur.execute('SELECT * FROM utenti'):
        if nick in row[0]:
            ip = row[1]
            porta = row[2]

    if ip == "" or porta == "": trovato = True

    return trovato, (ip, porta)


def main():
    
    #cur.execute('''CREATE TABLE Nickname (nick, ip)''')

    import socket as sck
    s = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)
    s.bind(("localhost", PORTA)) #(indirizzo ip della macchina server, porta)
    dizionario = {}

    while True:
        data, addr = s.recvfrom(4096) #dati ricevuti(data), addr è una tupla con indirizzo ip del client e porta del client
        messaggio = data.decode()
        print(messaggio)
        
        if "Nickname" in messaggio:
            inserimento(messaggio.split(":")[1], addr)
            print(messaggio.split(":")[1])
            s.sendto("ok".encode(), addr)
        
        if ("Sender" in messaggio):
            divisione = messaggio.split(",")
            print(divisione)
            sender = divisione[0].split(":")[1]
            print(sender)
            reciver = divisione[1].split(":")[1]
            print(reciver)
            mess = divisione[2]
            print(mess)
            
            if reciver in dizionario:
                print (f"Mando un messaggio a: {reciver} => {dizionario[reciver]}")
                s.sendto(f"Da {sender}: {mess}".encode(), dizionario[reciver])
            else: 
                print(f"ERRORE: {reciver} non trovato!")

if __name__ == "__main__":
    main()



        
    
    