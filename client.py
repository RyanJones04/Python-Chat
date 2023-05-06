import tkinter as tk
import socket
import threading

s = socket.socket()

msgs = {}
no = False
correct = ""
available = ""

class Chat(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("500x500")
        self.showFrame(Connect)

    def showFrame(self, frame):
        frame(self).pack()
    
    def replaceScreen(self, newFrame):
        _list = self.winfo_children()
        for child in _list:
            child.destroy()
        self.showFrame(newFrame)

class Connect(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="#111111")
        self.config(width = 500, height = 500, bg = "#111111")
        self.pack_propagate(False)
        tk.Label(self, text = "", bg="#111111").pack()
        tk.Label(self, text = "IP ADDRESS", bg="#111111", fg="#ffffff").pack()
        self.ip = tk.Entry(self)
        self.ip.pack()
        tk.Label(self, text = "", bg="#111111").pack()
        tk.Label(self, text = "PORT", bg="#111111", fg="#ffffff").pack()
        self.port = tk.Entry(self)
        self.port.pack()
        tk.Label(self, text = "", bg="#111111").pack()
        tk.Button(self, text = "SUBMIT", width = 10, height = 1, command = lambda: self.setConnect(master)).pack()
    
    def setConnect(self, master):
        global host, port
        host = self.ip.get()
        port = self.port.get()
        s.connect((host, int(port)))
        master.replaceScreen(Login)


class Login(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="#111111")
        self.config(width = 500, height = 500, bg = "#111111")
        self.pack_propagate(False)
        tk.Label(self, text = "", bg="#111111").pack()
        tk.Label(self, text = "LOGIN", bg="#111111", fg="#ffffff").pack()
        if correct == "NO":
            tk.Label(self, text = "", bg="#111111").pack()
            tk.Label(self, text = "Username or password incorrect!", bg="#111111", fg="#ffffff").pack()
        elif correct == "NOL":
            tk.Label(self, text = "", bg="#111111").pack()
            tk.Label(self, text = "This user is already logged in!", bg="#111111", fg="#ffffff").pack()
        tk.Label(self, text = "", bg="#111111").pack()
        tk.Label(self, text = "USERNAME", bg="#111111", fg="#ffffff").pack()
        self.username = tk.Entry(self)
        self.username.pack()
        tk.Label(self, text = "", bg="#111111").pack()
        tk.Label(self, text = "PASSWORD", bg="#111111", fg="#ffffff").pack()
        self.password = tk.Entry(self)
        self.password.pack()
        tk.Label(self, text = "", bg="#111111").pack()
        tk.Button(self, text = "SUBMIT", width = 10, height = 1, command = lambda: self.setLogin(master)).pack()
        tk.Label(self, text = "", bg="#111111").pack()
        tk.Button(self, text = "CREATE ACC", width = 10, height = 1, command = lambda: master.replaceScreen(CreateAcc)).pack()

    def setLogin(self, master):
        global username, correct
        status = "Login"
        username = self.username.get()
        password = self.password.get()
        if username != "" and password != "":
            s.send(status.encode())
            s.recv(1024)
            s.send(username.encode())
            s.recv(1024)
            s.send(password.encode())
            s.recv(1024)
            correct = s.recv(1024).decode()
            if correct == "OK":
                master.replaceScreen(CombinedFrame)
            elif correct == "NO" or correct == "NOL":
                master.replaceScreen(Login)
        
class CreateAcc(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="#111111")
        self.config(width = 500, height = 500, bg = "#111111")
        self.pack_propagate(False)
        tk.Label(self, text = "", bg="#111111").pack()
        tk.Label(self, text = "CREATE ACCOUNT", bg="#111111", fg="#ffffff").pack()
        if available == "NO":
            tk.Label(self, text = "", bg="#111111").pack()
            tk.Label(self, text = "That username is already taken!", bg="#111111", fg="#ffffff").pack()
        tk.Label(self, text = "", bg="#111111").pack()
        tk.Label(self, text = "USERNAME", bg="#111111", fg="#ffffff").pack()
        self.username = tk.Entry(self)
        self.username.pack()
        tk.Label(self, text = "", bg="#111111").pack()
        tk.Label(self, text = "PASSWORD", bg="#111111", fg="#ffffff").pack()
        self.password = tk.Entry(self)
        self.password.pack()
        tk.Label(self, text = "", bg="#111111").pack()
        tk.Button(self, text = "SUBMIT", width = 10, height = 1, command = lambda: self.setCreate(master)).pack()
        tk.Label(self, text = "", bg="#111111").pack()
        tk.Button(self, text = "LOGIN", width = 10, height = 1, command = lambda: master.replaceScreen(Login)).pack()
    
    def setCreate(self, master):
        global username, available
        status = "Create"
        username = self.username.get()
        password = self.password.get()
        if username != "" and password != "":
            s.send(status.encode())
            s.recv(1024)
            s.send(username.encode())
            s.recv(1024)
            s.send(password.encode())
            s.recv(1024)
            available = s.recv(1024).decode()
            if available == "OK":
                master.replaceScreen(CombinedFrame)
            elif available == "NO":
                master.replaceScreen(CreateAcc)

class MessageFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.config(width = 500, height = 420, bg = "#111111")
        self.pack_propagate(False)
        for msg in msgs:
            tk.Label(self, text = msg[:len(msg)-1]+": "+msgs.get(msg), font = ("calibri", 13), bg = "#111111", fg = "#ffffff").pack(anchor = "nw")

class SendFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.config(width = 500, height = 80, bg = "#888888")
        self.pack_propagate(False)
        self.msg = tk.Text(self, width = 48)
        self.msg.pack(side = "left", padx = 5, pady = 15)
        self.b = tk.Button(self, text = "SEND", width = 10, height = 2, command = lambda: self.send(master))
        self.b.pack(side = "left", padx = 5)
        if no != True:
            threading._start_new_thread(self.recive, (master,))

    
    def send(self, master):
        self.msg = self.msg.get("1.0", "end")
        self.msg = self.msg.strip()
        if self.msg != "":
            s.send(username.encode())
            s.send(self.msg.encode())
            print(f"sent {self.msg}")
        else:
            master.master.replaceScreen(CombinedFrame)
    
    def recive(self, master):
        global no
        no = True
        while True:
            self.name = s.recv(1024).decode()
            self.msg = s.recv(1024).decode()
            print(f"Recived {self.msg} from {self.name}")
            i = 0
            while True:
                if self.name+str(i) not in msgs:
                    self.name += str(i)
                    break
                i += 1
            msgs[self.name] = self.msg
            master.master.replaceScreen(CombinedFrame)

class CombinedFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.config(width = 500, height = 500, bg = "#111111")
        self.pack_propagate(False)
        MessageFrame(self).pack()
        SendFrame(self).pack()

chat = Chat()
chat.mainloop()
