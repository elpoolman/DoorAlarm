import serial
import subprocess
import signal

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=0.1)

proceso = None

def ejecutar_funcion():
    global proceso

    if proceso is None or proceso.poll() is not None:
        proceso = subprocess.Popen(['python3', 'PhotoCam.py'])

def detener_funcion():
    global proceso

    if proceso and proceso.poll() is None:
        proceso.send_signal(signal.SIGTERM)  
        proceso.wait() 

def esperar_trigger():
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            if line == "TRIGGER":
                ejecutar_funcion()
            elif line == "STOP":
                detener_funcion()

esperar_trigger()
