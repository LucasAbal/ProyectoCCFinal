import asyncio

Co2 = 0

async def esperar_respuesta(client, message, opciones=None):
    def check(m):
        if opciones:
            return m.author == message.author and m.channel == message.channel and m.content.lower() in opciones
        return m.author == message.author and m.channel == message.channel

    try:
        respuesta = await client.wait_for('message', timeout=30.0, check=check)
        return respuesta.content.lower()
    except asyncio.TimeoutError:
        await message.channel.send('Tiempo de espera agotado. No se recibió respuesta.')
        return None

def calcular_emisiones(puntos):
    if puntos <= 0:
        return 0
    elif puntos <= 50:
        return 1.0
    elif puntos <= 100:
        return 2.5
    elif puntos <= 150:
        return 5.0
    else:
        return 10.0

async def calcular_huella(client, message):
    global Co2

    if message.channel.id != 1269417941192020010:
        await message.channel.send('Este comando solo se puede usar en el canal #huella-de-carbono.')
        return

    await message.channel.send('Bienvenido usuario a la calculadora de huella de carbono')
    await message.channel.send('Ahora... ¿podrás responder a algunas preguntas que nos harán saber qué tanto gas emites a la atmósfera? (no te sientas abrumado ;) )')

    await message.channel.send('¿Tienes un auto? (Y/N)')
    respuesta = await esperar_respuesta(client, message)
    
    if respuesta == 'y':
        await message.channel.send('¿Qué tipo de auto tienes? Elige entre las siguientes opciones:')
        await message.channel.send('1. Sedan')
        await message.channel.send('2. SUV')
        await message.channel.send('3. Camioneta')
        await message.channel.send('4. Híbrido')
        tipo_auto = await esperar_respuesta(client, message, ['1', '2', '3', '4'])
        
        if tipo_auto == '1':
            Co2 += 10
        elif tipo_auto == '2':
            Co2 += 15
        elif tipo_auto == '3':
            Co2 += 20
        elif tipo_auto == '4':
            Co2 += 5
        
        await message.channel.send('¿Con qué frecuencia usas tu auto? Elige entre las siguientes opciones:')
        await message.channel.send('1. Diario')
        await message.channel.send('2. Semanalmente')
        await message.channel.send('3. Mensualmente')
        frecuencia = await esperar_respuesta(client, message, ['1', '2', '3'])
        
        if frecuencia == '1':
            Co2 += 30
        elif frecuencia == '2':
            Co2 += 10
        elif frecuencia == '3':
            Co2 += 5
        
        await message.channel.send('¿Con qué frecuencia viajas en avión? Elige entre las siguientes opciones:')
        await message.channel.send('1. Más de 3 veces al año')
        await message.channel.send('2. 1-3 veces al año')
        await message.channel.send('3. Raramente')
        viajes_avion = await esperar_respuesta(client, message, ['1', '2', '3'])
        
        if viajes_avion == '1':
            Co2 += 50
        elif viajes_avion == '2':
            Co2 += 20
        elif viajes_avion == '3':
            Co2 += 5
        
        await message.channel.send('¿Qué tipo de vivienda tienes? Elige entre las siguientes opciones:')
        await message.channel.send('1. Casa independiente')
        await message.channel.send('2. Departamento')
        await message.channel.send('3. Vivienda en edificio')
        vivienda = await esperar_respuesta(client, message, ['1', '2', '3'])
        
        if vivienda == '1':
            Co2 += 20
        elif vivienda == '2':
            Co2 += 10
        elif vivienda == '3':
            Co2 += 15
        
        await message.channel.send('¿Qué tipo de alimentación sigues? Elige entre las siguientes opciones:')
        await message.channel.send('1. Dieta basada en carne')
        await message.channel.send('2. Dieta mixta (carne y vegetales)')
        await message.channel.send('3. Dieta vegetariana')
        await message.channel.send('4. Dieta vegana')
        dieta = await esperar_respuesta(client, message, ['1', '2', '3', '4'])
        
        if dieta == '1':
            Co2 += 40
        elif dieta == '2':
            Co2 += 20
        elif dieta == '3':
            Co2 += 10
        elif dieta == '4':
            Co2 += 5
        
        await message.channel.send('¿Con qué frecuencia reciclas? Elige entre las siguientes opciones:')
        await message.channel.send('1. Siempre')
        await message.channel.send('2. A menudo')
        await message.channel.send('3. A veces')
        await message.channel.send('4. Nunca')
        reciclaje = await esperar_respuesta(client, message, ['1', '2', '3', '4'])
        
        if reciclaje == '1':
            Co2 -= 10
        elif reciclaje == '2':
            Co2 -= 5
        elif reciclaje == '3':
            Co2 -= 2
        elif reciclaje == '4':
            pass
        
        emisiones = calcular_emisiones(Co2)
        await message.channel.send(f'Gracias por tus respuestas. Tu huella de carbono estimada es {emisiones:.2f} toneladas de CO2 por año.')

    elif respuesta == 'n':
        await message.channel.send('Entendido. Si cambias de opinión, solo envía `!calculadora` para reiniciar.')

    else:
        await message.channel.send('Respuesta no válida. Por favor, responde con `Y` o `N`.')
