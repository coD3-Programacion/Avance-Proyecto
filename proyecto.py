import random
import time
import json 
import pygame
import sys
# Variables globales
tamaño_tablero = 10
espacio_sin_abrir = "."
cantidad_minas = 10
limite_tiempo = 0
modo_de_juego = " "
modo_de_dificultad = " "
nombre_usuario = ""
tiempo_final = 0
minas_correctamente_señaladas = 0
puntaje = 1
lista_minas_señaladas = []
mayores_puntuaciones_clasico = {}
mayores_puntuaciones_contrarreloj = {} 
colores = {
    "NEGRO"  :   (0,0,0),    
    "BLANCO" :   (255,255,255),
    "VERDE"  :   (0, 255,0),
    "ROJO"    :   (255,0,0),
    "AZUL"    :   (0,0,255),
    "GRIS"    :   (80,80,80),
    "BRONCE"  :   (205,150, 50)
}

# Función para generar y mostrar la matriz del tablero
# Función para generar y mostrar la matriz del tablero
def matriz_falsa_funcion():
    global matriz_falsa
    matriz_falsa = []

    # Encabezado de columnas ajustado para cualquier tamaño de tablero
    encabezado_columnas = "    " + "  ".join([f"{i:2}" for i in range(1, tamaño_tablero + 1)])
    matriz_falsa.append(encabezado_columnas)

    # Generar las filas del tablero
    for fila in range(tamaño_tablero):
        fila_matriz = [f"{fila + 1:2}"]  # Encabezado de fila ajustado
        for columna in range(tamaño_tablero):
            fila_matriz.append(espacio_sin_abrir)  # Espacio sin abrir
        matriz_falsa.append(fila_matriz)

def imprimir_tablero():
    # Imprimir encabezado de columnas
    print(matriz_falsa[0])

    # Imprimir filas con valores dentro de la cuadrícula
    for fila in range(1, tamaño_tablero + 1):
        # Dibujar línea horizontal superior ajustada
        print("   " + "-" * (3 * tamaño_tablero + tamaño_tablero + 1))

        # Dibujar la fila con valores
        fila_str = f"{fila:2} |"  # Encabezado de fila ajustado a dos dígitos
        for columna in range(1, tamaño_tablero + 1):
            fila_str += f" {matriz_falsa[fila][columna]} |"
        print(fila_str)

    # Dibujar la última línea inferior
    print("   " + "-" * (3 * tamaño_tablero + tamaño_tablero + 1))
            
#Se crea una funcion para crear la matriz donde va a ir toda la logica             
def matriz_real_funcion():
    global matriz_real
    matriz_real = []
    filas_matriz_real = []
    
    # Crear la matriz lógica con ceros
    for i in range(tamaño_tablero):
        for j in range(tamaño_tablero):
            filas_matriz_real.append(0)#Los elementos de la matriz se inicializan como 0  
        matriz_real.append(filas_matriz_real)
        filas_matriz_real = []

#Funcion para que el usuario pueda elegir si va a jugar en el terminal o en la ventana emergente 
def menu_principal():
    global lista_minas_señaladas
    #Se imprime el titulo y las reglas del juego
    print("--------------------------------------------------------------------------------------------------------")
    print("-----------------------------------------------BUSCAMINAS-----------------------------------------------")
    print("--------------------------------------------------------------------------------------------------------")
    print('\n \
    -El juego consiste en señalar todas las minas\n \
    -El número en una casilla indica el número de minas alrededor (en todas sus casillas adyacentes)\n \
    -Si destapas una casilla que es mina pierdes el juego\n \
    -Las minas se pueden señalar o marcar con "banderas"\n')

    print("------------------------------------------------JUGAR(Presiona J)----------------------------------------")
    print("------------------------------------------------CARGAR PARTIDA(Presiona C)-------------------------------")
    print("------------------------------------------------PUNTAJES MAS ALTOS(Presiona P)---------------------------")    
    entrada_usuario = str(input("Por favor ingrese su respuesta: "))
    if entrada_usuario.lower() not in ["j", "c", "p"]:#Si no es una entrada valida se le vuelve a pedir que ingrese su respuesta
        while entrada_usuario.lower() not in ["j", "c", "p"]:
            print("Por favor ingresa un valor valido.")
            entrada_usuario = str(input("Por favor ingrese su respuesta: "))
    if entrada_usuario.lower() == "j":
        print("¿Quieres jugar en la terminal de Python(presiona t) o quieres jugar en una ventana emergente(Presiona v)?")
        while True:
            x = str(input("Por favor ingrese su respuesta: "))#Si no es una entrada valida se le vuelve a pedir que ingrese su respuesta
            if x.lower() in ["t", "v"]:
                break
            else: 
                print("Por favor ingresar un valor valido.")
        if x.lower() == "t":#Se llaman a las demas funciones 
            jugar_terminal()
        elif x.lower() == "v":
            matriz_falsa_funcion()
            matriz_real_funcion()
            colocar_minas()
            pygames()
    elif entrada_usuario.lower() == "c":
        try:
            crear_partida_guardada()
        except TypeError:
            print("Primero debes guardar una partida")
    elif entrada_usuario.lower() == "p":
        imprimir_puntajes()

