from ollama import chat
import sys
import pyttsx3
import tkinter as tk
from tkinter import scrolledtext

# Inicializar el motor de síntesis de voz
engine = pyttsx3.init()

# Ajustar la velocidad del habla (puedes ajustar este valor según tus necesidades)
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 80)  # Disminuir la velocidad para una lectura más fluida

def run_chat():
    # Limpiar el área de texto antes de mostrar el nuevo mensaje
    text_area.delete(1.0, tk.END)
    
    stream = chat(
        model='deepseek-r1:8b',
        messages=[{'role': 'user', 'content': entry.get()}],
        stream=True,
    )

    content = ""

    for chunk in stream:
        if chunk and 'message' in chunk and chunk['message'].content:
            # Obtener el contenido del chunk
            chunk_content = chunk['message'].content
            
            # Imprimir el contenido en la interfaz gráfica
            text_area.insert(tk.END, chunk_content)
            text_area.see(tk.END)
            
            # Agregar el contenido al texto completo
            content += chunk_content

    # Decir el contenido en voz alta después de recibir todo el mensaje
    engine.say(content)
    engine.runAndWait()

# Crear la ventana principal
root = tk.Tk()
root.title("DeepSeek Chat")

# Crear un área de texto desplazable
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
text_area.pack(padx=10, pady=10)

# Crear una entrada de texto
entry = tk.Entry(root, width=50)
entry.pack(padx=10, pady=10)

# Crear un botón para iniciar el chat
button = tk.Button(root, text="Enviar", command=run_chat)
button.pack(padx=10, pady=10)

# Ejecutar la aplicación
root.mainloop()