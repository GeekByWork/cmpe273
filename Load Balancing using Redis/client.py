import socket

host = ''
port = 8000
server = "0.0.0.0:5003/v1/expenses/1"
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
request = "GET / HTTP/1.1\nHost: "+server+"\n\n"


s.connect((host,port))

s.send("hello")

while True:
    d=s.recv(1024)
    if d=="":
        break
    print d
s.close()
print "Connection Closed"