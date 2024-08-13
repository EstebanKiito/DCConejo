import sys
import socket
import threading
import json

class Servidor:

    def __init__(self, port: int, host: str):
        self.host = host
        self.port = port
        self.dict_sockets = {}
        self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.usuarios_invalidos = ['Estarducs777','EstebanpRo177','DonCarlos69']
        self.puntajes = [] # Actualizar: Rellenar cada vez que se guarde usuario en TXT
        self.usuarios = [] # Actualizar: al añadir usuario nuevo
        self.ranking = {}
        # Empezar Ciclo !!!
        self.iniciar_puntajes_usuarios()
        self.bind_listen()
        self.aceptar_conexiones()

    def iniciar_puntajes_usuarios(self):
        self.puntajes, self.usuarios = self.abrir_txt()

    def bind_listen(self): 
        # Empezaremos a recibir y escuchar clientes
        self.socket_servidor.bind( (self.host, self.port) )
        self.socket_servidor.listen( 10 ) # Revisar Enunciado -> Cuantos jugadores maximo
        print(f'Servidor escuchando en {self.host} : {self.port}')

    def aceptar_conexiones(self):
        # Este hilo esta encargado de aceptar las conexiones
        thread = threading.Thread( target=self.aceptar_conexiones_thread )
        thread.start()

    def aceptar_conexiones_thread(self):
        while True:
            # Siempre escucha posibles threads, guardaremos la direccion y crearemos
            # un nuevo hilo donde solo se escuche a ese cliente en especifico
            socket_cliente, adress = self.socket_servidor.accept() 
            self.dict_sockets[socket_cliente] = adress # Añadimos su direccion
            thread_escuchar_cliente = threading.Thread( target=self.thread_escuchar_cliente,
                                                        args= (socket_cliente,),
                                                        daemon=True)
            thread_escuchar_cliente.start()
            
    def thread_escuchar_cliente(self, socket_cliente: socket):
        try:
            i = 1
            while True:
                if i == 1:
                    print(f">>> {self.dict_sockets[socket_cliente]} Se ha Conectado!") # Solo imprimir 1 vez
                    i += 1
                print("--- Esperando Operacion ---")
                operacion = self.recibir_bytes(socket_cliente)
                operacion = int( self.transformar_mensaje(operacion)[0] ) # Posible Error: -> No recibir un string numerico (111) (222) (333)
                print(f"Se ha pedido operación: {operacion}")

                mensaje = self.recibir_bytes(socket_cliente)
                print("Se ha recibido el mensaje, hora de decodificarlo!")

                if operacion == 0:
                    # Desconexión!
                    print(f"{self.dict_sockets[socket_cliente]} Se ha desconectado!")
                    socket_cliente.close()  # -> REVISAR
                    del self.dict_sockets[socket_cliente]
                    #self.salir()
                    break
                try:
                    print( "Hora de Decodificar!" )
                    mensaje_procesado = self.transformar_mensaje(mensaje)
                    self.operar_mensaje(socket_cliente, operacion, mensaje_procesado)

                except ConnectionError as error:
                    print(f"{self.dict_sockets[socket_cliente]} Se ha desconectado!")
                    socket_cliente.close()  # -> REVISAR 
                    del self.dict_sockets[socket_cliente]
                    break
#
        except ValueError as error:
            print("Error de conexion con Cliente - Posible Desconexion")
