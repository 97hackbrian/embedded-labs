import serial as com
from time import sleep
class InitSerial:
    def __init__(self,baud) -> None:
        self.ser=None
        for x in range(11):
            try:
                self.ser=com.Serial(f"/dev/ttyACM{x}",baud,timeout=1)
                if self.ser.is_open:
                    print("Successful to connect in the port ttyACM",x)
                    self.ser.reset_input_buffer()
                    self.ser.reset_output_buffer()
                    break
            except:
                print("Problem to connect to ttyACM",x,"\nTry to connect to the next port")
                #print(f'/dev/ttyACM{x}')
    def send_data(self, *args):
        smg = ",".join(map(str, args))  # Join the arguments into a comma-separated string
        smg += "\n"  # Add a newline character at the end
        self.ser.write(smg.encode('utf-8'))  # Encode the string as bytes and send it


                
        
class Motors:
    num_motor = 1  # Variable de clase para llevar un registro del número de instancias
    
    def __init__(self, serial_instance) -> None:
        self.ser = serial_instance
        self.motor_number = Motors.num_motor  # Asignar el número de motor automáticamente
        Motors.num_motor += 1  # Incrementar el número de instancias

    def move(self, left, right):
        self.ser.send_data(f"motor", left, right)

    def stop(self):
        self.ser.send_data(f"motor", 1, 1)

class LedControl:
    def __init__(self, serial_instance) -> None:
        self.ser = serial_instance

    def write(self, l1, l2, l3, l4):
        # Verifica si los valores son booleanos
        #if not all(isinstance(val, bool) for val in (l1, l2, l3, l4)):
        #    raise ValueError("Los valores deben ser booleanos")
        self.ser.send_data(f"leds", l1, l2, l3, l4)

    def init_system(self,cam=0):
        sequences = [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1), (1, 1, 1, 1), (1, 1, 1, 1),(0, 0, 0,1)]

        for sequence in sequences:
            try:
                self.write(*sequence)
                if self.ser.ser.is_open:
                    print(".", end="", flush=True)  # Establece end="" para evitar el salto de línea
                if cam != 0:
                    if cam.is_open():  # Comprueba si la cámara está abierta
                        print("Cámara de la clase Camara está conectada.")
                    else:
                        print("Cámara de la clase Camara no está conectada.")
            except:
                print("Problem to connect to Serial")
            sleep(0.35)
