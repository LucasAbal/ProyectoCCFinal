# main_logic.py
from settings import settings
from foros_logic import *
from ayuda_logic import *
from calcu import *
import discord
import os


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'Hemos iniciado sesión como {client.user}')
    # Enviar mensaje al canal general
    general_channel = client.get_channel(1268342250828464193)
    if general_channel:
        await general_channel.send("¡El bot se ha iniciado! 🥳 El bot está programado para poder ayudarte en la mejora de tu vida ecológica y achicar tu huella de carbono 🤗💚")
        await general_channel.send("Primero: en el canal #foros podrás utilizar los comandos !foros + ambientales, manualidad, reciclo 📖🧐")
        await general_channel.send("Segundo: en el canal #ayuda encontraras videos sobre plantación, ambiente o manualidad, usa !ayuda + alguno de esos 3 📺🙀")
        await general_channel.send("Tercero: Ayuda a seguir mejorando el planeta 😊")
        await general_channel.send("Cuarto: Utiliza nuestra calculadora de huella de carbono personal 🙀😇🐾 usa !calculadora en el canal de #huella-de-carbono")
        await general_channel.send("Dato: La huella de carbono representa el volumen total de gases de efecto invernadero (GEI) que producen las actividades económicas y cotidianas del ser humano. ☘🌱")
        
        script_directory = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_directory, 'img', 'huella-carbono.jpg')
        with open(image_path, 'rb') as image_file:
            image = discord.File(image_file)
            await general_channel.send(file=image)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
     # Llamar a la función procesar_comando_foros desde foros_commands.py
    if message.content.startswith('!foros'):
        await comando_foros(message)
    # Llamar a la función enviar_videos_ayuda desde ayuda_logic.py
    if message.content.startswith('!ayuda'):
        await enviar_videos_ayuda(message)
    # Llamar a la funcion calcular_huella desde calcu.py
    if message.content.startswith('!calculadora'):
        await calcular_huella(client,message)

client.run(settings["TOKEN"])

