import ipywidgets as widgets
from IPython.display import display, HTML
import zipfile, os
from google.colab import files
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import CDN

# ===================== FUNCIÓN PRINCIPAL =====================
# Lista para guardar todos los contenedores de archivos

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

    bloques = []
    for archivo in archivos_lista:
        # Gráfico dummy
        # Valores de ejemplo
        x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        y = [5, 3, 6, 2, 7, 4, 8, 3, 9, 5]
        p = figure(width=350, height=160, title="Gráfico")
        p.line(x, y, line_width=2, color="green")
        script, div = components(p)
        recursos = CDN.render()


        # Contenedor para Bokeh
        salida_grafico = widgets.Output()
        with salida_grafico:
            display(HTML(recursos + div + script))  # ✅ aquí sí se ejecuta el JS


        # Mensajes según tipo
        if archivo.endswith(".csv"):
            mensajes = ["Cargando CSV...", "Procesando datos...", "✅ Listo"]
        elif archivo.endswith(".png"):
            mensajes = ["Cargando imagen...", "Aplicando filtros...", "✅ Imagen lista"]
        elif archivo.endswith(".txt"):
            mensajes = ["Leyendo TXT...", "Limpiando datos...", "✅ Texto procesado"]
        else:
            mensajes = ["Generando PDF...", "Insertando gráficos...", "✅ Documento creado"]
        bloque_texto = "<br>".join(mensajes)

        # Checkbox individual
        checkbox = widgets.Checkbox(value=False, description="")
        checkboxes_individuales.append(checkbox)
        checkbox.observe(lambda change, archivo=archivo: on_change(change, archivo), names='value')

        # Bloque con gráfico + mensajes + checkbox
        contenedor_final = widgets.HBox([
            salida_grafico,
            widgets.VBox([
                widgets.HBox([checkbox, widgets.HTML(f"<b>📄 {archivo}</b>")]),
                widgets.HTML(f"<div style='font-family:Courier New, monospace; font-size:13px; color:#2D6FA4; height:200px;width:500px'>{bloque_texto}</div>")
            ])
        ], layout=widgets.Layout(border="2px solid #2D6FA4", border_radius="10px",
                                padding="10px", margin="5px", width="900px",align_items="flex-start"))
        #display(contenedor_final
        contenedor_final.layout.flex = "0 0 auto"
        bloques.append(contenedor_final)  # acumulamos cada bloque

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
    box1 = make_box("Resumen general",bloques)
    box1.layout.width ='900px'
    box1.layout.height ='500px'
    box2 = make_box("Opciones ",opciones_boton)
    box2.layout.width ='900px'
    box2.layout.height ='100px'
    box3 = make_box("Cargar Archivo",salida_resultados)
    box3.layout.width ='900px'
    box3.layout.height ='600px'
    fila = widgets.VBox([box2,box1])
    fila2 = widgets.HBox([box3])

    display(widgets.HBox([fila,fila2]))  



super_resumen(archivos)
