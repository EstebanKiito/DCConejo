def usuario_permitido(nombre: str, usuarios_no_permitidos: list[str]) -> bool:
    if nombre in usuarios_no_permitidos:
        return False
    return True


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

    
    #return mensaje_separado_chunks
    
    pass
