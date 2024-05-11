import socket

# Configuración del servidor
HOST = '0.0.0.0'  # Escuchar en todas las interfaces de red
PORT = 12345       # Puerto de escucha

# Crear un socket TCP/IP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Enlazar el socket al servidor
server_socket.bind((HOST, PORT))

# Escuchar conexiones entrantes
server_socket.listen(1)
print(f"Esperando conexiones en el puerto {PORT}...")

# Aceptar la conexión
client_socket, client_address = server_socket.accept()
print(f"Conexión desde {client_address}")

while True:
    # Recibir datos del cliente
    data = client_socket.recv(1024)
    if not data:
        break  # Si no hay datos, salir del bucle
    
    # Procesar los datos recibidos
    instruction = data.decode('utf-8')
    print(f"Instrucción recibida: {instruction}")

# Cerrar la conexión
client_socket.close()
server_socket.close()
