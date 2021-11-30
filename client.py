import socket as sck
import logging
import threading
import time

IP = "localhost"
PORTA = 5000

s = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)     #socket UDP/IPv4

nikname = input("inserire il nikname: ")
s.sendto(f"Nickname:{nikname}".encode(),(IP, PORTA)) 

def thread_function(name):
    logging.info("Thread %s: inizio",name)
    while True:
        data, _ = s.recvfrom(4096)
        print(data.decode())

def main():
    format = "%(asctime)s : %(message)s"
    logging.basicConfig(format=format,level=logging.INFO,datefmt="%H:%M:%S")
    
    logging.info("Main   : creo il thread")
    x = threading.Thread(target=thread_function,args=(1,), daemon=True)
    logging.info("Main   : eseguo il thread")
    x.start()#avvio del thread x

    while True:
        ricevente = input("Inserire il nikname del destinatario: ")
        messaggio = input("Inserire il messaggio: ")
        s.sendto(f"Sender:{nikname},Recever:{ricevente},{messaggio}".encode(),(str(IP), int(PORTA)))

if __name__ == "__main__":
    main()