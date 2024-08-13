def posicion(elem: str, tablero: list[list]) -> tuple:
    filas = len(tablero)
    columnas = len(tablero[0])
    for f in range(filas):
        for c in range(columnas):
            if tablero[f][c] == elem:
                return (f,c)
            
#def verifica_esquina(elem, tablero):
#    filas = len(tablero)
#    columnas = len(tablero[0])
#    pos = posicion(elem)
#    if pos == (0,0):