#Funcion para que el usuario pueda elegir en que modo de juego y dificultad va a jugar
def menu_terminal():
    global cantidad_minas, tamaño_tablero, lista_numeros, limite_tiempo, modo_de_juego, nombre_usuario, modo_de_dificultad 

    nombre_usuario = str(input("Por favor ingresa tu nombre o usuario = "))

    print("-----------------------------------------------Modo de Juego--------------------------------------------")
    print("Elige el modo de juego en el que quieres jugar: ")#se le pregunta al usuario que modo de juego va a jugar
    print("\n \
          -Contrarreloj (Escribe c)\n \
          -Clásico (Escribe cl)")
    while True:
        modo_de_juego = input("Por favor ingrese el modo de juego en el que desea jugar: ").lower()#Si no es una entrada valida se le vuelve a pedir que ingrese su respuesta
        if modo_de_juego in ["c", "cl"]:
            break
        else:
            print("Por favor ingrese un valor válido.")

    print("-----------------------------------------------Dificultad-----------------------------------------------")
    print("Elige el nivel de dificultad en el que quieres jugar: ")#Se le pregunta al usuario en que modo de juego va a jugar
    print("\n \
          -Fácil (Escribe F)\n \
          -Mediano (Escribe M)\n \
          -Difícil (Escribe d)\n \
          -Muy difícil (Escribe md)\n \
          -Legendario (Escribe L)\n \
          -Personalizado (Escribe E)\n")
    while True:
        modo_de_dificultad = input("Ingresa el nivel de dificultad en el que quieres jugar: ").lower()
        if modo_de_dificultad == "f":
            cantidad_minas = 5
            tamaño_tablero = 7
            lista_numeros = [str(i) for i in range(1, tamaño_tablero + 1)]
            limite_tiempo = 90
            break
        elif modo_de_dificultad == "m":
            cantidad_minas = 10
            tamaño_tablero = 10
            lista_numeros = [str(i) for i in range(1, tamaño_tablero + 1)]
            limite_tiempo = 180
            break
        elif modo_de_dificultad == "d":
            cantidad_minas = 20
            tamaño_tablero = 15
            lista_numeros = [str(i) for i in range(1, tamaño_tablero + 1)]
            limite_tiempo = 300
            break
        elif modo_de_dificultad == "md":
            cantidad_minas = 40
            tamaño_tablero = 30
            lista_numeros = [str(i) for i in range(1, tamaño_tablero + 1)]
            limite_tiempo = 600
            break    
        elif modo_de_dificultad == "l":
            cantidad_minas = 150
            tamaño_tablero = 30
            lista_numeros = [str(i) for i in range(1, tamaño_tablero + 1)]
            limite_tiempo = 1200
            break
        elif modo_de_dificultad == "e":
            tamaño_tablero = int(input("Por favor ingrese el tamaño del tablero deseado: "))
            cantidad_minas = int(input("Por favor ingrese la cantidad de minas deseada: "))
            x = input("¿Quieres jugar en contrarreloj? (Responde con si o no): ").lower()
            if x == "si":
                while True:
                    try:
                        limite_tiempo = int(input("Por favor ingresa el límite de tiempo con el que quieres jugar (en segundos): "))
                        break
                    except ValueError:
                        print("Error: Por favor ingresa un número válido.")
            else:
                limite_tiempo = 0  # Sin límite de tiempo
            lista_numeros = [str(i) for i in range(1, tamaño_tablero + 1)]
            break
        else: 
            print("Por favor ingrese un valor válido.")

def colocar_minas():
    numero_minas = 0

    while numero_minas < cantidad_minas:
        fila_mina = random.randint(0, tamaño_tablero - 1) 
        columna_mina = random.randint(0, tamaño_tablero - 1)

        # Asegurarse de que no se coloque una mina en una posición ya ocupada
        if matriz_real[fila_mina][columna_mina] == "*":
            continue  # Saltar a la siguiente iteración si ya hay una mina aquí
        
        # Colocar la mina
        matriz_real[fila_mina][columna_mina] = "*" 
        
        # Actualizar las celdas adyacentes
        for i in range(fila_mina - 1, fila_mina + 2):
            for j in range(columna_mina - 1, columna_mina + 2):
                if 0 <= i < tamaño_tablero and 0 <= j < tamaño_tablero:
                    if matriz_real[i][j] != "*":
                        matriz_real[i][j] += 1
        
        numero_minas += 1

def ingresar_verificar_posicion():
     
    global lista_numeros
    print('\nIngrese una posición que desee destapar o señalar como una mina separándola con "-" de la siguiente manera M-fila-columna: ("M" para señalar mina o "D" para destapar, ej: D-9-1, M-10-8)\n \
          -Si desea guardar la partida presione G-G-G ')
    
    while True:
        usuario_posicion = input("Ingrese posición: ").upper()
        lista_usuario_posicion = usuario_posicion.split("-")
    
        # Validar el formato de entrada
        if len(lista_usuario_posicion) != 3:
            print("\nIngreso una posición incorrecta (no tiene 3 partes separadas por '-'), intente de nuevo.")
            continue

        accion, fila, columna = lista_usuario_posicion

        # Se verifica si el usuario quiere guardar la partida.    
        if usuario_posicion == "G-G-G":
            guardar_partida(nombre_archivo="archivos.json")
            return accion, fila, columna        
        
        if accion not in ["M", "D"]:
            print('\nIngreso una posición incorrecta (el primer carácter debe ser "M" o "D"), intente de nuevo.')
            continue 
        
        if fila not in lista_numeros or columna not in lista_numeros:
            print("\nIngreso una posición incorrecta (la fila o columna está fuera del rango), intente de nuevo.")
            continue
        
        # Convertir fila y columna a enteros
        fila = int(fila)
        columna = int(columna)
        
        # Verificar que la fila y columna estén dentro del tablero
        if not (1 <= fila <= tamaño_tablero) or not (1 <= columna <= tamaño_tablero):
            print("\nIngreso una posición incorrecta (la fila o columna está fuera del tablero), intente de nuevo.")
            continue
        
        return accion, fila, columna

