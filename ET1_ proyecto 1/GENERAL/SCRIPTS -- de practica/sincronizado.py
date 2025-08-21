
import ipywidgets as widgets
from IPython.display import display, HTML

# mi_script.py
def super_resumen(archivos_lista):
    """
    Recibe una lista de archivos y los muestra en un formulario interactivo
    con checkboxes.
    """
    for archivo in archivos_lista:
        print(archivo)

        if archivo.endswith(".csv"):
         mensajes = ["Cargando imagen...", "Aplicando filtros...", "Corrigiendo colores...", "Guardando copia...", "✅ Imagen lista"]

        elif archivo.endswith(".png"):
            mensajes = ["Cargando imagen...", "Aplicando filtros...", "Corrigiendo colores...", "Guardando copia...", "✅ Imagen lista"]
        elif archivo.endswith(".txt"):
            mensajes = ["Leyendo TXT...", "Buscando errores...", "Transformando datos...", "Escribiendo nuevo archivo...", "✅ Texto procesado"]
        else:
            mensajes = ["Generando archivo...", "Agregando contenido...", "Insertando gráficos...", "Guardando PDF...", "✅ Documento creado"]
        bloque_texto = "<br>".join(mensajes)

        mensajes_y_checkbox = widgets.VBox([
            widgets.HBox([widgets.HTML(f"<b>📄 {archivo}</b>")]),
            widgets.HTML(f"<div style='font-family:Courier New, monospace; font-size:13px; color:#2D6FA4; overflow:auto; height:200px;width:500px'>{bloque_texto}</div>")
            #widgets.HBox([widgets.HTML(f"<b>📄 {archivo}</b>"),checkbox])

        ])

        display( mensajes_y_checkbox)


