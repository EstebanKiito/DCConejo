#from backend.funciones_extras import posicion

def posicion(elem: str, tablero: list[list]) -> tuple:
    filas = len(tablero)
    columnas = len(tablero[0])
    for f in range(filas):
        for c in range(columnas):
            if tablero[f][c] == elem:
                return (f,c)

def validacion_formato(nombre:str) -> bool:
    if not nombre.isalnum():
        return False
    if len(nombre) > 16 or len(nombre) < 3:
        return False
    mayus = False
    num = False
    for letra in nombre:
        if letra.isnumeric():
            num = True
        if letra.isupper():
            mayus = True
    if mayus and num: # Ya aprobo todos los casos
        return True
    return False # No logro la comprobacion final


def riesgo_mortal(laberinto: list[list]) -> bool:
    pos_jugador = posicion("C", laberinto) # -> (fila, columna)
    fila_conejo , columna_conejo = pos_jugador
    aux_fila_conejo , aux_columna_conejo = fila_conejo , columna_conejo
    n_filas = len(laberinto)
    n_columnas = len(laberinto[0])
    
    # Revisar la horizontal
    lista_horizontal = []
    for col in range(n_columnas):
        lista_horizontal.append(laberinto[fila_conejo][col])
    
    if "LH" in lista_horizontal or "CL" in lista_horizontal or "CR" in lista_horizontal:
        while columna_conejo != 0:
            if lista_horizontal[columna_conejo] in ["P", "CL"]:
                break
            if lista_horizontal[columna_conejo] in ["LH", "CR"]:
                return True
            columna_conejo -= 1
        columna_conejo = aux_columna_conejo
        while columna_conejo != (n_columnas):
            if lista_horizontal[columna_conejo] in ["P", "CR"]:
                break
            if lista_horizontal[columna_conejo] in ["LH", "CL"]:
                return True
            columna_conejo += 1
        columna_conejo = aux_columna_conejo

    # Revisar Vertical
    lista_vertical = []
    for fil in range(n_filas):
        lista_vertical.append(laberinto[fil][columna_conejo])

    if "LV" in lista_vertical or "CD" in lista_vertical or "CU" in lista_vertical:
        while fila_conejo != 0:
            if lista_vertical[fila_conejo] in ["P", "CU"]:
                break
            if lista_vertical[fila_conejo] in ["LV", "CD"]:
                return True
            fila_conejo -= 1
        fila_conejo = aux_fila_conejo
        while fila_conejo != (n_filas):
            if lista_vertical[fila_conejo] in ["P", "CD"]:
                break
            if lista_vertical[fila_conejo] in ["LV", "CU"]:
                return True
            fila_conejo += 1
        fila_conejo = aux_fila_conejo

    return False # Nunca retorno True, por lo que es segura: return -> False


def usar_item(item: str, inventario: list) -> tuple[bool, list]:
    if item not in inventario:
        return (False, inventario.copy() )
    else:
        copia = inventario.copy()
        copia.remove(item)
        return (True, copia)


def calcular_puntaje(tiempo: int, vidas: int, cantidad_lobos: int, PUNTAJE_LOBO: int) -> float:
    if cantidad_lobos == 0:
        return round(float(0), 2)
    else:
        puntaje = ( tiempo * vidas ) / (cantidad_lobos * PUNTAJE_LOBO )
        return round(puntaje, 2)


def validar_direccion(laberinto: list[list], tecla: str) -> bool:
    filas_tablero = len(laberinto)
    columnas_tablero = len(laberinto[0])
    conejo = posicion("C", laberinto)
    fila_conejo, columna_conejo = conejo
    
    if tecla == "W": # Arriba
        if laberinto[fila_conejo - 1][columna_conejo] in ["P", "CU", "CD", "CR", "CL"]:
            return False
        return True

    if tecla == "S": # Abajo
        if laberinto[fila_conejo + 1][columna_conejo] in ["P", "CU", "CD", "CR", "CL"]:
            return False
        return True
    
    if tecla == "A": # Izquierda
        if laberinto[fila_conejo][columna_conejo - 1] in ["P", "CU", "CD", "CR", "CL"]:
            return False
        return True
    if tecla == "D": # Derecha
        if laberinto[fila_conejo][columna_conejo + 1] in ["P", "CU", "CD", "CR", "CL"]:
            return False
        return True




# Necesarias para mandar los mensajes: 
def serializar_mensaje(mensaje: str) -> bytearray:
    return bytearray( mensaje.encode("utf-8", "big") )


def separar_mensaje(mensaje: bytearray) -> list[bytearray]:
    orden_1 = True
    orden_2 = False
    contador = 0
    lista_encriptada = [ bytearray(), bytearray() , bytearray() ]
    for byte in mensaje:
        if orden_1 and not orden_2:
            lista_encriptada[contador].append(byte)
            contador += 1
            if contador == 3:
                contador = 2
                orden_1, orden_2 = False, True
                continue
        if not orden_1 and orden_2:
            lista_encriptada[contador].append(byte)
            contador -= 1
            if contador == -1:
                contador = 0
                orden_1, orden_2 = True, False
                continue

    return lista_encriptada


def encriptar_mensaje(mensaje: bytearray) -> bytearray:
    lista_encriptada = separar_mensaje(mensaje)
    suma = int(lista_encriptada[0][0]) + int(lista_encriptada[1][-1]) + int(lista_encriptada[2][0])

    if suma % 2 == 0: 
        n = "1"
        n = n.encode("utf-8")
        encriptado = n + lista_encriptada[0] + lista_encriptada[2] + lista_encriptada[1]
        return bytearray(encriptado)
    else:
        n = "0"
        n = n.encode("utf-8")
        encriptado = n + lista_encriptada[1] + lista_encriptada[0] + lista_encriptada[2]
        return bytearray(encriptado)
    


