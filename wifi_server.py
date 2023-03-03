import socket
import sys
sys.path.insert(0, '/home/pi/picar-4wd')
import picar_4wd as fc

HOST = "24.18.178.149" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)

#make a car
#have it respond to some functions
#start moving

def respond(data: str):
    if data == "forward":
        print("forward")
    elif data == "backward":
        print("backward")
    elif data == "right":
        print("right")
    elif data == "left":
        print("left")
    else:
        print("nope",data)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    try:
        while 1:
            client, clientInfo = s.accept()
            print("server recv from: ", clientInfo)
            data = client.recv(1024)      # receive 1024 Bytes of message in binary format
            if data != b"":
                print(data)
                received = data.decode() 
                respond(data)    
                client.sendall(data) # Echo back to client
    except: 
        print("Closing socket")
        client.close()
        s.close()    