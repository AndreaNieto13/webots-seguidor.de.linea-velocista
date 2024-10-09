from controller import Robot, Motor, DistanceSensor

# Constantes
TIEMPO_PASO = 30  # tiempo de paso en milisegundos [ms] 
N_SENSORES_TERRAZA = 3 # n. sensores de lineas 
SEN_IZ= 0 #indice del sensor izquierdo
SEN_DE = 2 #indice del sensor derecho
SEN_CE = 1 #indice del sensor central 


# Parámetros del módulo de seguimiento de línea
VELOCIDAD_MAXIMA = 7  # Velocidad máxima en radianes por segundo
VELOCIDAD_AVANCE = 7.0  # Velocidad de avance ajustada
GANANCIA_RESPUESTA = 0.02  # Ganancia ajustada para una respuesta más suave


# Inicialización del robot y sensores de línea
robot = Robot()
sensores_terreno = [robot.getDevice(f"gs{i}") for i in range(N_SENSORES_TERRAZA)]
valores_sensores = [0] * N_SENSORES_TERRAZA

for sensor in sensores_terreno:
    sensor.enable(TIEMPO_PASO)
    print(f"Inicializado sensor de línea: {sensor.getName()}")

# Inicialización de motores
motor_izquierdo = robot.getDevice("left wheel motor")
motor_derecho = robot.getDevice("right wheel motor")

for motor in (motor_izquierdo, motor_derecho):
    motor.setPosition(float('inf'))
    motor.setVelocity(0.0)

# Función del módulo de seguimiento de línea
def moduloSeguimientoLinea():
    diferencia_sensores = valores_sensores[SEN_DE] - valores_sensores[SEN_IZ]
    
    velocidad_motor_izquierdo = VELOCIDAD_AVANCE - GANANCIA_RESPUESTA * diferencia_sensores
    velocidad_motor_derecho = VELOCIDAD_AVANCE + GANANCIA_RESPUESTA * diferencia_sensores
    
    # Limitar las velocidades
    velocidad_motor_izquierdo = max(min(velocidad_motor_izquierdo, VELOCIDAD_MAXIMA), 0.0)
    velocidad_motor_derecho = max(min(velocidad_motor_derecho, VELOCIDAD_MAXIMA), 0.0)
    
    return velocidad_motor_izquierdo, velocidad_motor_derecho

# Bucle principal
while robot.step(TIEMPO_PASO) != -1:
    # Leer los valores de los sensores de línea
    valores_sensores = [sensor.getValue() for sensor in sensores_terreno]
    
    # Mostrar los valores de los sensores de línea en consola
    print(f"Lectura actual de sensores de línea: {valores_sensores}")
    
    # Ejecutar el módulo de seguimiento de línea
    velocidad_izquierda, velocidad_derecha = moduloSeguimientoLinea()
    
    # Configurar las velocidades de los motores
    motor_izquierdo.setVelocity(velocidad_izquierda)
    motor_derecho.setVelocity(velocidad_derecha)

    # Mostrar las velocidades calculadas en consola
    print(f"Velocidades calculadas - Izquierda: {velocidad_izquierda}, Derecha: {velocidad_derecha}")
    print(f"Velocidades de los motores - Izquierda: {motor_izquierdo.getVelocity()}, Derecha: {motor_derecho.getVelocity()}")