def codificar_mensaje(mensaje: bytearray) -> list[bytearray]:
    TAMANO_CHUNK = 36
    largo = len(mensaje)
    largo = bytearray(largo.to_bytes(4, "big"))

    mensaje_separado_chunks = []
    bloque = 1
    for i in range(0, len(mensaje), TAMANO_CHUNK):

        mensaje_separado_chunks.append( bytearray( bloque.to_bytes(4,"big")) )
        bloque += 1
        chunk = bytearray( mensaje[i:i+TAMANO_CHUNK] )
        if len(chunk) != TAMANO_CHUNK:
            add = TAMANO_CHUNK - len(chunk)
            for i in range(add):
                chunk.append(0)
        mensaje_separado_chunks.append(chunk)
        
    lista_codificada = [largo] + mensaje_separado_chunks
    return lista_codificada


def decodificar_mensaje( lista_codificada: list[bytearray] ):
    largo_lista = len(lista_codificada)
    largo = int.from_bytes(lista_codificada[0], "big")
    mensaje = bytearray()
    # Recorramos de 2 en 2 la lista, sacando solo el mensaje
    for i in range(2, largo_lista, 2 ):
        mensaje += lista_codificada[i] 
    # Quitamos los 0 añadidos de relleno    
    mensaje = mensaje[:largo]
    return mensaje



def juntar_mensaje(lista: list[bytearray], largo):
    if largo == 2: # Revisar este caso y el de 1
        pass
    if largo == 1:
        pass
    partes = largo // 3 
    sobra = largo % 3
    mensaje_original = bytearray()
    acabo = False
    contador = 0
    bajada = True
    while len(mensaje_original) != largo:
        if bajada == True: # Va bajando
            while contador < 3 and bajada != False and acabo == False:
                mensaje_original.append( lista[contador][0] )
                if len(mensaje_original) == largo: # Comprobar si ya llegamos
                    acabo = True
                    break
                lista[contador] = lista[contador][1:]
                contador += 1
                if contador == 3:
                    contador = 2
                    bajada = False
                    continue
        elif bajada == False: # Va subiendo
            while contador > -1 and bajada == False and acabo == False:
                mensaje_original.append( lista[contador][0] )
                if len(mensaje_original) == largo: # Comprobar si ya llegamos
                    acabo = True
                    break
                lista[contador] = lista[contador][1:]
                contador -= 1
                if contador == -1:
                    contador = 0
                    bajada = True
                    continue
    return mensaje_original 

def desencriptar_mensaje( mensaje: bytearray ):
    n = int(mensaje[0:1])
    mensaje = mensaje[1:]
    largo = len(mensaje)
    partes = largo // 3 
    sobra = largo % 3
    #return (partes, sobra)
    if sobra == 0: # Mejor Caso, todas tienen misma reparticion
        len_a, len_b, len_c = partes, partes, partes
    if sobra == 1: # Significa que al A o al C se le suma el sobrante
        if partes % 2 == 0: # Si partes es Par -> Bajo y Subio segun el algoritmo, el restante es de A
            len_a, len_b, len_c = partes + 1, partes, partes
        else:
            len_a, len_b, len_c = partes, partes, partes + 1
    if sobra == 2: # Significa que al A o al C se le suma un sobrante, y a B Siempre!
        if partes % 2 == 0: # Si partes es Par -> Bajo y Subio segun el algoritmo, el restante es de A
            len_a, len_b, len_c = partes + 1 , partes + 1, partes
        else:
            len_a, len_b, len_c = partes  , partes + 1, partes + 1
    if n == 0: # Suma Par: B A C
        B = mensaje[0:len_b]
        A = mensaje[len_b:len_b+len_a]
        C = mensaje[len_b + len_a: len_b + len_a + len_c ]
        mensaje_original = juntar_mensaje( [ A, B, C ], largo)
        return mensaje_original
    if n == 1: # Suma Impar: A C B
        A = mensaje[0:len_a]
        C = mensaje[len_a:len_a+len_c]
        B = mensaje[len_a + len_c: len_a + len_c + len_b ]
        mensaje_original = juntar_mensaje( [ A, B, C ], largo)
        return mensaje_original
    
def deserializar_mensaje(mensaje: str) -> bytearray:
    return mensaje.decode("utf-8", "big")

# --------------------------------------------------------------
# Funciones Entidades:

def pared_left(mapa, x, y):
    fil = y
    for col in range(x, -1, -1):
        if mapa[fil][col] in ["CU", "CR", "CD", "CL"]:
            pass
        elif mapa[fil][col] in ["P", "CU", "CR", "CD", "CL"]:
            return (col, fil)
        if col == 0:
            return (col-1, fil)

def pared_right(mapa, x, y):
    fil = y
    for col in range(x, len(mapa[0])):
        if mapa[fil][col] in ["CU", "CR", "CD", "CL"]:
            pass
        elif mapa[fil][col] in ["P", "CU", "CR", "CD", "CL"]:
            return (col, fil)
        if col == 15:
            return (col+1, fil)

def pared_up(mapa, x, y):
    col = x
    for fil in range(y, -1, -1):
        if mapa[fil][col] in ["CU", "CR", "CD", "CL"]:
            pass
        elif mapa[fil][col] in ["P", "CU", "CR", "CD", "CL"]:
            return (col, fil)
        if fil == 0:
            return (col, fil-1)

def pared_down(mapa, x, y):
    col = x
    for fil in range(y, len(mapa)):
        if mapa[fil][col] in ["CU", "CR", "CD", "CL"]:
            pass
        elif mapa[fil][col] in ["P", "CU", "CR", "CD", "CL"]:
            return (col, fil)
        if fil == 15:
            return (col, fil+1)












