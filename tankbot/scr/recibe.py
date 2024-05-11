import socket
from time import sleep as delay
import sys
sys.path.append('/root/Desktop/embedded-labs/tankbot')
from libs.tiva import *

from gpiozero import Servo
from time import sleep
servo = Servo(27)
servo.value=-1
HOST = '192.168.200.51'  # Reemplaza con la dirección IP de tu PC
PORT = 8081  # Puerto de conexión

# Crear un socket TCP/IP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Vincular el socket al host y puerto
server_socket.bind((HOST, PORT))

# Escuchar conexiones entrantes (máximo de 1)
server_socket.listen(1)

print(f"Esperando conexiones en {HOST}:{PORT}...")

# Aceptar la conexión entrante
client_connection, client_address = server_socket.accept()
print(f"Conexión establecida desde {client_address}")
tiva1 = InitSerial(baud=9600)
motors = Motors(serial_instance=tiva1)
caja=Gripper(serial_instance=tiva1)
# Bucle para recibir mensajes
men=""
servo.value=-1
try:
    while True:
        data = client_connection.recv(1024)
        if not data:
            break  # Si no hay datos, cerrar la conexión
        print(f"Mensaje recibido: {data.decode('utf-8')}")
        men=data.decode('utf-8')
        if men=="OPEN":
            motors.stop()
            delay(0.2)
            caja.move(-100)
            delay(3)
            caja.move(0)
            delay(6)
            caja.move(100)
            delay(4)
            caja.move(0)
            servo.value=0
            delay(4)
            motors.stop()
        elif men=="ADELANTE":
            caja.move(0)
            motors.stop()
            delay(1.5)
            motors.move(140,120)
            delay(1)
        else:
            motors.move(-83,73)
            servo.value=-1

except KeyboardInterrupt:
    motors.move(0,0)

# Cerrar la conexión
client_connection.close()
server_socket.close()
