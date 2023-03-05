import socket
import sys
import time
import traceback
sys.path.insert(0, '/home/pi/picar-4wd')
import picar_4wd as fc
from picar_4wd.utils import *
from picar_4wd.speed import *


HOST = "192.168.86.87" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)

def respond(data: str, direction: str):
    try:
        if data == b"forward":
            if (direction == "backward"):
                fc.stop()
            else:
                fc.forward(50)
            direction = "forward"
        elif data == b"backward":
            if (direction == "forward"):
                fc.stop()
            else:
                fc.backward(50)
            direction = "backward"
        elif data == b"right":
            if (direction == "left"):
                fc.stop()
            else:
                fc.turn_right(50)
            direction = "right"
        elif data == b"left":
            if (direction == "right"):
                fc.stop()
            else:
                fc.turn_left(50)
            direction = "left"
    except Exception:
        traceback.print_exc()
    return direction

def carMetrics():
    try:
        power = power_read()
        cpu_temp = cpu_temperature()
        cpu = cpu_usage()
        metrics = "power:" + str(power) + ",temp:" + str(cpu_temp) + ",cpu:" + str(cpu)
        return metrics
    except Exception:
        traceback.print_exc()
    return "ope"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    direction = "forward"
    try:
        while 1:
            client, clientInfo = s.accept()
            #print("server recv from: ", clientInfo)
            data = client.recv(1024)      # receive 1024 Bytes of message in binary format
            if data != b"":
                received = data.decode() 
                direction = respond(data, direction)    
                client.sendall(carMetrics().encode()) # Echo back to client
    except: 
        print("Closing socket")
        client.close()
        s.close()    
