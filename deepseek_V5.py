import sys
import pyttsx3
import customtkinter as ctk
from tkinter import Text
import speech_recognition as sr
from ollama import chat

# Inicializar el motor de síntesis de voz
engine = pyttsx3.init()

# Ajustar la velocidad del habla (puedes ajustar este valor según tus necesidades)
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 80)  # Disminuir la velocidad para una lectura más fluida

# Inicializar el reconocedor de voz
recognizer = sr.Recognizer()

def listen_and_recognize():
    with sr.Microphone() as source:
        print("Escuchando...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="es-ES")
            print(f"Has dicho: {text}")
            entry.delete(0, ctk.END)
            entry.insert(0, text)
            run_chat()
        except sr.UnknownValueError:
            print("No se pudo entender el audio")
        except sr.RequestError as e:
            print(f"Error al solicitar resultados del servicio de reconocimiento de voz; {e}")

def run_chat():
    # Limpiar el área de texto antes de mostrar el nuevo mensaje
    text_area.delete("1.0", ctk.END)
    
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
            
            # Imprimir el contenido en la interfaz gráfica con la fuente deseada
            text_area.insert(ctk.END, chunk_content, "response_font")
            text_area.see(ctk.END)
            
            # Agregar el contenido al texto completo
            content += chunk_content

    # Decir el contenido en voz alta después de recibir todo el mensaje
    engine.say(content)
    engine.runAndWait()

# Configurar la apariencia de customtkinter
ctk.set_appearance_mode("dark")  # Modo oscuro
ctk.set_default_color_theme("blue")  # Tema de color

# Crear la ventana principal
root = ctk.CTk()
root.title("DeepSeek Chat")

# Crear un área de texto desplazable usando el widget estándar de tkinter
text_area = Text(root, wrap="word", width=60, height=20, font=("Helvetica", 12))
text_area.pack(padx=10, pady=10)

# Configurar la fuente para la respuesta de la IA
text_area.tag_configure("response_font", font=("Times New Roman", 12))

# Crear una entrada de texto
entry = ctk.CTkEntry(root, width=500, font=("Helvetica", 12))
entry.pack(padx=10, pady=10)

# Crear un botón para iniciar el chat
button = ctk.CTkButton(root, text="Enviar", command=run_chat, font=("Helvetica", 12))
button.pack(padx=10, pady=10)

# Crear un botón para iniciar el reconocimiento de voz
voice_button = ctk.CTkButton(root, text="Hablar", command=listen_and_recognize, font=("Helvetica", 12))
voice_button.pack(padx=10, pady=10)

# Ejecutar la aplicación
root.mainloop()