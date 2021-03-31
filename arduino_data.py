import serial

import threading

import csv


class ArduinoData:
    def __init__(self):
        self.arduino_data = ""
        try:
            self.arduinoSerialData = serial.Serial('com3', 9600)  #9600 is the Baudrate

            read_thread = threading.Thread(target=self.start_reading_data)
            read_thread.daemon = True
            read_thread.start()
        except:
            print("Error: Arduino Not Connected")
            quit()

    def start_reading_data(self):
        fieldnames = ["Altitude", "Temperature", "Velocity", "Pressure", "Duration"]
        with open('data.csv', 'w', newline="") as csv_file:
                    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                    csv_writer.writeheader()
        
        while True:
            if (self.arduinoSerialData.inWaiting() > 0):  # Only proceeds when there is something from arduino
                self.arduino_raw_data = self.arduinoSerialData.readline()
                self.arduino_data = self.arduino_data + self.arduino_raw_data.decode().strip() + "\n"
                
                readings = self.arduino_raw_data.decode().strip().split(",")
                
                altitude = int(readings[0])
                temperature = int(readings[1])
                velocity = int(readings[2])
                pressure = int(readings[3])
                duration = int(readings[4])

                with open('data.csv', 'a', newline="") as csv_file:
                    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

                    info = {
                        "Altitude": altitude,
                        "Temperature": temperature,
                        "Velocity": velocity,
                        "Pressure" : pressure,
                        "Duration" : duration
                    }

                    csv_writer.writerow(info)
                    print(altitude, temperature, velocity, pressure, duration)

    def get_arduino_data(self):
        if self.arduino_data != None:
            return self.arduino_data
        else:
            pass