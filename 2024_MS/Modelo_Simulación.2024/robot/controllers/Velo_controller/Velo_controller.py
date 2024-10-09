from controller import Robot #importar la clase Robot
import time #importar la clase time, para usar la función sleep

# Constantes
TIEMPO_PASO = 32  # [ms]
# Asignación de pines de sensores de tierra, en este caso se usan los pines 0, 1 y 2
NUM_SENSORES = 3
S_IZ = 0 # Sensor izquierdo
S_CE = 1 # Sensor central
S_DE = 2 # Sensor derecho
UMBRAL_ROJO = 778  # Ajustar según la intensidad del rojo detectada
TIEMPO_ESPERA = 0.1  # Tiempo de espera en segundos después de detectar el color rojo
VELOCIDAD_MAXIMA = 6.15  # Velocidad máxima del robot
GANANCIA = 0.01  # Reducción de la ganancia para suavizar el movimiento
FILTRO_ERROR = 0.9  # Para suavizar los cambios en el error (valor cercano a 1 reduce más el temblor)

# Inicialización del robot
robot = Robot()
# Obtener el tiempo de paso del robot
time_step = int(robot.getBasicTimeStep())

# Inicialización de motores
motor_izquierdo = robot.getDevice("left wheel motor") # Obtener el motor izquierdo
motor_derecho = robot.getDevice("right wheel motor") # Obtener el motor derecho
motor_izquierdo.setPosition(float('inf')) # Posición infinita para que el motor gire continuamente
motor_derecho.setPosition(float('inf')) # Posición infinita para que el motor gire continuamente

# Obtener el dispositivo emisor
# Se utiliza para enviar mensajes al receptor, en este caso se utiliza
# para enviar el número de vuelta y el tiempo de la vuelta
emisor = robot.getDevice('emitter') # Obtener el dispositivo emisor
emisor.setChannel(1) # Establecer el canal del emisor

# Inicialización de sensores de línea
sensores_terreno = [robot.getDevice(f"gs{i}") for i in range(NUM_SENSORES)] # Obtener los sensores de línea
for sensor in sensores_terreno: # Configurar los sensores de línea
    sensor.enable(time_step) # Habilitar los sensores de línea

# Contador de vueltas
n_vuelta = 0  
fin_pistaroja = False  # Estado del robot después de la vuelta roja
tiempo_inicio_vuelta = time.time()  # Inicialización del tiempo de la primera vuelta

# Inicialización del error previo
error_anterior = 0 # Inicialización del error previo a 0, para evitar errores en la primera vuelta

# Bucle principal
while robot.step(time_step) != -1: #Se ejecuta hasta que el robot se detenga o se detenga el programa
    if n_vuelta >= 4:  # Detener el robot después de 4 vueltas
        break 
   
    # Obtener los valores de los sensores de línea
    valores_sensores = [sensor.getValue() for sensor in sensores_terreno]
    # Obtener el valor del sensor central
    sensor_central = valores_sensores[S_CE]

    # Verificar si se detecta el color rojo en el sensor central y no se ha completado la vuelta roja
    if sensor_central > UMBRAL_ROJO and not fin_pistaroja:
        
        n_vuelta += 1 # Incrementar el contador de vueltas
        tiempo_vuelta = time.time() - tiempo_inicio_vuelta  # Calcular tiempo de la vuelta
        print(f"Número de vueltas: {n_vuelta} Tiempo de la vuelta: {tiempo_vuelta:.2f} segundos")
        print("---------------------------------------------------------------------")
        tiempo_inicio_vuelta = time.time()  # Reiniciar el tiempo para la siguiente vuelta
        fin_pistaroja = True # Marcar la vuelta como completada
        time.sleep(TIEMPO_ESPERA)  # Espera para evitar múltiples detecciones
        
        # Enviar el mensaje al receptor
        #Declaramos una variable mensaje que se le asignara el número y el tiempo de la vuelta de cada recorrido
        mensaje = f"{n_vuelta}-{tiempo_vuelta:.2f}" # Construir el mensaje
        emisor.send(mensaje.encode('utf-8'))  # Enviamos el mensaje
        
    # Verificar si se detecta el color rojo en el sensor central y se ha completado la vuelta roja
    elif sensor_central < UMBRAL_ROJO:
        fin_pistaroja = False  # Restablecer la detección de la vuelta roja

    # Lógica de seguimiento de línea
    error_actual = valores_sensores[S_DE] - valores_sensores[S_IZ]

    # Aplicar filtro de suavizado de error
    error_suavizado = FILTRO_ERROR * error_anterior + (1 - FILTRO_ERROR) * error_actual
    error_anterior = error_suavizado

    # Calcular velocidades basadas en el error suavizado
    velocidad_base = 6.1 # Velocidad base del robot
    # Ajustar la ganancia para suavizar el movimiento
    velocidad_izquierda = velocidad_base - GANANCIA * error_suavizado
    # Ajustar la ganancia para suavizar el movimiento
    velocidad_derecha = velocidad_base + GANANCIA * error_suavizado

    # Establecer velocidades con límites
    # Establecer la velocidad del motor izquierdo y derecho con límites
    motor_izquierdo.setVelocity(max(0.0, min(velocidad_izquierda, VELOCIDAD_MAXIMA))) 
    motor_derecho.setVelocity(max(0.0, min(velocidad_derecha, VELOCIDAD_MAXIMA)))

# Detener los motores al finalizar después de las 4 vueltas
motor_izquierdo.setVelocity(0)
motor_derecho.setVelocity(0)
print("El robot ha completado 4 vueltas y se ha detenido.")
