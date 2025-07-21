# interfaz.py
import tkinter as tk
import subprocess

def ejecutar_script():
    # Ejecutar script_secundario.py
    subprocess.run(["python", "script_secundario.py"])

# Crear ventana
ventana = tk.Tk()
ventana.title("Interfaz con botón")
ventana.geometry("300x150")

# Crear botón
boton = tk.Button(ventana, text="Ejecutar Script", command=ejecutar_script)
boton.pack(pady=40)

# Iniciar la interfaz
ventana.mainloop()