def casillas_adyacentes(fila_escogida, columna_escogida):
    direcciones = [(-1, -1), (-1, 0), (-1, 1),(0, -1),(0, 1),(1, -1),(1, 0),(1, 1)]

    # Verificar si la posición ya fue destapada
    if matriz_falsa[fila_escogida][columna_escogida] != espacio_sin_abrir:
        return

    # Si la celda en la matriz real es 0, destapar las adyacentes
    if matriz_real[fila_escogida-1][columna_escogida-1] == 0:
        matriz_falsa[fila_escogida][columna_escogida] = "0" 
        
        for direccion in direcciones:
            fila_adicional = fila_escogida + direccion[0]
            columna_adicional = columna_escogida + direccion[1]

            if 1 <= fila_adicional <= tamaño_tablero and 1 <= columna_adicional <= tamaño_tablero:
                if matriz_falsa[fila_adicional][columna_adicional] == espacio_sin_abrir:
                    if matriz_real[fila_adicional - 1][columna_adicional - 1] == 0:
                        casillas_adyacentes(fila_adicional, columna_adicional)
                    else:
                        matriz_falsa[fila_adicional][columna_adicional] = f"{matriz_real[fila_adicional - 1][columna_adicional - 1]}"
    
    else:
        matriz_falsa[fila_escogida][columna_escogida] = f" {matriz_real[fila_escogida-1][columna_escogida-1]} "

def destapar_celda(bandera_o_destapar, fila_escogida, columna_escogida):
    global minas_correctamente_señaladas
    global lista_minas_señaladas
    global lista_banderas

    fila_idx = fila_escogida - 1
    columna_idx = columna_escogida - 1
    lista_banderas = {}

    if bandera_o_destapar == "M": 
        matriz_falsa[fila_escogida][columna_escogida] = "\U0001F6A9"
        if matriz_real[fila_idx][columna_idx] == "*" and (fila_escogida, columna_escogida) not in lista_minas_señaladas:
            minas_correctamente_señaladas += 1
            lista_minas_señaladas.append((fila_escogida, columna_escogida))
        
            if minas_correctamente_señaladas == cantidad_minas:
                imprimir_tablero()
                print("\n--------------------------------------------------------------------------------------------------------")
                print("------------------------HAS SEÑALADO TODAS LAS MINAS CORRECTAMENTE! HAS GANADO!-------------------------")
                print("--------------------------------------------------------------------------------------------------------")
                return True 
    
    elif bandera_o_destapar == "D":
        casillas_adyacentes(fila_escogida, columna_escogida)
        matriz_falsa[fila_escogida][columna_escogida] = f"{matriz_real[fila_idx][columna_idx]}"
        
        if matriz_real[fila_idx][columna_idx] == "*":
            matriz_falsa[fila_escogida][columna_escogida] = "\U0001F4A3"
            imprimir_tablero()
            print("\n--------------------------------------------------------------------------------------------------------")
            print("-----------------------------------HAS PISADO UNA MINA! GAME OVER!----------------------------------------")
            print("----------------------------------------------------------------------------------------------------------")
            return True

    # Imprimir la matriz actualizada
    imprimir_tablero()

    return False  # El juego continúa

def transcurso_juego():
    global modo_de_juego, limite_tiempo, tiempo_final, tiempo_restante
    # Inicializar el tiempo solo si es modo "c" (con límite de tiempo)
    if modo_de_juego == "c":
        inicio = time.time()
    else:
        inicio = None  # No se usa en modo clásico
    
    # Ciclo principal del juego
    while True:
        #Se verifica si el usuario quiere guardar la partida
        bandera_o_destapar, fila_escogida, columna_escogida = ingresar_verificar_posicion()
        if bandera_o_destapar == "G" and fila_escogida == "G" and columna_escogida == "G":
            tiempo_restante = limite_tiempo - int(tiempoTranscurrido)
            print("\n-----------------------------------------------------------------------------------------")
            print("-----------------------------------PARTIDA GUARDADA----------------------------------------")
            print("-------------------------------------------------------------------------------------------")
            break

        # Llamar a la función para destapar la celda o marcar una mina
        Terminar = destapar_celda(bandera_o_destapar, fila_escogida, columna_escogida)
        # Verificar si el juego ha terminado (ganar o pisar una mina)
        if Terminar == True:
            break
        # Si el modo de juego es contrarreloj, verificar el tiempo transcurrido
        if modo_de_juego == "c":
            tiempoTranscurrido = time.time() - inicio
            if tiempoTranscurrido >= limite_tiempo:
                imprimir_tablero()
                print("\n--------------------------------------------------------------------------------------------------------")
                print("-----------------------------------FIN DEL TIEMPO! GAME OVER!--------------------------------------------")
                print("--------------------------------------------------------------------------------------------------------")
                tiempo_final = 1
                break
            else:
                #Mostrar el tiempo restante
                tiempo_restante = limite_tiempo - int(tiempoTranscurrido)
                tiempo_final = tiempo_restante
                print(f"Tiempo restante: {tiempo_restante} segundos")

def puntuaciones():
    global tiempo_final,minas_correctamente_señaladas, puntaje, modo_de_dificultad, modo_de_juego
    if modo_de_juego.lower() == "c":
        valor_nivel = 1
        if modo_de_dificultad == "f":
            valor_nivel = 1
        elif modo_de_dificultad == "m":
            valor_nivel = 10 
        elif modo_de_dificultad == "d":
            valor_nivel = 100
        elif modo_de_dificultad == "md":
            valor_nivel = 500    
        elif modo_de_dificultad == "l":
            valor_nivel = 1000
        elif modo_de_dificultad == "e":
            valor_nivel = cantidad_minas * (1000/150) 
        
        puntaje = ((minas_correctamente_señaladas*500)*valor_nivel) +10/(1/tiempo_final)

        print(f"El nivel de dificultad fue {modo_de_dificultad}\n \
            La cantidad de minas señaladas correctamente es {minas_correctamente_señaladas}\n \
            Felicidades tu puntaje fue {puntaje}")
    elif modo_de_juego.lower() == "cl":
        puntaje = minas_correctamente_señaladas*500
        print(f"El nivel de dificultad fue {modo_de_dificultad}\n \
            La cantidad de minas señaladas correctamente es {minas_correctamente_señaladas}\n \
            Felicidades tu puntaje fue {puntaje}")
        


