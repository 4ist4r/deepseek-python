from ollama import chat
import sys
import pyttsx3

# Inicializar el motor de síntesis de voz
engine = pyttsx3.init()

# Ajustar la velocidad del habla (puedes ajustar este valor según tus necesidades)
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 80)  # Disminuir la velocidad para una lectura más fluida

stream = chat(
    model='deepseek-r1:8b',
    messages=[{'role': 'user', 'content': "What is the capital of France?"}],
    stream=True,
)

content = ""

for chunk in stream:
    if chunk and 'message' in chunk and chunk['message'].content:
        # Obtener el contenido del chunk
        chunk_content = chunk['message'].content
        
        # Imprimir el contenido inmediatamente, sin nueva línea
        sys.stdout.write(chunk_content)
        sys.stdout.flush()
        
        # Agregar el contenido al texto completo
        content += chunk_content

# Decir el contenido en voz alta después de recibir todo el mensaje
engine.say(content)
engine.runAndWait()