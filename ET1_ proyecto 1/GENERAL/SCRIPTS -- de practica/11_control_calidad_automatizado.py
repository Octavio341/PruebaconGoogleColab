from datetime import timedelta
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
import sys
import os
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
######################################################
#========== CONTROL DE CALIDAD  ===============
#####################################################
# Funci'on que determina si un anio es bisiesto o no
def es_bisiesto(anio):
    resto = anio % 4
    if resto == 0:
        resto = anio % 100
        if resto == 0:
            resto = anio % 400
            if resto == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False

# Verificar que se haya pasado el n'umero correcto de par'ametros
if len(sys.argv) < 2:
    print("No se ha proporcionado el nombre del archivo a verificar")
    quit()

# Obtener el nombre del archivo de entrada a procesar de la lista de par'ametros
nombre_archivo = sys.argv[1]
#print("Se va a cargar el archivo: "+nombre_archivo)

# Leer el archivo de datos y guardarlo en un dataframe de Pandas
matriz_toga = pd.read_csv(nombre_archivo, sep=r'\s+', names = ["StationID", "StationName", "Date", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12"], engine = 'python', skiprows = 1, na_values = "9999")
######################################################################################
print("")
matriz= matriz_toga.iloc[:,3:].dropna()
tamano= matriz.size
fecha_analisis = str(matriz_toga["Date"][1])
resto = int(fecha_analisis[:4])%4
if resto == 0:
    resto2 = int(fecha_analisis[:4])%100

    if resto2 == 0:
        resto3 = int(fecha_analisis[:4])%400

        if resto3 == 0:
            print('Es bisiesto') 

            if tamano == 8784:
                print('La cantidad de datos esta completa')
            else:
                print('La cantidad de datos esta incompleta','...', 'Faltan', 8784-tamano)


        else:
            print('No es bisiesto')
            
            if tamano == 8760:
                print('La cantidad de datos esta completa')
            else:
                print('La cantidad de datos esta incompleta','...', 'Faltan', 8760-tamano)

    else:
        print('Es bisiesto')
        
        if tamano  == 8784:
            print('La cantidad de datos esta completa')
        else:
            print('La cantidad de datos esta incompleta','...', 'Faltan', 8784-tamano)

else:
    print('No es bisiesto')
    
    if tamano == 8760:
        print('La cantidad de datos esta completa')
    else:
        print('La cantidad de datos esta incompleta','...', 'Faltan', 8760-tamano)


#########################################################################################
# Obtener el anio del archivo
fecha = str(matriz_toga["Date"][0])
print("Se ha cargado el archivo "+nombre_archivo+" y se han encontrado datos del anio "+fecha[0:4]+".")
print("")
print("***** Inicio de la revision del archivo *****")

###################################################
# Revisi'on de numero correcto de l'ineas de datos#
###################################################

print("Comprobando que el archivo contenga el numero correcto de lineas de datos ",end = '')

# Calcular cu'antas lineas de datos se esperan
anio_datos = int(fecha[:4])
if es_bisiesto(anio_datos):
    dias_esperados=366*2
else:
    dias_esperados=365*2

if len(matriz_toga.index) == dias_esperados:
    print("[OK]")
else:
    print("[FAIL]")
    print("ERROR: se esperaban "+str(dias_esperados)+" lineas de datos y se han encontrado "+str(len(matriz_toga.index))+".")
    print("Favor de corregir este problema para poder realizar los procesos automatizados de control de calidad.")
    sys.exit(1)

#########################################################
# Revision de existencia de contenido de datos v'alidos #
#########################################################

print("Comprobando que el archivo no este conformado unicamente de datos nulos ",end = '')

if matriz_toga.isna().sum().sum() == 12*dias_esperados:
    print("[FAIL]")
    print("ERROR: El archivo de entrada no contiene datos, unicamente contiene valores nulos. No se puede procesar.")
    print("***** Fin de la revision del archivo *****")
    sys.exit()
else:
    print("[OK]")

####################################################
# Revisi'on del incremento cronol'ogico del tiempo #
####################################################

print("Comprobando que el tiempo se incremente cronologicamente en los datos ",end = '')

# Crear la fecha de control
fecha_control=datetime.datetime(anio_datos,1,1)
hora_control=1
dias_faltantes=0
dias_existentes=0
anio_final=int(fecha[:4])+1
ind = 0

# Generar una a una las fechas y compararlas con el dataframe
while fecha_control.year < anio_final:

    if ind < len(matriz_toga.index):

        # Cargar la fecha del dataframe
        fecha = str(matriz_toga["Date"][ind])

        # Verificar si la fecha de control y la fecha del dataframe son iguales
        if fecha != fecha_control.strftime("%Y%m%d")+str(hora_control):
            print("[FAIL]")
            print("ERROR: El tiempo no se incrementa cronologicamente en los datos, se esperaba la fecha "+fecha_control.strftime("%Y%m%d")+str(hora_control)+" y se ha encontrado la fecha "+fecha+".")
            print("Favor de corregir este problema para poder realizar los procesos automatizados de control de calidad.")
            sys.exit(1)

        # Incrementar el indice del dataframe
        ind = ind + 1

        # Avanzar la fecha de control
        if hora_control == 1:
            hora_control = 2
        else:
            hora_control = 1
            fecha_control=fecha_control+timedelta(days=1)

if fecha_control.year == anio_final:
    print("[OK]")
else:
    print("[FAIL]")
    print("ERROR: El tiempo no se incrementa cronologicamente en los datos")
    print("Favor de corregir este problema para poder realizar los procesos automatizados de control de calidad.")
    sys.exit(1)

#######################################
# Detecci'on de caracteres inv'alidos #
#######################################

print("Detectando si las columnas de datos contienen caracteres invalidos ",end = '')

# Verificar si alguna columna de datos contiene valores no num'ericos
if str(matriz_toga["Date"].dtypes) == "object" or str(matriz_toga["D1"].dtypes) == "object" or str(matriz_toga["D2"].dtypes) == "object" or str(matriz_toga["D3"].dtypes) == "object" or str(matriz_toga["D4"].dtypes) == "object" or str(matriz_toga["D5"].dtypes) == "object" or str(matriz_toga["D6"].dtypes) == "object" or str(matriz_toga["D7"].dtypes) == "object" or str(matriz_toga["D8"].dtypes) == "object" or str(matriz_toga["D9"].dtypes) == "object" or str(matriz_toga["D10"].dtypes) == "object" or str(matriz_toga["D11"].dtypes) == "object" or str(matriz_toga["D12"].dtypes) == "object":
    print("[FAIL]")
    print("ERROR: Se han detectado las siguientes columnas de datos que contienen valores no numericos: ",end = '')
    for colname in ["Date", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12"]:
        if matriz_toga[colname].dtypes == "object":
            print(colname+" ",end = '')
    print("\nFavor de corregir este problema para poder realizar los procesos automatizados de control de calidad.")
else:
    print("[OK]")

########################################################################
# Crear el array de fechas, valores y etiquetas a partir del dataframe #
########################################################################

lista_fechas = list()
lista_datos = list()
lista_etiquetas = list()
ind = 0

# Recorrer todo el dataframe
while ind < len(matriz_toga.index):

    # Cargar la fecha de la columna correspondiente
    fecha = str(matriz_toga["Date"][ind])

    # Crear la fecha inicial
    if fecha[8:9] == "1":
        fecha_inicial = datetime.datetime(int(fecha[:4]), int(fecha[4:6]), int(fecha[6:8]))
    else:
        fecha_inicial = datetime.datetime(int(fecha[:4]), int(fecha[4:6]), int(fecha[6:8]), 12)

    # Cargar los 12 datos dejando fuera a los NaN
    for dat in ["D1", "D2", "D3", "D4",  "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12"]:
        if str(matriz_toga[dat][ind]) != "nan":
            lista_fechas.append(fecha_inicial)
            lista_datos.append(matriz_toga[dat][ind])
            lista_etiquetas.append(0)
        fecha_inicial = fecha_inicial + timedelta(hours=1)

    # Avanzar el 'indice
    ind = ind + 1
##########################
# Prueba de l'inea recta #
##########################
print("")
print("***** analisis de los datos   *****")
print("Realizando prueba de estabilidad (linea recta)")

stucktotal = 0
stuckcount = 0                  # Contador de valores consecutivos iguales
stucklimit = 4                  # Cantidad de valores consecutivos  a partir de la cual la serie se considera atorada
stuckvalue = lista_datos[0]     
stuckindex = 0

lista_stuck_datos = list()
lista_stuck_fechas = list()

# Recorrer todo el arreglo de datos
for ind in range(len(lista_datos)):

    # Comenzar a partir del segundo dato
    if ind > 0:

        # Verificar si el dato que se está revisando actualmente no es igual al stuckvalue
        if stuckvalue == lista_datos[ind] and ind-1 == stuckindex:
            stuckcount = stuckcount + 1
        else:
            stuckcount = 0

        if stuckcount >= stucklimit-1:

            # Si se trata de los primeros tres valores, etiquetar los dos valores previos
            if stuckcount == stucklimit-1:
                for k in range(ind-(stucklimit-1), ind):
                    lista_etiquetas[k]=3
                    #print("---Se han encontrado y etiquetado valores iguales consecutivos (stuck values). Valor: "+str(lista_datos[k])+" Posicion: "+str(k))
                    lista_stuck_datos.append(lista_datos[k])
                    lista_stuck_fechas.append(lista_fechas[k])
                stucktotal = stucktotal + 1
            
            # Etiquetar el stuckvalue actual
            lista_etiquetas[ind]=3
            #print("---Se han encontrado y etiquetado valores iguales consecutivos (stuck values). Valor: "+str(lista_datos[ind])+" Posicion: "+str(ind))
            lista_stuck_datos.append(lista_datos[ind])
            lista_stuck_fechas.append(lista_fechas[ind])

        stuckvalue = lista_datos[ind]
        stuckindex = ind


##################################
# Prueba de detecci'ion de picos #
##################################

print("Realizando la prueba de deteccion de picos.")

contadorpicos = 0
spikedetected = True    # Bandera de que un pico ha sido detetado
splinedegree = 2        # Grado del spline que ser'a ajustado
winsize = 200           # Tamanio de la ventana
maxiter = 1             # N'umero m'aximo de iteraciones
nsigma = 4              # Valor de sigma a considerar
iter = 0                # N'umero de iteraci'on actual

# Funci'on que obtiene el RMSE
def rmse(predictions, targets):
        return np.sqrt(((predictions - targets) ** 2).mean()) 

# Crear la lista de indices con elementos de punto flotante
lista_indices = list()
for i in range(len(lista_datos)):
    lista_indices.append(float(i))

# Iterar el algoritmo solo si se encontraron picos en la iteracion previa y si no se ha alcanzado del m'aximo de iteraciones
# spikedetected se inicializa con True para que siempre se haga al menos la primer iteraci'on
while spikedetected and iter < maxiter:
    spikedetected = False                   # Si no se detecta ning'un pico en la primer iteracion, ya no se hace la segunda
    for ix in range(len(lista_datos)):      # ix recorrer'a todos los indices de la lista de datos
        if (ix < winsize/2):                # Si el indice est'a dentro de los primeros 100 valores
            ini=0
            end=winsize-1
            winix = ix
        elif (ix > len(lista_datos) - winsize/2):   # Si el 'indice esta en los 'ultimos 100 datos
            ini=len(lista_datos)-winsize
            end=len(lista_datos)-1
            winix = (winsize-1)-(end-ix+1)
        else:                                       # Si el 'indice no est'a ni en los primeros ni en los 'ultimos 100 datos
            ini = int(ix - winsize/2)
            end = int(ix + winsize/2)
            winix = int(winsize/2)
        winx = lista_indices[ini:end]
        windata = lista_datos[ini:end]
        splinefit = np.polyfit(winx, windata, splinedegree)
        splinedata = np.polyval(splinefit, winx)
        rmse_val = rmse(splinedata, windata) #¿Usar np.array?
        if (abs(splinedata[winix]-lista_datos[ix]) >= nsigma*rmse_val):
                print ("Se ha encontrado un pico en la posicion "+str(ix)+" y el valor es "+str(lista_datos[ix]))
                lista_etiquetas[ix] = 8 
                spikedetected = True
                contadorpicos = contadorpicos + 1
    iter=iter+1

print("Resumen del contol de calidad. Se han encontrado "+str(contadorpicos)+" picos y "+str(stucktotal)+" lineas (stuckdata).")
#####################################################
# Escribir el archivo de texto de datos etiquetados #
#####################################################

print("Se va a proceder a escribir el archivo de salida con los datos etiquetados.")

# Crear el archivo de salida etiquetado
#archivo_salida = open("labeled-"+nombre_archivo, 'w+')