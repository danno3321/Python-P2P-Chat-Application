from _thread import *
import socket, os, math, sys, emoji, threading



HOST = '127.0.0.1'
PORT = 2000

# Listen for messages from the other device. Second thread connects to here
def receive_messages(connection):
    sending = True
    try:
        while sending:
            data = connection.recv(4096)
            a = data.decode("utf-8")
            if a == "!q!q!q!q!q" or a == "":
                print("\n\n\n---------------------------------------------\nPartner has left the chat.")
                print("Press Enter to Terminate Application\n---------------------------------------------")
                conn.close()
                break
            else:
                #TODO: Implement character by character check for colons to search for emojis, use emojize to print them
                numChars = len(a)
                i = 0
                endPrint = 0
                while i < numChars:
                    if a[i] == ':' :
                        j = i + 1
                        while j < numChars:
                            if a[j] == ':':
                                try:
                                    if endPrint == 0:
                                        print(a[0:i], emoji.emojize(a[i:j+1]), end="")
                                    else:
                                        print(a[endPrint:i], emoji.emojize(a[i:j+1]), end = "")
                                    i = j
                                    endPrint = i + 1
                                    break
                                except:
                                    print(a[i:j+1],end="")
                                    i = j
                                    endPrint = j + 1
                                    break
                            j += 1
                    i += 1
                if endPrint == 0:
                    print(a)
                elif endPrint < numChars:
                    print(a[endPrint:numChars])
                else:
                    print("")
                #TODO: Once emoji handler code is written, copy receive_messages to Client
    except:
        sys.exit()
    sys.exit(0)

# Entry point of the program
name = input("Enter your name: ")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    wait = input("Wait for connection? (y/n) ")
    global conn, client
    if wait == "y":
        s.bind((HOST, PORT))
        s.listen()
        print("Server Listening")
        conn, client = s.accept()
    else:
         target = input("Please input the IP of the target host: ")
         tPort = input("Please input the port # to use at the target IP: ")
         conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         conn.connect((target, int(tPort)))
    sending = True
    try:
        print("\n\n\n---------------------------------------------\nConnection established!")
        print("Type your message and press Enter to send.")
        print("To terminate chat, type '!q!q!q!q!q' or\n press Enter with an empty line.\n\nBeginning chat...\n---------------------------------------------\n")
        x = threading.Thread(target=receive_messages, args=(conn,))
        x.start()

        while (sending == True):
            message = input("")
            if message == "!q!q!q!q!q" or message == "":
                conn.send("!q!q!q!q!q".encode('utf-8'))
                sending = False
                conn.close()
                print("\n\n---------------------------------------------\nLeaving Chat...\n---------------------------------------------")
            else:
                conn.send("{}-> {}".format(name, message).encode('utf-8'))
    except:
        sys.exit()
    sys.exit(0)