def guardar_partida(nombre_archivo="partida_guardada.json"):
    global matriz_real, lista_minas_señaladas, matriz_falsa, modo_de_dificultad, modo_de_juego, tiempo_restante, tamaño_tablero, lista_numeros
    datos_partida = {
        "matriz_real": list(matriz_real),
        "tablero": list(matriz_falsa),
        "tamaño tablero": int(tamaño_tablero),
        "banderas": list(lista_minas_señaladas),
        "modo de dificultad": str(modo_de_dificultad),
        "modo de juego": str(modo_de_juego),
        "tiempo restante": int(tiempo_restante),
        "lista numeros": list(lista_numeros)
    }
    with open(nombre_archivo, "w") as archivo:
        json.dump(datos_partida, archivo)
    return datos_partida


def cargar_partida():
    nombre_archivo="archivos.json"
    try:
        with open(nombre_archivo, "r") as archivo:
            datos_partida = json.load(archivo)  

        print(f"Partida cargada desde {nombre_archivo}")
        return datos_partida
    except FileNotFoundError:
        print(f"No se encontro ninguna partida guardada.")
        return None
    
def crear_partida_guardada():
    global matriz_real, lista_minas_señaladas, matriz_falsa, modo_de_dificultad, modo_de_juego, tiempo_restante,limite_tiempo, tamaño_tablero, lista_numeros
    datos_partida = {}
    datos_partida = cargar_partida()
    tamaño_tablero = datos_partida["tamaño tablero"]
    lista_minas_señaladas = datos_partida["banderas"]
    matriz_falsa = datos_partida["tablero"]
    modo_de_dificultad = datos_partida["modo de dificultad"]
    modo_de_juego = datos_partida["modo de juego"]
    tiempo_restante = datos_partida["tiempo restante"]
    matriz_real = datos_partida["matriz_real"]

    print("-------------------------------------------------------------------------------------------------------")
    print("--------------------------------PARTIDA CARGADA CORRECTAMENTE------------------------------------------")
    print("-------------------------------------------------------------------------------------------------------")

    lista_numeros = [str(i) for i in range(1, tamaño_tablero + 1)]    
        
    imprimir_tablero()
    inicio = time.time()
    while True:
        #Se verifica si el usuario quiere guardar la partida
        bandera_o_destapar, fila_escogida, columna_escogida = ingresar_verificar_posicion()
        if bandera_o_destapar == "G" and fila_escogida == "G" and columna_escogida == "G":
            print("\n-----------------------------------------------------------------------------------------")
            print("-----------------------------------PARTIDA GUARDADA----------------------------------------")
            print("-------------------------------------------------------------------------------------------")
            break

        # Llamar a la función para destapar la celda o marcar una mina
        Terminar = destapar_celda(bandera_o_destapar, fila_escogida, columna_escogida)
        # Verificar si el juego ha terminado (ganar o pisar una mina)
        if Terminar == True:
            break
        
        # Si el modo de juego es contrarreloj, verificar el tiempo transcurrido
        if modo_de_juego == "c":
            limite_tiempo = tiempo_restante
            tiempoTranscurrido = time.time() - inicio
            if tiempoTranscurrido >= limite_tiempo:
                imprimir_tablero()
                print("\n--------------------------------------------------------------------------------------------------------")
                print("-----------------------------------FIN DEL TIEMPO! GAME OVER!--------------------------------------------")
                print("--------------------------------------------------------------------------------------------------------")
                tiempo_final = 1
                break
            else:
                #Mostrar el tiempo restante
                tiempo_restante = limite_tiempo - int(tiempoTranscurrido)
                tiempo_final = tiempo_restante
                print(f"Tiempo restante: {tiempo_restante} segundos")
    puntuaciones()

def jugar_terminal():
    # Inicializar las variables con las que se gana el juego
    minas_correctamente_señaladas = 0
    lista_minas_señaladas = []
    
    # Crear la matriz falsa y la matriz lógica
    menu_terminal()
    matriz_falsa_funcion()
    matriz_real_funcion()
    colocar_minas()
    imprimir_tablero()
    
    # Iniciar el ciclo principal del juego
    transcurso_juego()
    puntuaciones()
    puntuaciones_mas_altas()
    
    # Verificar si el juego terminó por señalamiento correcto de todas las minas
    if minas_correctamente_señaladas == cantidad_minas:
        print("¡Felicidades! Has ganado el juego.")
    else:
        print("Gracias por jugar.")

