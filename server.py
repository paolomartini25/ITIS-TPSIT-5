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

def inserimento(nick, addr):
    cur = con.cursor()
    cur.execute(f"INSERT INTO utenti VALUES ('{nick}','{addr[0]}',{addr[1]})") #i text (stringhe) vanno separate da apici singoli
    con.commit()
    #dizionario[nik] = addr[0]
    cur.close()
    

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
        print (messaggio)
        
        if messaggio.split(":")[0].lower() == "nickname":
            inserimento(messaggio.split(":")[1], addr)
            s.sendto("ok".encode(), addr)
        
        if (messaggio.split(":")[0].lower() == "sender"):
            divisione = messaggio.split(",")
            sender = divisione[0].split(":")[1]
            reciver = divisione[1].split(":")[1]
            mess = divisione[2]
            trovato, indirizzo = richiestaADDR(reciver)
            if trovato:
                print (f"Mando un messaggio a: {reciver} => {indirizzo[0]}")
                #s.sendto(f"Da {sender}: {mess}".encode(), indirizzo)
            else: 
                print(f"ERRORE: {reciver} non trovato!")

if __name__ == "__main__":
    main()



        
    
    