#    def salir(self):
#        cerrar = input("""
#¿Quieres Cerrar Servidor?: 
#[0] Si 
#[1] No 
#""")
#        if cerrar == "0":
#            self.socket_servidor.close()
#        else:
#            pass

    def recibir_bytes(self, socket_cliente: socket) -> list[bytearray]:
        bytes_largo = socket_cliente.recv(4) # Largo
        largo = int.from_bytes( bytes_largo, "big" )
        lista = []
        lista.append(bytes_largo)
        bytes_leidos = 0
        contador = 1
        while bytes_leidos < largo:
            if contador % 2 == 0:   # Leyendo 36 chunks de mensajes
                mensaje_chunck = socket_cliente.recv(36)
                lista.append(mensaje_chunck)
                bytes_leidos += len(mensaje_chunck)
                contador += 1
            else:                   # Leyendo Bloque Mensaje
                mensaje_bloque = socket_cliente.recv(4)
                lista.append(mensaje_bloque)
                bytes_leidos += len(mensaje_bloque)
                contador += 1
        return lista
    

    def operar_mensaje(self, socket_cliente, operacion, mensaje):
        if operacion == 1: # Operacion: Validar Usuario -> INGRESAR USUARIO POR INPUT
            usuario = mensaje
            es_valido = self.validar_usuario(usuario)
            if not es_valido:
                self.enviar_mensaje(socket_cliente, "NO VALIDO") 
                print("---Usuario No Valido---")
            else:
                # Revisar Usuarios:
                self.iniciar_puntajes_usuarios()
                if usuario in self.usuarios:             
                    # YA EXISTE: Devolver partida: puntaje y nivel actual!
                    user_level = self.encontrar(usuario)
                    self.enviar_mensaje(socket_cliente, user_level)
                    print("---Partida Encontrada!---")
                
                else:                          
                    #  GUARDAR NUEVO USUARIO!
                    self.escribir_nuevo_en_txt(f"{usuario},1,0")
                    self.enviar_mensaje(socket_cliente, f"{usuario},1,0")
                    print("---Partida Nueva Guardada Exitosamente!---")

        if operacion == 2: # Pase de Nivel -> Guardar partida (jugador,nivel,puntajes)
            # SOBREESCRIBIR Y GUARDAR EN EL TXT            
            partida_nueva = mensaje
            self.sobrescribir_puntaje_en_txt(partida_nueva)
            print("---Jugador paso de nivel!---")
            # self.enviar_mensaje(f"Felicidades, jugador paso de nivel")
        
        if operacion == 3: # Pedir Ranking de los mejores 5 Jugadores
            print("---SACANDO RANKING---")
            # IGNORAR MENSAJE
            ranking = self.top_5()
            print(type(ranking))
            self.enviar_mensaje(socket_cliente, ranking)
            print("---He enviado el Ranking!---")

        # if operacion == 4: 
        # TERMINO JUEGO, Reiniciar nivel, No PUNTAJES! OPERACION DE BACKEND!
        #  -> el mandara nuevo puntaje y nivel

    def encontrar(self, usuario: str) -> str:
        for i in self.puntajes:
            if i[0] == usuario:
                user_level = ",".join(i)
                return user_level

    def abrir_txt(self) -> list:
        with open( "puntajes.txt" , "r") as archivo:
            puntajes_crudo = archivo.readlines()
        puntajes = []
        usuarios = []
        for i in puntajes_crudo:
            data = i.strip().split(",")
            puntajes.append(data)
            usuarios.append(data[0])
        return (puntajes,usuarios)
    
    def escribir_nuevo_en_txt(self, mensaje: str):
        mensaje = mensaje.split(",")
        self.puntajes.append(mensaje)
        mensaje_str = ""
        for i in self.puntajes:
            mensaje_str += ",".join(i)
            mensaje_str += "\n"
        with open( "puntajes.txt", "w" ) as archivo:
            archivo.write(mensaje_str)

    def sobrescribir_puntaje_en_txt(self, mensaje: str):
        partida_nueva = mensaje.split(",") # En forma de lista, para preguntar por el nombre [0]
        for i in range(len(self.puntajes)):
            if self.puntajes[i][0] == partida_nueva[0]:
                self.puntajes[i] = partida_nueva # Reemplazar puntaje
        # Escribir nueva lista de puntajes en el TXT
        mensaje_str = ""
        for i in self.puntajes:
            mensaje_str += ",".join(i)
            mensaje_str += "\n"
        with open( "puntajes.txt", "w" ) as archivo:
            archivo.write(mensaje_str)

    def top_5(self) -> str:
        # self.puntajes
        # Busquemos en el archivo los puntajes mas altos, devolviendo sus nombres
        # Con los nombres llamamos 5 veces a encontrar y los guardamos en una lista
        # Finalmente le hacemos ",".join() -> str y retornamos
        # Pensar en como vamos a separar en el backend cada puntaje para actualizar sus labels
        self.iniciar_puntajes_usuarios()
        ranking = []
        lista_ordenada = self.puntajes.copy()
        lista_ordenada.sort(key=lambda x: int(x[2]), reverse=True)
        ranking = lista_ordenada[:5] # Saco los 5 mejores
        # Ranking es una lista de listas, hay que ir desempaquetandola:
        mensaje = []
        for elem in ranking:
            mensaje.append( ",".join(map(str, elem)) )
        mensaje =  ";".join(mensaje)
        print(mensaje)
        return mensaje
    
