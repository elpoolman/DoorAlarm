import cv2
import os
from datetime import datetime
import time
import subprocess  
import sys


root_folder = "Pics"


now = datetime.now()
date_folder = now.strftime("%Y-%m-%d")  
time_folder = now.strftime("%Hh-%Mm")   


date_path = os.path.join(root_folder, date_folder)
os.makedirs(date_path, exist_ok=True)


save_path = os.path.join(date_path, time_folder)
os.makedirs(save_path, exist_ok=True)


camera = cv2.VideoCapture(0) 
if not camera.isOpened():
    print("No se pudo acceder a la cámara.")
else:
    print("Cámara detectada. Preparándose para tomar fotos...")

    photos = [] 

    for i in range(1, 4):  
        print(f"Capturando foto {i}...")
        ret, frame = camera.read()
        if ret:
            file_path = os.path.join(save_path, f"foto_{i}.jpg")
            cv2.imwrite(file_path, frame)
            print(f"Foto {i} guardada en: {file_path}")
            photos.append(file_path)  
        else:
            print(f"No se pudo capturar la foto {i}.")


        time.sleep(0.7)


    camera.release()
    print(f"Cámara liberada. Fotos guardadas en: {save_path}")

    try:
        result = subprocess.run(["python", "Cloud.py", save_path], check=True, capture_output=True, text=True)
        print(f"Script Cloud.py ejecutado correctamente. Salida:\n{result.stdout}")
    except subprocess.CalledProcessError as error:
        print(f"Error al ejecutar Cloud.py. Código de retorno: {error.returncode}\nSalida de error:\n{error.stderr}")

    try:
        subprocess.run(["python", "Mail.py"] + photos, check=True)
        print("Script Mail.py ejecutado correctamente. Correo enviado.")
    except subprocess.CalledProcessError as error:
        print(f"Error al ejecutar Mail.py. Código de retorno: {error.returncode}")

