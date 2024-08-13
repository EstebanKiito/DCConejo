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
    
def deserializar_mensaje(mensaje: bytearray) -> str:
    return mensaje.decode("utf-8", "big")


if __name__ == '__main__':
    mensaje = "Esteban9823,2,1000;EstebanPro69,1,0;OjedaCarlos13,1,0;ElOtakuQl1,1,0;LanDrake666,1,0"
    print(mensaje)
    mensaje = serializar_mensaje(mensaje)
    print(mensaje)
    #mensaje = separar_mensaje(mensaje)
    #print(mensaje)
    mensaje = encriptar_mensaje(mensaje)
    print(mensaje)
    mensaje = codificar_mensaje(mensaje)
    print(mensaje)

    mensaje = decodificar_mensaje(mensaje)
    print(mensaje)

    mensaje = desencriptar_mensaje(mensaje)
    print(mensaje)

    mensaje = deserializar_mensaje(mensaje)
    print(mensaje)