import smtplib
from email.mime.text import MIMEText
import ollama

# Destino
destinatario = input("Correo destino: ")
instruccion = input("¿Qué quieres enviar? ")

# IA redacta el mensaje
prompt = f"Redacta un correo claro y breve con este contenido: {instruccion}"

respuesta = ollama.chat(
    model='llama3',
    messages=[{'role': 'user', 'content': prompt}]
)

mensaje_texto = respuesta['message']['content']

# Datos cuenta remitente
remitente = "mauricioalexander27121999@gmail.com"
clave = "lxtn lorf fnnr ohbv"

# Crear mensaje
mensaje = MIMEText(mensaje_texto)
mensaje["Subject"] = "Correo automático"
mensaje["From"] = remitente
mensaje["To"] = destinatario

# Enviar
with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
    servidor.starttls()
    servidor.login(remitente, clave)
    servidor.send_message(mensaje)

print("Correo enviado correctamente")
