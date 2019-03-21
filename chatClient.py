#! /usr/bin/python3

import socket
import struct
import sys
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
    header = receive_fixed_length_msg(sock, HEADER_LENGTH)  # preberi glavo sporocila (v prvih 2 bytih je dolzina sporocila)
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

    message = header + encoded_message  # najprej posljemo dolzino sporocila, sele nato sporocilo samo
    sock.sendall(message);

napaka = False

# message_receiver funkcija tece v loceni niti
def message_receiver():
    global napaka
    while napaka == False:
        try:
            msg_received = receive_message(sock)
            if len(msg_received) > 0:  # ce obstaja sporocilo
                msg_received_content = msg_received.split("|")
                cas = float(msg_received_content[0])
                h = str(time.localtime(cas).tm_hour)
                m = str(time.localtime(cas).tm_min)
                if len(h) == 1:
                    h = "0" + h
                if len(m) == 1:
                    m = "0" + m
                posiljatelj = msg_received_content[1]
                vsebina = msg_received_content[2]
                print("[%s:%s | %s]: %s" % (h, m, posiljatelj, vsebina))  # izpisi
        except RuntimeError:
            print("Napaka: strežnik ni dosegljiv.")
            napaka = True
            sock.close()
            sys.exit()

# pridobi uporabniško ime
badUsername = True
while badUsername == True:
    username = input("Uporabniško ime: ")
    for i in range(len(username)):
        if username[i] == " " or username[i] == "@" or username[i] == "|":
            print("Neveljaven znak uporabniškega imena: \"" + username[i] + "\"")
            badUsername = True
            break
        else:
            badUsername = False

# povezi se na streznik
print("[system] connecting to chat server ...")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", PORT))
print("[system] connected!")
send_message(sock, username)

# zazeni message_receiver funkcijo v loceni niti
thread = threading.Thread(target=message_receiver)
thread.daemon = True
thread.start()

# pocakaj da uporabnik nekaj natipka in poslji na streznik
while napaka == False:
    try:
        msg_send = input("")
        nedovoljen_znak = False
        for i in range(len(msg_send)):
            if msg_send[i] == "|":
                nedovoljen_znak = True
                break
        if nedovoljen_znak == False:
            if msg_send[0] == "@":
                naslovnik = msg_send.split(" ")[0].split("@")[1]
                i = len(naslovnik) + 2
            else:
                naslovnik = ""
                i = 0
            send_message(sock,str(time.time()) + "|" + username + "|" + naslovnik + "|" + msg_send[i:])
        else:
            print("Napaka: nedovoljen znak: \"|\"")
    except KeyboardInterrupt:
        sock.close()
        sys.exit()