def puntuaciones_mas_altas():
    global nombre_usuario, mayores_puntuaciones_clasico, mayores_puntuaciones_contrarreloj, modo_de_dificultad
    if modo_de_juego == "c":
        #Se define un diccionario para los mayores puntajes
        mayores_puntuaciones_contrarreloj = {
            "1" : {
                "nombre_usuario": "0",
                "modo_de_dificultad": "0", 
                "puntaje": 0
            },
            "2":{"nombre_usuario": "0",
                "modo_de_dificultad": "0", 
                "puntaje" : 0},
            "3":{"nombre_usuario": "0",
                "modo_de_dificultad": "0", 
                "puntaje" : 0},
        }
    elif modo_de_juego == "cl":
                mayores_puntuaciones_clasico = {
            "1":{
                "nombre_usuario": "0",
                "modo_de_dificultad" : "0", 
                "puntaje" : 0
            },
            "2":{ 
                "nombre_usuario" : "0",
                "modo_de_dificultad" : "0", 
                "puntaje" : 0},
            "3":{  
                "nombre_usuario" : "0",
                "modo_de_dificultad" : "0", 
                "puntaje" : 0}
        }
    #Segun que tan grande sea el puntaje los puntajes cambian de puesto
    if modo_de_juego == "c":
        if puntaje > mayores_puntuaciones_contrarreloj["1"]["puntaje"] and mayores_puntuaciones_contrarreloj["1"]["puntaje"] == 0:
            mayores_puntuaciones_contrarreloj["1"]["puntaje"] = puntaje
            mayores_puntuaciones_contrarreloj["1"]["modo_de_dificultad"] = modo_de_dificultad
            mayores_puntuaciones_contrarreloj["1"]["nombre_usuario"] = nombre_usuario
        if puntaje > mayores_puntuaciones_contrarreloj["1"]["puntaje"]:
            mayores_puntuaciones_contrarreloj["3"] = mayores_puntuaciones_contrarreloj["2"]
            mayores_puntuaciones_contrarreloj["2"] = mayores_puntuaciones_contrarreloj["1"]
            mayores_puntuaciones_contrarreloj["1"]["puntaje"] = puntaje
            mayores_puntuaciones_contrarreloj["1"]["modo_de_dificultad"] = modo_de_dificultad
            mayores_puntuaciones_contrarreloj["1"]["nombre_usuario"] = nombre_usuario
        elif mayores_puntuaciones_contrarreloj["2"]["puntaje"] < puntaje < mayores_puntuaciones_contrarreloj["1"]["puntaje"]:
            mayores_puntuaciones_contrarreloj["3"] = mayores_puntuaciones_contrarreloj["2"]
            mayores_puntuaciones_contrarreloj["2"]["puntaje"] = puntaje
            mayores_puntuaciones_contrarreloj["2"]["modo_de_dificultad"] = modo_de_dificultad
            mayores_puntuaciones_contrarreloj["2"]["nombre_usuario"] = nombre_usuario
        elif mayores_puntuaciones_contrarreloj["3"]["puntaje"] < puntaje < mayores_puntuaciones_contrarreloj["2"]["puntaje"]:
            mayores_puntuaciones_contrarreloj["3"]["puntaje"] = puntaje
            mayores_puntuaciones_contrarreloj["3"]["modo_de_dificultad"] = modo_de_dificultad
            mayores_puntuaciones_contrarreloj["3"]["nombre_usuario"] = nombre_usuario

    if modo_de_juego == "cl":
        if puntaje > mayores_puntuaciones_clasico["1"]["puntaje"]:
            mayores_puntuaciones_clasico["3"] = mayores_puntuaciones_clasico["2"]
            mayores_puntuaciones_clasico["2"] = mayores_puntuaciones_clasico["1"]
            mayores_puntuaciones_clasico["1"]["puntaje"] = puntaje
            mayores_puntuaciones_clasico["1"]["modo_de_dificultad"] = modo_de_dificultad
            mayores_puntuaciones_clasico["1"]["nombre_usuario"] = nombre_usuario
        elif mayores_puntuaciones_clasico["2"]["puntaje"] < puntaje < mayores_puntuaciones_clasico["1"]["puntaje"]:
            mayores_puntuaciones_clasico["3"] = mayores_puntuaciones_clasico["2"]
            mayores_puntuaciones_clasico["2"]["puntaje"] = puntaje
            mayores_puntuaciones_clasico["2"]["modo_de_dificultad"] = modo_de_dificultad
            mayores_puntuaciones_clasico["2"]["nombre_usuario"] = nombre_usuario
        elif mayores_puntuaciones_clasico["3"]["puntaje"] < puntaje < mayores_puntuaciones_clasico["2"]["puntaje"]:
            mayores_puntuaciones_clasico["3"]["puntaje"] = puntaje
            mayores_puntuaciones_clasico["3"]["modo_de_dificultad"] = modo_de_dificultad
            mayores_puntuaciones_clasico["3"]["nombre_usuario"] = nombre_usuario

    with open("puntuaciones_contrarreloj.json", "w") as writeFile:
        json.dump(mayores_puntuaciones_contrarreloj, writeFile)

    with open("puntuaciones_clasico.json", "w") as writeFile:
        json.dump(mayores_puntuaciones_clasico, writeFile)

def imprimir_puntajes():
    print("Quieres ver los puntajes del modo contrarreloj(presiona c) o del modo clasico(presiona cl)?")
    with open("puntuaciones_contrarreloj.json", "r") as readFile:
        puntuaciones_contrarreloj: dict = json.load(readFile)
    with open("puntuaciones_clasico.json", "r") as readFile:
        puntuaciones_clasico: dict = json.load(readFile)  
    while True:
        x = str(input("Por favor ingrese la respuesta: "))
        if x.lower() in ["c", "cl"]:
            break
        else:
            print("Por favor ingrese un valor valido.")
    print("--------------------------------------------------------------------------------------------------------")
    print("------------------------------------------MAYORES PUNTUACIONES------------------------------------------")
    print("--------------------------------------------------------------------------------------------------------")
    if x.lower() == "c":
        print("|NOMBRE USUARIO       |MODO DE DIFICULTAD        |PUNTAJE")
        print("------------------------------------------------------------------")
        for key in puntuaciones_contrarreloj:
            puntaje = puntuaciones_contrarreloj[key].get("puntaje", "N/A")
            modo_de_dificultad = puntuaciones_contrarreloj[key].get("modo_de_dificultad", "N/A")
            nombre_usuario = puntuaciones_contrarreloj[key].get("nombre_usuario", "N/A")
            print(f"|{nombre_usuario}                    |{modo_de_dificultad}                         |{puntaje}       ")
            print("------------------------------------------------------------------")

    elif x.lower() == "cl":
        print("|NOMBRE USUARIO       |MODO DE DIFICULTAD        |PUNTAJE")
        print("------------------------------------------------------------------")
        for key in puntuaciones_clasico:
            puntaje = puntuaciones_clasico[key].get("puntaje")
            modo_de_dificultad = puntuaciones_clasico[key].get("modo_de_dificultad")
            nombre_usuario = puntuaciones_clasico[key].get("nombre_usuario")
            print(f"|{nombre_usuario}                    |{modo_de_dificultad}                         |{puntaje}       ")
            print("------------------------------------------------------------------")