# ---------------------------------------------------------------------------------------

# TRANSFORMAR MENSAJE:
    def transformar_mensaje(self, mensaje) -> str:
        mensaje = self.decodificar_mensaje(mensaje)
        mensaje = self.desencriptar_mensaje(mensaje)
        mensaje = self.deserializar_mensaje(mensaje)
        return mensaje

    def decodificar_mensaje( self, lista_codificada: list[bytearray] ):
        largo_lista = len(lista_codificada)
        largo = int.from_bytes(lista_codificada[0], "big")
        mensaje = bytearray()
        # Recorramos de 2 en 2 la lista, sacando solo el mensaje
        for i in range(2, largo_lista, 2 ):
            mensaje += lista_codificada[i] 
        # Quitamos los 0 añadidos de relleno    
        mensaje = mensaje[:largo]
        return mensaje

    def juntar_mensaje(self, lista: list[bytearray], largo):
        if largo == 2: # Revisar este caso y el de 1
            pass
        if largo == 1:
            pass
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

    def desencriptar_mensaje( self, mensaje: bytearray ):
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
            mensaje_original = self.juntar_mensaje( [ A, B, C ], largo)
            return mensaje_original
        if n == 1: # Suma Impar: A C B
            A = mensaje[0:len_a]
            C = mensaje[len_a:len_a+len_c]
            B = mensaje[len_a + len_c: len_a + len_c + len_b ]
            mensaje_original = self.juntar_mensaje( [ A, B, C ], largo)
            return mensaje_original

    def deserializar_mensaje(self, mensaje: bytearray) -> str:
        return mensaje.decode("utf-8", "big")

# --------------------------------------------------------------------------------------------------

    def validar_usuario(self, usuario: str) -> bool: # Buscar en la Lista Baneados y devolver una respuesta
        if usuario in self.usuarios_invalidos:
            return False
        return True

# ---------------------------------------------------------------------------------------------------
# ENVIO DE MENSAJES

    def serializar_mensaje(self, mensaje: str) -> bytearray:
        return bytearray( mensaje.encode("utf-8", "big") )

    def separar_mensaje(self, mensaje: bytearray) -> list[bytearray]:
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

    def encriptar_mensaje(self, mensaje: bytearray) -> bytearray:
        lista_encriptada = self.separar_mensaje(mensaje)
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

    def codificar_mensaje(self, mensaje: bytearray) -> list[bytearray]:
        TAMANO_CHUNK = 36
        largo = len(mensaje)
        largo_bytes = largo.to_bytes(4, byteorder="big")
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

        lista_codificada = [largo_bytes] + mensaje_separado_chunks
        return lista_codificada

    def enviar_mensaje(self, socket_cliente, mensaje: str): # Recordar Mandar de la nueva forma ! -> Mandar recorriendo mensaje codificado [list[bytearray]]
        mensaje = self.serializar_mensaje(mensaje)
        mensaje = self.encriptar_mensaje(mensaje)
        mensaje = self.codificar_mensaje(mensaje)
        # Ahora tenemos la lista, Enviarla !
        for elem in mensaje:
            #print("ELEMENTO ENVIADO: ", elem)
            socket_cliente.sendall(elem)

if __name__ == '__main__':
    PORT = 8001 if len(sys.argv) < 2 else int(sys.argv[1])
    with open('host_servidor.json', 'r') as archivo:
        host = json.load(archivo)
        HOST = host["host"] if len(sys.argv) < 3 else sys.argv[2]
    servidor = Servidor(PORT, HOST)