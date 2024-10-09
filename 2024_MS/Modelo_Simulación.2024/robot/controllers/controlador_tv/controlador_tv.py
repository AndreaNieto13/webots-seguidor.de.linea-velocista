from controller import Robot # Importar la clase Robot de la biblioteca controller
import time # Importar la clase time de la biblioteca time

# Inicializar el robot
robot = Robot()

# Configuración del display y receptor
display = robot.getDevice('ds_tv') # Obtener el dispositivo display
timeStep = int(robot.getBasicTimeStep()) # Obtener el tiempo de paso básico

# Configurar el receptor
receptor = robot.getDevice('receiver') # Obtener el dispositivo receptor
receptor.enable(timeStep) # Habilitar el receptor
receptor.setChannel(1) # Establecer el canal del receptor

# Obtener el tamaño del display
width = display.getWidth() # Obtener el ancho del display ya estipulado en el children del ds__tv
height = display.getHeight() # Obtener la altura del display ya estipulado en el children del ds__tv

# Tamaño de fuente 
sizeFont = 55 
background_color = 0xFFFFFF  # Fondo blanco
text_color = 0x000000  # Texto negro

# Configurar fuente Arial, tamaño de letra y negrita
display.setFont("Lucida Console", sizeFont, True)

# Definir posiciones de texto
alignTextX = (width - sizeFont) / 5  #texto en el eje x, asi mismo estara en el centro del display
alignTextY = height / 4 #  el texto en el eje y, asi mismo estara en el centro del display

#bucle principal 

#aqui aplicamos el tiempo de paso básico, siempre y cuando el robot este activo
while robot.step(timeStep) != -1: 

    # Verificar si el receptor está recibiendo mensajes
    if receptor.getQueueLength() > 0: # Si el receptor está recibiendo mensajes
        message = receptor.getString()  # Obtener el mensaje

        # Decodificar y mostrar el mensaje recibido
        print(f"Mensaje recibido: {message}")  # Mostrar el mensaje en la consola
        
        receptor.nextPacket() # Obtener el siguiente paquete, si hay uno más en la cola

        # Dividir el mensaje para obtener el número de vuelta y tiempo
        n_vuelta, tiempo_vuelta = message.split('-')
        
        # Limpiar el display y mostrar texto nítido
        display.setColor(background_color) # Fondo blanco 
        display.fillRectangle(0, 0, width, height)  # Limpia el display con el color de fondo

        # Dibujar texto en color negro
        display.setColor(text_color) # Color negro
        display.drawText(f"Vuelta {n_vuelta}", alignTextX, alignTextY) # Ajuste de posición para evitar superposición
        display.drawText(f"{tiempo_vuelta} seg", alignTextX, alignTextY+100 )  # Ajuste de posición para evitar superposición
    
    else:
        print("No hay mensajes en la cola del receptor")  # Depuración