# Variables globales (declarar colores o cualquier otra variable necesaria antes)
colores = {
    "BLANCO": (255, 255, 255),
    "NEGRO": (0, 0, 0),
    "BRONCE": (205, 127, 50),
    "GRIS": (128, 128, 128),
}

# Variables globales del juego
ancho_celda = 30
alto_celda = 30
margen = 5
tamaño_tablero = 10  # Se modificará según la dificultad seleccionada
cantidad_minas = 10
matriz_real = []
posiciones_celdas = []

# Colores
colores = {
    "BRONCE": (205, 127, 50),
    "BLANCO": (255, 255, 255),
    "NEGRO": (0, 0, 0),
    "GRIS": (128, 128, 128)
}

def pygames():
    # Inicialización
    pygame.init()
    tamaño = (900, 600)
    pantalla = pygame.display.set_mode(tamaño)
    clock = pygame.time.Clock()
    pygame.display.set_caption("BUSCAMINAS")
    button_font = pygame.font.Font(None, 40)
    font = pygame.font.Font(None, 36)
    title_font = pygame.font.Font(None, 80)
    
    global ancho_celda, alto_celda, celdas, cantidad_minas, matriz_real, tamaño_tablero, matriz_pygame_visual, ganar, tiempo_inicial, cronometro, limite_tiempo, final_tiempo
    cronometro = False
    limite_tiempo = 0
    final_tiempo = False 
    ganar = False
    margen = 5
    tamaño_tablero = 15  # Tamaño inicial del tablero
    # Generación de celdas con un estado inicial cubierto
    celdas = [[{"rect": None, "estado": "cubierto"} for _ in range(tamaño_tablero)] for _ in range(tamaño_tablero)]

    # Generación de matriz visual
    def generar_matriz():
        espacio_sin_abrir = "."
        matriz_visual = []
        for fila in range(tamaño_tablero):
            fila_matriz = [espacio_sin_abrir] * tamaño_tablero
            matriz_visual.append(fila_matriz)
        return matriz_visual
    
    def matriz_real_f(tamaño_tablero):
        global matriz_pygame
        matriz_pygame = []
        
        # Crear la matriz lógica con ceros
        for i in range(tamaño_tablero):
            filas_matriz_real = [0] * tamaño_tablero
            matriz_pygame.append(filas_matriz_real)

    def casillas_adyacentes(fila_escogida, columna_escogida, matriz_pygame, matriz_visual, tamaño_tablero, espacio_sin_abrir):
        direcciones = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        # Verificar si la posición ya fue destapada
        if matriz_visual[fila_escogida][columna_escogida] != espacio_sin_abrir:
            return

        # Si la celda en la matriz real es 0, destapar las adyacentes
        if matriz_pygame[fila_escogida][columna_escogida] == 0:
            matriz_visual[fila_escogida][columna_escogida] = "0"

            # Explorar las direcciones adyacentes
            for direccion in direcciones:
                fila_adicional = fila_escogida + direccion[0]
                columna_adicional = columna_escogida + direccion[1]

                # Verificar que las posiciones estén dentro de los límites de la matriz
                if 0 <= fila_adicional < tamaño_tablero and 0 <= columna_adicional < tamaño_tablero:
                    if matriz_visual[fila_adicional][columna_adicional] == espacio_sin_abrir:
                        # Si es un 0, destapar las celdas adyacentes recursivamente
                        if matriz_pygame[fila_adicional][columna_adicional] == 0:
                            casillas_adyacentes(fila_adicional, columna_adicional, matriz_pygame, matriz_visual, tamaño_tablero, espacio_sin_abrir)
                        else:
                            matriz_visual[fila_adicional][columna_adicional] = str(matriz_pygame[fila_adicional][columna_adicional])
        
        else:
            matriz_visual[fila_escogida][columna_escogida] = str(matriz_pygame[fila_escogida][columna_escogida])

        return matriz_visual

    def destapar_celda(fila_escogida, columna_escogida, accion):
        global minas_correctamente_señaladas
        global lista_minas_señaladas
        global ganar
        lista_minas_señaladas = []
        
        if accion: 
            matriz_pygame_visual[fila_escogida][columna_escogida] = "\U0001F6A9"  # Bandera
            if matriz_pygame[fila_escogida][columna_escogida] == "*":
                minas_correctamente_señaladas += 1
                lista_minas_señaladas.append((fila_escogida, columna_escogida))
                
                # Verificar la condición de victoria
                if minas_correctamente_señaladas == minas:  # Asegúrate de que 'minas' tenga el valor correcto
                    ganar = True
                    return False
        else:
            matriz_visual = casillas_adyacentes(fila_escogida, columna_escogida, matriz_pygame, matriz_pygame_visual, tamaño_tablero, ".")
            matriz_pygame_visual[fila_escogida][columna_escogida] = str(matriz_pygame[fila_escogida][columna_escogida])
            if matriz_pygame[fila_escogida][columna_escogida] == "*":
                matriz_pygame_visual[fila_escogida][columna_escogida] = "\U0001F4A3"  # Mina
                return True
            
        return False  # El juego continúa
    def dibujar_tablero(pantalla, centro):
        global posiciones_celdas, tamaño_tablero
        posiciones_celdas = []
        
        for fila in range(tamaño_tablero):
            for columna in range(tamaño_tablero):
                # Definir el rectángulo de cada celda
                rect = pygame.Rect(
                    (margen + ancho_celda) * columna + margen + centro[0],
                    (margen + alto_celda) * fila + margen + 15,
                    ancho_celda,
                    alto_celda
                )
                # Guardar las posiciones de las celdas en una lista global
                posiciones_celdas.append([rect, fila, columna])
                pygame.draw.rect(pantalla, colores["BRONCE"], rect)
                
                # Renderizar el texto dentro de la celda
                valor = matriz_pygame_visual[fila][columna]  # Cambiar aquí para usar matriz_pygame_visual
                texto = font.render(str(valor), True, colores["NEGRO"])  # Asegúrate de convertir a string
                
                # Centrar el texto en la celda
                pantalla.blit(
                    texto,
                    [
                        rect.x + ancho_celda // 3,
                        rect.y + alto_celda // 4,
                    ]
                )

    # Configuración de dificultad según el modo de juego y se definen varias variables con respecto a esta
    def dificultad(modo_juego: str):
        global tamaño_tablero, ancho_celda, alto_celda, minas
        global minas
        if modo_juego.lower() == "f":
            tamaño_tablero = 7
            ancho_celda = 30
            alto_celda = 30
            minas = 5
        elif modo_juego.lower() == "m":
            tamaño_tablero = 10
            ancho_celda = 30
            alto_celda = 30
            minas = 10
        elif modo_juego.lower() == "d":
            tamaño_tablero = 15
            ancho_celda = 30
            alto_celda = 30
            minas = 20
        return minas

    def colocar_minas(tamaño_tablero):
        global matriz_pygame
        numero_minas = 0

        while numero_minas < minas:
            fila_mina = random.randint(0, tamaño_tablero - 1) 
            columna_mina = random.randint(0, tamaño_tablero - 1)

            # Asegurarse de que no se coloque una mina en una posición ya ocupada
            if matriz_pygame[fila_mina][columna_mina] == "*":
                continue  # Saltar a la siguiente iteración si ya hay una mina aquí
            
            # Colocar la mina
            matriz_pygame[fila_mina][columna_mina] = "*" 
            
            # Actualizar las celdas adyacentes
            for i in range(fila_mina - 1, fila_mina + 2):
                for j in range(columna_mina - 1, columna_mina + 2):
                    if 0 <= i < tamaño_tablero and 0 <= j < tamaño_tablero:
                        if matriz_pygame[i][j] != "*":
                            matriz_pygame[i][j] += 1
            numero_minas += 1


    # Transcurso del juego principal
    def transcurso_juego(pantalla):
        global tamaño_tablero, tamaño, matriz_real, matriz_pygame_visual, cronometro
        font_grande = pygame.font.Font(None, 74)
        tamaño = (900, 600)
        background = pygame.image.load("fondo1.jpg").convert()
        background = pygame.transform.scale(background, tamaño)
        done = False #Se definen booleanos para el manejo de eventos
        mostrar_boton = True
        mostrar_botones_opciones = False
        mostrar_botones_modo_juego = False
        mostrar_tablero = False
        mostrar_titulo = True
        accion = False
        continuar_juego = True
        matriz_pygame_visual = generar_matriz()

        #Ciclo principal
        while not done:
            global tiempo_inicial
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    sys.exit()

                # Detectar clics del mouse
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    x, y = mouse_pos
                    
                    if mostrar_tablero:#Detectar los clics del juego en el tablero
                        for celda in posiciones_celdas:
                            rect, fila, columna = celda
                            if rect.collidepoint(mouse_pos):
                                print(f"Usted presionó el botón en fila {fila}, columna {columna}")
                                terminar = destapar_celda(fila, columna, accion)
                                pygame.display.flip()
                                if terminar == True:
                                    mostrar_tablero = False 
                                    continuar_juego = False

                    # Verificar si el clic ocurrió dentro del área del primer botón
                    if 380 <= x <= 530 and 270 <= y <= 370 and mostrar_boton:
                        mostrar_boton = False
                        mostrar_botones_opciones = True

                    # Manejar clic en los botones adicionales
                    if mostrar_botones_opciones:
                        global cronometro
                        if 105 <= x <= 305 and 270 <= y <= 370:
                            mostrar_botones_modo_juego = True
                            mostrar_botones_opciones = False
                            tiempo_inicial = pygame.time.get_ticks()
                            cronometro = True
                        elif 605 <= x <= 755 and 270 <= y <= 370:
                            mostrar_botones_modo_juego = True
                            mostrar_botones_opciones = False

                    # Manejar los botones del modo de juego
                    if mostrar_botones_modo_juego:
                        global limite_tiempo
                        #Dependiendo del modo de dificultad se definen varias cosas y con los valores booleanos se le da una logica para que el juego continue 
                        if 50 <= x <= 150 and 270 <= y <= 370:
                            mostrar_tablero = True
                            modo_dificultad = "f"
                            dificultad(modo_dificultad)
                            mostrar_botones_modo_juego = False
                            mostrar_titulo = False
                            limite_tiempo = 9
                            matriz_real_f(tamaño_tablero)
                            colocar_minas(tamaño_tablero) 
                        elif 300 <= x <= 450 and 270 <= y <= 370:
                            mostrar_tablero = True
                            modo_dificultad = "m"
                            dificultad(modo_dificultad)
                            mostrar_botones_modo_juego = False
                            mostrar_titulo = False
                            limite_tiempo = 180
                            matriz_real_f(tamaño_tablero)
                            colocar_minas(tamaño_tablero) 
                        elif 650 <= x <= 800 and 270 <= y <= 370:
                            mostrar_tablero = True
                            modo_dificultad = "d"
                            dificultad(modo_dificultad)
                            mostrar_botones_modo_juego = False
                            mostrar_titulo = False
                            limite_tiempo = 250
                            matriz_real_f(tamaño_tablero)
                            colocar_minas(tamaño_tablero) 
                    if mostrar_tablero == True:
                        if 30 <= x <= 180 and 100 <= y <= 200:
                            accion = True
                        elif 30 <= x <= 180 and 300 <= y <= 400:
                            accion = False                   

            ## Dibujar la interfaz ##
            pantalla.blit(background, [0, 0])
            
            if mostrar_titulo:
                titulo = font_grande.render("BUSCAMINAS", True, colores["BLANCO"])
                text_rect = titulo.get_rect(center=(450, 100))
                pantalla.blit(titulo, text_rect)
            

            if mostrar_boton:
                # DIBUJAR BOTON JUGAR
                pygame.draw.rect(pantalla, colores["BRONCE"], (390, 280, 130, 80))
                boton_inicio_texto = button_font.render("JUGAR", True, colores["BLANCO"])
                pantalla.blit(boton_inicio_texto, (405, 305))

            if mostrar_botones_opciones:
                # DIBUJAR BOTONES MODO JUEGO
                pygame.draw.rect(pantalla, colores["BRONCE"], (100, 275, 250, 90))
                boton_contrarreloj_texto = button_font.render("CONTRARRELOJ", True, colores["BLANCO"])
                pantalla.blit(boton_contrarreloj_texto, (105, 305))

                pygame.draw.rect(pantalla, colores["BRONCE"], (600, 275, 150, 90))
                boton_normal_texto = button_font.render("NORMAL", True, colores["BLANCO"])
                pantalla.blit(boton_normal_texto, (605, 305))

            if mostrar_botones_modo_juego:
                # DIBUJAR BOTONES DIFICULTAD
                pygame.draw.rect(pantalla, colores["BRONCE"], (50, 275, 100, 90))
                boton_facil_texto = button_font.render("FACIL", True, colores["BLANCO"])
                pantalla.blit(boton_facil_texto, (50, 305))

                pygame.draw.rect(pantalla, colores["BRONCE"], (300, 275, 150, 90))
                boton_medio_texto = button_font.render("MEDIO", True, colores["BLANCO"])
                pantalla.blit(boton_medio_texto, (300, 305))

                pygame.draw.rect(pantalla, colores["BRONCE"], (650, 275, 150, 90))
                boton_dificil_texto = button_font.render("DIFICIL", True, colores["BLANCO"])
                pantalla.blit(boton_dificil_texto, (650, 305))
            if cronometro == True and mostrar_tablero== True:
                global final_tiempo
                tiempo_actual = pygame.time.get_ticks()
                tiempo_transcurrido = (tiempo_actual - tiempo_inicial) // 1000  # Convertir a segundos
                # Convertir el tiempo a minutos y segundos
                minutos = tiempo_transcurrido // 60
                segundos = tiempo_transcurrido % 60
                cronometro_texto = f"{minutos:02}:{segundos:02}"
                texto_renderizado = font.render(cronometro_texto, True, (255, 255, 255))
                pantalla.blit(texto_renderizado, (20, 20))  # Dibujar en la esquina superior izquierda
                if tiempo_transcurrido > limite_tiempo:
                    final_tiempo = True
            
            if final_tiempo == True:#Si se termina el tiempo, el juego se acaba
                mostrar_tablero = False
                final = title_font.render("SE TE ACABO EL TIEMPO", True, colores["BLANCO"])
                pantalla.blit(final, (150, 250))


            if mostrar_tablero:#Se muestra el tablero 
                centro = [tamaño[0] / 2 - (tamaño_tablero * (ancho_celda + margen)) / 2, 130]
                dibujar_tablero(pantalla, centro)

            if mostrar_tablero:#Si se muestra el tablero que se muestren los botones de bandera y destapar
                pygame.draw.rect(pantalla, colores["BRONCE"], (30, 100, 150, 100))
                boton_bandera = button_font.render("Bandera", True, colores["BLANCO"])
                pantalla.blit(boton_bandera, (40, 110))
                pygame.draw.rect(pantalla, colores["BRONCE"], (30, 300, 150, 100))
                boton_bandera = button_font.render("Destapar", True, colores["BLANCO"])
                pantalla.blit(boton_bandera, (40, 310))

            if continuar_juego == False: 
                if ganar:  # Solo verifica si ganar es True
                    ganaste = title_font.render("FELICIDADES GANASTE!!!!!!", True, colores["BLANCO"])
                    mostrar_tablero = False
                    pantalla.blit(ganaste, (40, 310))
                else:  # Aquí solo se ejecuta si ganar es False
                    final = title_font.render("PERDISTE", True, colores["BLANCO"])
                    pantalla.blit(final, (350, 250))

            if ganar == True:
                ganaste = title_font.render("FELICIDADES GANASTE!!!!!!", True, colores["BLANCO"])
                mostrar_tablero = False
                pantalla.blit(ganaste, (100,250))
            # Actualizar pantalla en cada iteración del bucle principal
            pygame.display.flip()

        pygame.quit()
    transcurso_juego(pantalla)

if __name__ == "__main__":
    menu_principal()
            