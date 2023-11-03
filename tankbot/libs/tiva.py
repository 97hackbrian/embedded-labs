import serial as com

class InitSerial:
    def __init__(self,baud) -> None:
        for x in range(11):
            try:
                self.ser=com.Serial('/dev/ttyACM{x}',baud,timeout=1)
                if self.ser.is_open:
                    print("Successful to connect in the port ttyACM",x)
                    self.ser.reset_input_buffer()
                    self.ser.reset_output_buffer()
                    break
            except:
                print("Problem to connect to ttyACM",x,"\nTry to connect to the next port")
    def send_data(self,*args):
        smg = ",".join(map(str, args))  # Une los argumentos en una cadena separada por comas
        self.ser.write(f"{smg}\n")  # Agrega un salto de línea al final para enviar los datos

                
        
class Motors:
    def __init__(self,number_motors,serial_instance) -> None:
        self.ser=serial_instance
    def move(self,left,right):
        self.ser.send_data("",,)