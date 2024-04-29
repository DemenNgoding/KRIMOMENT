import serial
import serial.tools.list_ports as port_list


class Arduino:
    def __init__(self, port=0):
        ports = list(port_list.comports())
        
        port = ports[port].device
        
        baud_rate = 2000000
        for i in ports:
            print("Serial connection: ", i.device)
        arduino = serial.Serial(port=port, baudrate=baud_rate, timeout=.1)

        self.arduino = arduino
        self.port = port

    def send_serial(self, data: str) -> str:
        data += "\n"
        try:
            self.arduino.write(str(data).encode())
            return data + " sent..."
        except: 
            return f"arduino in {self.port} data send error..."
        
