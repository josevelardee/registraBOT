from keras.models import load_model
import numpy as np
import cv2
from labels import *

# Cargamos el modelo descargado de teachablemachine
model = load_model('keras/keras_model.h5',compile=False)
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)  
# define a video capture object
cap = cv2.VideoCapture(0)
validar=[]
  
while (cap.isOpened()):
    # Capture el video frame por frame
    ret, frame = cap.read()
    # Transformamos el frame del video de BGR propio de OpenCV a RGB de la libreria PIL para utilizar el codigo de predicción
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Recortamos el frame en un cuadrado
    frame = frame[0:1080, 430:1510]
    # Redimensionamos el frame para ver como lo lee el codigo 224x244
    size = (224, 224)
    frame = cv2.resize(frame, size, interpolation = cv2.INTER_AREA)
    #Convertimos la imagen en un numpy array
    image_array = np.asarray(frame)
    # Normalizamos la imagen
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    # Cargamos la imagen dentro del array
    data[0] = normalized_image_array

    #Corremos el modelo
    prediction = model.predict(data)
    #Buscamos la posición del valor más alto del array de predicciones
    max_value = np.max(prediction)
    max_index = np.argmax(prediction)
    p_prediccion=np.amax(prediction)
    producto=labels_array[max_index]
    #imprimimos el nombre del producto detectado
    #print(producto)
    
    #validamos si se ha detectado 3 veces seguida el mismo producto y si es asi se rompe el loop
    if (max_value > 0.95) & (producto != "Mano") & (producto != "Nada"):
        print(producto)
        break
        #validar.append(producto)
        #print(validar)
        #print(len(validar))
        # if (len(validar)==3) & (len(set(validar))==1):
        #     print("HOLA TU PRODUCTO ES: "+ str(producto))
        #     validar = []
        #     break
        # elif (len(validar)==3):
        #     validar.pop(0)



    #Regresamos los colores del frame del video para visualizar en la pantalla
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Mostramos el video en la pantalla
    cv2.imshow('Frame', frame)

    # define q as the exit button
    key = cv2.waitKey(25)
    if key == ord('n') or key == ord('p'):
        break


  
# After the loop release the cap object
cap.release()
# Destroy all the windows
cv2.destroyAllWindows()