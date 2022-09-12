import tkinter as tk
from tkinter import ttk

peso_producto=10
nombre_producto = "Mayonesa"

def calcular_precio():
    ventana.after(100,calcular_precio)
    precio_unitario = caja_precio_unitario.get()
    try:
        precio_total = peso_producto * float(precio_unitario)

    except:
        precio_total = ''
    etiqueta_precio_total.config(text=f"Precio Total S/: {precio_total}")
    etiqueta_precio_total.pack


ventana = tk.Tk()
ventana.title("Detector de Producto")
ventana.config(width=400, height=300)

etiqueta_nombre_producto = ttk.Label(text="Nombre del Producto:")
etiqueta_nombre_producto.config(text=f"Nombre del Producto: {nombre_producto}")
etiqueta_nombre_producto.place(x=20, y=20)

etiqueta_peso_producto = ttk.Label(text="Peso:")
etiqueta_peso_producto.config(text=f"Peso: {peso_producto} Kg")
etiqueta_peso_producto.place(x=20, y=50)

etiqueta_precio_unitario = ttk.Label(text="Precio Unitario (S/Kg):")
etiqueta_precio_unitario.place(x=20, y=80)

caja_precio_unitario = ttk.Entry(ventana)
caja_precio_unitario.place(x=160, y=80, width=60)

etiqueta_precio_total = ttk.Label(text="Precio Total S/: n/a")
etiqueta_precio_total.place(x=20, y=110)

boton_terminar = ttk.Button(text="Terminar Venta")
boton_terminar.place(x=20, y=140)

caja_precio_unitario.bind('<Return>', calcular_precio)
ventana.after(100,calcular_precio)

ventana.mainloop()