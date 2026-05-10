# Archivo: codigo_sucio.py
import os, shutil

def f(x,y):
 z = x + y
 return z

def PROC_DAT(lista):
    res=[]
    for i in range(len(lista)):
        # error de tipo potencial y logica lenta
        val = lista[i] * 1.15
        res.append(val)
    return res

# No hay manejo de errores, variables confusas
def mve(a,b):
    shutil.move(a,b)
    print("listo")

input_usuario = [100, 200, 300]
print(PROC_DAT(input_usuario))