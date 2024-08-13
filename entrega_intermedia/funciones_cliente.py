from funciones_extras import posicion

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

