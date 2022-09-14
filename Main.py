from keras.models import load_model
import time
import numpy as np
import cv2
import random
import gspread

# Cargamos el modelo descargado de teachablemachine
model = load_model('keras/keras_model.h5',compile=False)

sa = gspread.service_account(filename="service_account.json")
sh = sa.open("registraBOTdata")
wks = sh.worksheet("data")

labels_array = []
with open('keras/labels.txt') as labels:
    for line in labels:
        x=line.split(", ")
        producto=x[0].split(" ",1)[1]
        marca=x[1].split("\n")[0]
        labels_array.append([producto, marca])
labels.close()

def detectar_objeto_v1():
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)  
    # define a video capture object
    cap = cv2.VideoCapture(0)
    validar = []  
    while (cap.isOpened()):
        # Capture el video frame por frame
        ret, frame = cap.read()
        # Transformamos el frame del video de BGR propio de OpenCV a RGB de la libreria PIL para utilizar el codigo de predicción
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h=frame.shape[0]
        w=frame.shape[1]
        h2=int((w-h)/2)
        #recortamos imagen en un cuadrado
        frame = frame[0:h, h2:h2+h]
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
        
        #validamos si se ha detectado 2 veces seguida el mismo producto y si es asi se rompe el loop
        if (max_value > 0.95) & (producto[0] != "Mano") & (producto[0] != "Nada"):
            #validar.append(producto)
            break
            #print(validar)
            #print(len(validar))
            #if (len(validar)==2) & (len(set(validar))==1):
                #print("HOLA TU PRODUCTO ES: "+ str(producto))
            #    validar = []
            #    break
            #elif (len(validar)==2):
            #    validar.pop(0)

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
    # Cerrar camara
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    return producto

def pesar():
    peso=random.randint(5, 15)/10
    return peso

def precio(peso):
    while True:
        try:
            precio_unitario = float(input("Escribe el precio del Producto: \n"))
        except ValueError:
            print("Debes escribir un número.\n")
            continue

        if precio_unitario < 0:
            print("Debes escribir un número positivo.\n")
            continue
        else:
            precio_total=round(float(precio_unitario)*peso,2)
            break
    return precio_total, precio_unitario

def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list)+1)

def subir_data(producto, marca, peso, precio_unitario, precio_total, hora, fecha):
    print('PRESIONA ENTER PARA TERMINAR LA VENTA Y SUBIR LA DATA')
    while(1):
        accion = input()
        if accion=="":
            lista_subir=[producto,marca,peso,precio_unitario,precio_total,hora,fecha]
            next_row = next_available_row(wks)
            for x in range(len(lista_subir)):
                wks.update_cell(next_row,x+1,lista_subir[x])
            print("DATA SUBIDA Y VENTA TERMINADA\n")
            break

def main():
    while(1):
        print('\n\nPRESIONA ENTER PARA DETECTAR UN NUEVO PRODUCTO')
        accion = input()
        if accion=="":
            [Producto, Marca] = (detectar_objeto_v1())
            if Marca == "Granel":
                Peso=pesar()
                print("\nTu producto es: " + str(Producto) + " y pesa: "  + str(Peso)+ " Kilos\n")
                Precio_total, Precio_unitario = precio(Peso)
            else:
                Peso="-"
                print("\nTu producto es: " + str(Producto)+"\n")
                Precio_total, Precio_unitario = precio(1)
            
            Hora=time.strftime("%X")
            Fecha=time.strftime("%x")
            print("\nEL PRECIO TOTAL ES: S/" + str(Precio_total)+"\n")
            subir_data(Producto, Marca, str(Peso), Precio_unitario, Precio_total, Hora, Fecha)

if __name__ == "__main__":
    main()


