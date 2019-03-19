#! /usr/bin/python3

import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)
import socket
import struct
import threading
import time

PORT = 8081
HEADER_LENGTH = 2


def receive_fixed_length_msg(sock, msglen):
    message = b''
    while len(message) < msglen:
        chunk = sock.recv(msglen - len(message))  # preberi nekaj bajtov
        if chunk == b'':
            raise RuntimeError("socket connection broken")
        message = message + chunk  # pripni prebrane bajte sporocilu

    return message


def receive_message(sock):
    header = receive_fixed_length_msg(sock,
                                      HEADER_LENGTH)  # preberi glavo sporocila (v prvih 2 bytih je dolzina sporocila)
    message_length = struct.unpack("!H", header)[0]  # pretvori dolzino sporocila v int

    message = None
    if message_length > 0:  # ce je vse OK
        message = receive_fixed_length_msg(sock, message_length)  # preberi sporocilo
        message = message.decode("utf-8")

    return message


def send_message(sock, message):
    encoded_message = message.encode("utf-8")  # pretvori sporocilo v niz bajtov, uporabi UTF-8 kodno tabelo

    # ustvari glavo v prvih 2 bytih je dolzina sporocila (HEADER_LENGTH)
    # metoda pack "!H" : !=network byte order, H=unsigned short
    header = struct.pack("!H", len(encoded_message))

    message = header + encoded_message  # najprj posljemo dolzino sporocilo, slee nato sporocilo samo
    sock.sendall(message);


# funkcija za komunikacijo z odjemalcem (tece v loceni niti za vsakega odjemalca)
def client_thread(client_sock, client_addr, client_username):
    global clients

    print("[system] connected with " + client_addr[0] + ":" + str(client_addr[1]) + " - " + client_username)
    print("[system] we now have " + str(len(clients)) + " clients")
    for client in clients:
        if client[0] != client_sock:
            send_message(client[0], str(time.time()) + "|RKchat|Pridružil se nam je uporabnik " + client_username)

    try:

        while True:  # neskoncna zanka
            msg_received = receive_message(client_sock)
            msg_received_content = msg_received.upper().split("|")
            cas         = msg_received_content[0]
            posiljatelj = msg_received_content[1]
            naslovnik   = msg_received_content[2]
            vsebina     = msg_received_content[3]

            if not msg_received:  # ce obstaja sporocilo
                break
            if naslovnik != "":
                # pošlji zasebno sporočilo
                obstaja = False
                for client in clients:
                    if client[1] == naslovnik:
                        send_message(client[0], cas + "|" + posiljatelj + "|" + vsebina + " (private)")
                        obstaja =  True
                if obstaja == False: # naslovnik ne obstaja
                    send_message(client_sock, str(time.time()) + "|RKchat|Napaka: uporabniško ime ne obstaja.")
            else:
                # pošlji javno sporočilo
                for client in clients:
                    if client[0] != client_sock:
                        send_message(client[0], cas + "|" + posiljatelj + "|" + vsebina + " (public)")

            print("[" + posiljatelj + "] " + vsebina)

    except:
        # tule bi lahko bolj elegantno reagirali, npr. na posamezne izjeme. Trenutno kar pozremo izjemo
        pass

    # prisli smo iz neskoncne zanke
    print("[system] " + client_addr[0] + ":" + str(client_addr[1]) + " - " + client_username + " disconnected")
    with clients_lock:
        clients.remove((client_sock, client_username))
    print("[system] we now have " + str(len(clients)) + " clients")
    for client in clients:
        send_message(client[0], str(time.time()) + "|RKchat|Uporabnik " + client_username + " je odšel")
    client_sock.close()


# kreiraj socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", PORT))
server_socket.listen(1)

# cakaj na nove odjemalce
print("[system] listening ...")
clients = set()
clients_lock = threading.Lock()
while True:
    try:
        # pocakaj na novo povezavo - blokirajoc klic
        client_sock, client_addr = server_socket.accept()
        client_username = receive_message(client_sock).upper()
        with clients_lock:
            clients.add((client_sock, client_username))

        thread = threading.Thread(target=client_thread, args=(client_sock, client_addr, client_username));
        thread.daemon = True
        thread.start()

    except KeyboardInterrupt:
        break

print("[system] closing server socket ...")
server_socket.close()
