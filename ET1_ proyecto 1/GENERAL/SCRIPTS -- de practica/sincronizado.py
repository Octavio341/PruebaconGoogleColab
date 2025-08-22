import ipywidgets as widgets
from IPython.display import display, HTML
import zipfile, os
from google.colab import files
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.models import Range1d

#para los datos toga 
from io import StringIO
import pandas as pd
import numpy as np
from datetime import timedelta

import io

# ===================== FUNCIÓN PRINCIPAL =====================
# Lista para guardar todos los contenedores de archivos
todos_los_contenedores = []
def super_resumen(archivos_lista):
    # ===================== VARIABLES GLOBALES =====================
    archivos_seleccionados = []
    checkboxes_individuales = []

    # ===================== FUNCIONES GLOBALES =====================
    def actualizar_mensaje():
        mensaje = "Estos son los archivos que convertiremos:<br>" + "<br>".join(archivos_seleccionados)
        salida.value = mensaje

    def on_change(change, archivo):
        if change['new']:
            if archivo not in archivos_seleccionados:
                archivos_seleccionados.append(archivo)
        else:
            if archivo in archivos_seleccionados:
                archivos_seleccionados.remove(archivo)
        actualizar_mensaje()

    def on_seleccionar_todo(change):
        for cb in checkboxes_individuales:
            cb.value = change['new']  # Esto dispara on_change automáticamente
    salida_error = widgets.Output()
    salida_archivo = widgets.Output()
    def descargar_zip(b):
        zip_filename = "mis_archivos.zip"
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for archivo in archivos_seleccionados:
                if os.path.exists(archivo):
                    zipf.write(archivo, os.path.basename(archivo))
                else:
                    with salida_error:
                      print(f"⚠️ No se encontró: {archivo}")
        files.download(zip_filename)

    # ===================== WIDGETS FIJOS =====================
    seleccionar_todo = widgets.Checkbox(value=False, description="Seleccionar todo")
    seleccionar_todo.observe(on_seleccionar_todo, names='value')

    salida = widgets.HTML(value="")
    boton_descargar = widgets.Button(description="📦 Descargar ZIP", button_style='success')
    boton_descargar.on_click(descargar_zip)

    opciones_boton= widgets.HBox([seleccionar_todo, boton_descargar])
  
    salida_resultados=widgets.HBox([salida,salida_error])

    # Simulamos contenedor_final
    contenedor_global = widgets.HBox([widgets.HTML("Contenido del archivo")])

    contenedor_general = []
    mensajes = []
    bloques = []
    archivos_procesados = set()  # almacena nombres de archivos ya analizados

    for nombre, contenido in archivos_lista.items():
        mensajes = []
        mensajes.append(f"Procesando: {nombre}")
        bloque_texto = "<br>".join(mensajes)
    
        matriz_toga = pd.read_csv(io.StringIO(contenido),
                            sep=r'\s+',
                            names=["StationID","StationName","Date","D1","D2","D3","D4","D5","D6",
                                    "D7","D8","D9","D10","D11","D12"],
                            engine='python', skiprows=1, na_values="9999")
        
        matriz_toga["Archivo"] = nombre  # agregamos columna con nombre de archivo
        #bloques.append(matriz_toga.head())  # guardamos DataFrame de ejemplo
        #matriz_toga = pd.read_csv(nombre,sep=r'\s+',names =["StationID", "StationName", "Date", "D1", "D2", "D3","D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12"], engine = 'python', skiprows = 2, na_values = "9999")
        #display(matriz_toga)
        lista_fecha= list()
        lista_datos=list()

        # Crear la fecha de control
        fecha = str(matriz_toga["Date"][0])
        fecha_control=datetime.datetime(int(fecha[:4]),1,1)
        mensajes.append(f"Archivo: {nombre} cargado se han encontrado datos del anio {fecha_control.strftime('%Y')}")
        bloque_texto = "<br>".join(mensajes)

        #####################################  ==========================
        ind = 0
        hora_control=1
        dias_faltantes=0
        dias_existentes=0
        anio_final=int(fecha[:4])+1
        # Generar una a una las fechas y compararlas con el dataframe
        while fecha_control.year < anio_final:
        ###################################################

            if ind < len(matriz_toga.index):

                # Cargar la fecha del dataframe
                fecha = str(matriz_toga['Date'][ind])

            # Verificar si la fecha de control y la fecha del dataframe son iguales
            if fecha == fecha_control.strftime('%Y%m%d')+str(hora_control):

                # Contar el dia existente
                dias_existentes = dias_existentes+1

            else:
        ###################################################
                # Si la fecha de control y la fecha del dataframe no son iguales, avisar al usuario y contar la linea faltante
                #print("No se encontr'o la fecha "+fecha_control.strftime("%Y%m%d")+str(hora_control))
                mensajes.append(f"No se encontro la fecha {fecha_control.strftime('%Y%m%d')}{str(hora_control)}")
                bloque_texto = "<br>".join(mensajes)
                dias_faltantes=dias_faltantes+1

                # Avanzar con la fecha de control hasta que sea igual a la del dataframeo se acabe el año
        ###################################################
                while fecha != fecha_control.strftime('%Y%m%d')+str(hora_control) and fecha_control.year < anio_final:
                    # Avanzar la fecha de control
                    if hora_control == 1:
                        hora_control = 2
                    else:
                        hora_control = 1
                        fecha_control=fecha_control+timedelta(days=1)
                
                    if fecha == fecha_control.strftime('%Y%m%d')+str(hora_control):
                        # Si la fecha de control y la fecha del dataframe son iguales, contarlo
                        dias_existentes=dias_existentes+1
                    else:
                        # Si la fecha de control y la fecha del dataframe no son iguales, avisar al usuario y contar la linea faltante
                        mensajes.append(f"No se encontro la fecha {fecha_control.strftime('%Y%m%d')} {str(hora_control)}")
                        bloque_texto = "<br>".join(mensajes)
                        #print("No se encontr'o la fecha "+fecha_control.strftime("%Y%m%d")+str(hora_control))
                        dias_faltantes=dias_faltantes+1
        ###################################################
            # Incrementar el indice del dataframe
            ind = ind + 1
        ###################################################
            # Avanzar la fecha de control
            if hora_control == 1:
                hora_control = 2
            else:
                hora_control = 1
                fecha_control=fecha_control+timedelta(days=1)

        ###################################################
        datos_validos=(dias_faltantes+dias_existentes)*12-matriz_toga.isna().sum().sum()
        mensajes.append(f"Hay {str(datos_validos)} datos validos ({str("{0:.2f}".format(datos_validos*100/((dias_faltantes+dias_existentes)*12)))}% ) y {str(matriz_toga.isna().sum().sum())} datos nulos ({str("{0:.2f}".format(matriz_toga.isna().sum().sum()*100/((dias_faltantes+dias_existentes)*12)))}%)")
        bloque_texto = "<br>".join(mensajes)
        #print("Hay "+str(datos_validos)+" datos validos ("+str("{0:.2f}".format(datos_validos*100/((dias_faltantes+dias_existentes)*12)))+"%) y "+str(matriz_toga.isna().sum().sum())+" datos nulos ("+str("{0:.2f}".format(matriz_toga.isna().sum().sum()*100/((dias_faltantes+dias_existentes)*12)))+"%)")
        ##################################### ==========================
        for filas_dat in matriz_toga.index:
          fecha = str(matriz_toga["Date"][filas_dat])
          #fecha es =  195701011
          if fecha[8:9]== "1": # seleccionamos dia
            fecha_inicial = datetime.datetime(int(fecha[:4]),int(fecha[4:6]),int(fecha[6:8]))
            # fecha_inicial es = 1955-08-25 00:00:00
          else:
            fecha_inicial = datetime.datetime(int(fecha[:4]),int(fecha[4:6]),int(fecha[6:8]),12)
            #fecha inicial es = 1960-01-01 12:00:00
          for dat in ["D1", "D2", "D3", "D4",  "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12"]:
            lista_fecha.append(fecha_inicial)
            lista_datos.append(matriz_toga[dat][filas_dat])
            #lista_datos.append(matriz_toga[dat][archivo])      #AGRAGMOS LAS LISTA ETIQUETAS
            fecha_inicial=fecha_inicial+datetime.timedelta(hours=1)
        
        x = np.array(lista_fecha)
        y = np.array(lista_datos)

        p = figure(width=450,x_axis_type='datetime', height=260, title="Gráfico")
        p.line(x, y, line_width=1, color="blue")
        script, div = components(p)
        recursos = CDN.render()


        # Contenedor para Bokeh
        salida_grafico = widgets.Output()
        with salida_grafico:
            display(HTML(recursos + div + script))  # ✅ aquí sí se ejecuta el JS


        # Checkbox individual
        checkbox = widgets.Checkbox(value=False, description="")
        checkboxes_individuales.append(checkbox)
        checkbox.observe(lambda change, archivo=nombre: on_change(change, archivo), names='value')

        # Bloque con gráfico + mensajes + checkbox
        contenedor_final = widgets.HBox([
            salida_grafico,
            widgets.VBox([
                widgets.HBox([checkbox, widgets.HTML(f"<b>📄 {nombre}</b>")]),
                widgets.HTML(f"<div style='font-family:Courier New, monospace; font-size:13px; color:#2D6FA4; height:200px;width:500px'>{bloque_texto}</div>")
            ])
        ], layout=widgets.Layout(border="2px solid #2D6FA4", border_radius="10px",
                                padding="10px", margin="5px", width="1100px",align_items="flex-start"))
        #display(contenedor_final
        contenedor_final.layout.flex = "0 0 auto"
        contenedor_general.append(contenedor_final)  # acumulamos cada bloque

    # Agrupamos todos los bloques en un contenedor principal
    #[2]=================  Cuadros  ==========================
    style_box = {
      'border': '5px solid #2D6FA4',
      'padding': '10px',
      'margin': '1.5px',
      'border-radius': '8px',
      'background-color': '#10283B',  #
      'width': '570px',
      'height': '280px',
      'overflow': 'auto',
  }
    #[3]=================  Cuadros  ==========================
    #todo el contenido del cuadrito
    def make_box(title, content_widgets):
      label = widgets.HTML(value=f"<b>{title}</b>")
      if isinstance(content_widgets, list):  # si es lista, empaquetamos
          content_widgets = widgets.VBox(content_widgets)

      box = widgets.VBox([label, content_widgets])
      box.layout = widgets.Layout(
          border=style_box['border'],
          padding=style_box['padding'],
          margin=style_box['margin'],
          border_radius=style_box['border-radius'],
          background_color=style_box['background-color'],
          width=style_box['width'],
          height=style_box['height'],
          overflow=style_box['overflow'],
      )
      return box

    # Crear cajas con contenido variado
    box1 = make_box("Resumen general",contenedor_general)
    box1.layout.width ='1200px'
    box1.layout.height ='500px'
    box2 = make_box("Opciones ",opciones_boton)
    box2.layout.width ='1200px'
    box2.layout.height ='100px'
    box3 = make_box("Cargar Archivo",salida_resultados)
    box3.layout.width ='500px'
    box3.layout.height ='600px'
    fila = widgets.VBox([box2,box1])
    fila2 = widgets.HBox([box3])

    fila_total = widgets.HBox([fila, fila2])

    return fila_total  # 👈 devuelvo el widget en vez de display
