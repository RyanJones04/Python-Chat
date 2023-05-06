import socket
import threading
from hashlib import sha256

s = socket.socket()
host = input("Please enter a valid IP Address: ")
port = int(input("Please enter a valid Port: "))
while True:
    try:
        s.bind((host, port))
        print("[+] Server binded succesfully!")
        break
    except:
        print("[-] Unable to bind, trying again!")
        pass
s.listen(2)

chatters = {}
IDs = []

def clients(client, info, ID):
    def resetAccountList():
        global accounts
        accounts = []
        with open("accounts", "r") as accountFile:
            for account in accountFile:
                smallList = account.split(":")
                accounts.append(smallList)
    
    def checkUsernameAvail(name):
        for account in accounts:
            if account[0] == name:
                return False
        return True
    
    def getAccIndex(name):
        i = -1
        for account in accounts:
            i += 1
            if account[0] == name:
                break
        return i

    while True:
        status = client.recv(1024).decode()
        client.send("Y".encode())
        username = client.recv(1024).decode()
        client.send("Y".encode())
        password = client.recv(1024).decode()
        client.send("Y".encode())
        hashedWord = sha256(password.encode("utf-8")).hexdigest()
        resetAccountList()
        if status == "Create":
            if checkUsernameAvail(username):
                with open("accounts", "a") as accountFile:
                    accountFile.write(username+":"+hashedWord+"\n")
                resetAccountList()
                client.send("OK".encode())
                break
            else:
                client.send("NO".encode())
        elif status == "Login":
            if checkUsernameAvail(username) != True:
                accIndex = getAccIndex(username)
                if hashedWord == accounts[accIndex][1][:-1]:
                    try: 
                        test = chatters[username]
                        client.send("NOL".encode())
                    except:
                        client.send("OK".encode())
                        break
                else:
                    client.send("NO".encode())
            else:
                client.send("NO".encode())
            
    print(f"[+] {username} has connected from {info[0]}")
    chatters[username] = client
    while True:
        try:
            print("Ready!")
            name = client.recv(1024)
            msg = client.recv(1024)
            if len(name) < 1:
                raise Exception("Client Died")
            print(f"Recived {msg} from {name}")
            for names in chatters:
                c = chatters[names]
                c.send(name)
                c.send(msg)
            print("Sent all")
        except:
            print("[-]", info[0], "has disconnected!")
            IDs.pop(IDs.index(ID))
            del chatters[username]
            break

while True:
    conn, addr = s.accept()

    i = 0
    while True:
        i += 1
        if i not in IDs:
            current = i
            IDs.append(i)
            IDs.sort()
            break
    threading._start_new_thread(clients, (conn, addr, current))
