import time
import os
import socket
import sys
from PyQt6.QtCore import QObject, QThread, pyqtSignal, QTimer
from backend.funciones_cliente import (validacion_formato,validar_direccion,
                               riesgo_mortal, usar_item, calcular_puntaje, posicion,
                               serializar_mensaje, separar_mensaje, 
                               encriptar_mensaje, codificar_mensaje, 
                               decodificar_mensaje, desencriptar_mensaje, 
                               separar_mensaje, deserializar_mensaje,
                               pared_left, pared_right, pared_up, pared_down)
import backend.parametros as parametros
from backend.clases import Conejo, EntidadNpc, Bomba

class Backend(QObject): 
    """ ----- BACKEND es el cliente quien se comunica con el Servidor --------"""
    # señales:
    senal_usuario_revisado = pyqtSignal(str)
    senal_actualizar_ranking = pyqtSignal(str)
    senal_abrir_ventana_juego = pyqtSignal()
    senal_enviar_mapa = pyqtSignal()
    senal_enviar_user_nivel = pyqtSignal(str, int)
    senal_enviar_nivel = pyqtSignal(str)
    senal_enviar_nivel_2 = pyqtSignal(str)
    senal_desconexion_server = pyqtSignal()
    senal_enviar_puntaje = pyqtSignal(int)

    def __init__(self, port: int, host: str):
        super().__init__()
        self.thread = None
        self.conectado = False
        self.port = port
        self.host = host
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.usuario = ""
        self.nivel = 1
        self.puntaje = 0
        try: # ----- INTENTAREMOS CONECTARNOS AL SERVIDOR ----
            self.conectar_servidor()
            self.conectado = True
        except ConnectionError:
            print('Conexion terminada 😢')
            print('No se logro establecer conexión con el servidor 😭')
            self.socket_cliente.close()
            self.conectado = False
            exit()

    def conectar_servidor(self):
        self.socket_cliente.connect((self.host, self.port))
        print("Conectado exitosamente al servidor.")
# -------------------------------------------------------------------
    def nuevo_nivel(self, nivel, puntaje):
        """--- Metodo utilizado al terminar un nivel -> Avanzar y guardar partida nueva ---"""
        print(f"LLEGUE A Backend.nuevo_nivel, nivel: {nivel}")
        self.nivel = str(nivel)
        self.puntaje = puntaje
        self.senal_enviar_nivel_2.emit(self.nivel)
        self.guardar_partida(f"{self.usuario},{self.nivel},{self.puntaje}")

    def operacion_salir(self, mensaje):
        """ --- Este metodo se activa desde el frontend a traves de una señal -> (boton salir)"""
        if mensaje == "0":
            print("SALIENDO DEL JUEGO -> Desconectando del servidor!")
            self.salir()

    def operacion_ranking(self, mensaje):
        """ --- Este metodo se inicia siempre al abrir el juego --- """
        if mensaje == "3":
            print("Pidiendo Ranking al servidor!")
            self.pedir_raking()

    def procesar_nombre(self, user: str):
            print("Revisando Usuario")
            self.ingresar_usuario(user)

# -----------------------------------------------------------------------------------
    def ingresar_usuario(self, usuario):
        """ --- Metodo que ingresa un usuario, y lo procesa ---"""
        es_valido = validacion_formato(usuario)
        if es_valido:
            self.enviar_mensaje(self.socket_cliente, "11111111") # Operacion 1
            self.enviar_mensaje(self.socket_cliente, usuario)
            print(f"-----Enviando Usuario: {usuario}------")
            mensaje_del_servidor = self.recibir_bytes(self.socket_cliente)
            mensaje_del_servidor = self.transformar_mensaje(mensaje_del_servidor)
            print(f"---MENSAJE RECIBIDO: {mensaje_del_servidor}")
            if mensaje_del_servidor == "NO VALIDO":
                print("-----Usuario no valido-----")
                self.senal_usuario_revisado.emit("NO VALIDO")

            else:
                # Mandar señal al frontend: Empieza el JUEGO !!!
                print(f"---Usuario valido, empezando la partida: {mensaje_del_servidor}---")
                elementos = mensaje_del_servidor.split(",")
                
                """----- ¡AQUI SETEAREMOS LOS DATOS DE LA PARTIDA! ------"""
                self.usuario, self.nivel, self.puntaje = elementos[0], elementos[1], elementos[2]
                
                self.senal_usuario_revisado.emit(mensaje_del_servidor)
                self.senal_abrir_ventana_juego.emit()
                self.senal_enviar_user_nivel.emit(self.usuario, int(self.nivel))
                self.senal_enviar_nivel.emit(self.nivel)
                self.senal_enviar_puntaje.emit(int(self.puntaje))
        
        else:
            print("Nombre en formato no Valido: 3 < Largo < 16 / Con Mayusculas y Numeros")
            self.senal_usuario_revisado.emit("FORMATO NO VALIDO")

    def guardar_partida(self, partida: str):
        """---Metodo Sobreescribe en el servidor la partida con nuevo nivel y puntaje"""
        self.enviar_mensaje(self.socket_cliente, "22222222") # Operacion 2
        self.enviar_mensaje(self.socket_cliente, partida)
        print(f"-----Enviando Partida: {partida}-----")

    def pedir_raking(self):
        # PEDIMOS EL RANKING AL SERVIDOR
        self.enviar_mensaje(self.socket_cliente, "33333333")
        self.enviar_mensaje(self.socket_cliente, "OBVIAR ESTE MENSAJE")
        print("-----Pidiendo Ranking-----")
        lista_ranking = self.recibir_bytes(self.socket_cliente)
        ranking = self.transformar_mensaje(lista_ranking)
        self.senal_actualizar_ranking.emit(ranking)
        return ranking

    def salir(self):
            # Cerrar Socket Correctamente
            self.enviar_mensaje(self.socket_cliente, "00000000")
            self.enviar_mensaje(self.socket_cliente, "OBVIAR MENSAJE")
            self.socket_cliente.close()
            self.conectado = False
            print("Desconexion, se ha cerrado sesión")
    # ---------------------------------------------------------------------
    """ A CONTINUACION : Funciones para el envio y recibo de mensajes """
    def enviar_mensaje(self, socket_cliente, mensaje: str): # Recordar Mandar de la nueva forma ! -> Mandar recorriendo mensaje codificado [list[bytearray]]
        mensaje = serializar_mensaje(mensaje)
        mensaje = encriptar_mensaje(mensaje)
        mensaje = codificar_mensaje(mensaje)
        try:
            for elem in mensaje:
                socket_cliente.sendall(elem)
        except ConnectionError:
            print("No se pudo mandar el mensaje")

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

    def transformar_mensaje(self, mensaje) -> str:
        mensaje = decodificar_mensaje(mensaje)
        mensaje = desencriptar_mensaje(mensaje)
        mensaje = deserializar_mensaje(mensaje)
        return mensaje

# -----------------------------------------------------------------------------------------
"""----- A CONTINUACION: La logica del juego, controla la simulacion del juego, 
    el movimiento de las entidades, colisiones, etc.... --------"""

class LogicaJuego(QObject):
    # Señales:
    senal_enviar_entidad = pyqtSignal(str, tuple, int)
    senal_detener_juego = pyqtSignal()
    senal_actualizar_tiempo_vidas_puntajes = pyqtSignal(int, int, int)
    senal_cambiar_spirte = pyqtSignal(int, int, str)
    senal_cambiar_spirte_conejo = pyqtSignal(int, int, str)
    senal_mover_icono = pyqtSignal(int, tuple) # Id , (x,y)
    senal_conectar_tecla_conejo = pyqtSignal(str)
    senal_victoria = pyqtSignal(int)
    senal_pasarse_el_juego = pyqtSignal()
    senal_perdiste = pyqtSignal()
    senal_backend_avanzar_nivel = pyqtSignal(int)
    avisar_backend_avanzar_nivel = pyqtSignal(int, int)
    senal_quitar_bomba = pyqtSignal(int)
    senal_matar_todos = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.entidades = {} # Npc en el mapa + el conejo
        self.bombas = {} # 
        self.items = {} # recolectados por el jugador
        self.reloj_juego = QTimer(self)
        self.reloj_juego.setInterval(1000)
        self.reloj_juego.timeout.connect(self.actualizar_tiempo)
        self.nivel = None
        self.vidas = 3
        self.puntaje = 0
        self.puntaje_partida = 0
        self.inicio = False
        self.x_conejo = 0
        self.y_conejo = 0
        self.id_bombas = 999
        self.vida_infinita = False

    def reset_entidades(self):
        self.entidades = {}

    def setear_puntaje(self, puntaje:int):
        self.puntaje = puntaje

    def tecla_a_conejo(self, tecla:str):
        self.tecla = tecla
        self.conejo.empezar_movimiento(tecla)
    
    def start(self):
        self.tiempo = 121
        self.reloj_juego.start()

    def actualizar_tiempo(self): 
        # --- Se actualiza el tiempo en frontend cada 1 segundo ---
        if self.vida_infinita == True:
            self.senal_actualizar_tiempo_vidas_puntajes.emit(self.tiempo, self.vidas, self.puntaje)
            pass
        else:
            self.tiempo -= 1
            self.senal_actualizar_tiempo_vidas_puntajes.emit(self.tiempo, self.vidas, self.puntaje)
            if self.tiempo == 0:
                self.reloj_juego.stop()
                self.vidas -= 1
                if self.vidas == 0:
                    self.conejo.volver_a_entrada(self.entrada[0], self.entrada[1])
                    self.senal_perdiste.emit()
                    self.senal_detener_juego.emit()
                else:
                    self.conejo.volver_a_entrada(self.entrada[0], self.entrada[1])
                    self.senal_perdiste.emit()
                    self.start()

    def detener_tiempo(self):
        # PARAR EL TIMER DEL RELOJ DEL JUEGO
        self.reloj_juego.stop()
        self.tiempo = 121

    def abrir_mapa(self, nivel):
        """ METODO IMPORTANTE: Abrir el mapa y llamar a funcion que coloca entidades (y añade al Diccionario)"""
        self.nivel = nivel
        with open( os.path.join('frontend', 'assets', 'laberintos', f'tablero_{nivel}.txt') , "r") as archivo:
            mapa = archivo.readlines()
        laberinto = []
        for i in mapa:
            laberinto.append(i.strip(",\n").split(","))
        self.mapa = laberinto
        self.colocar_entidad()

    def colocar_entidad(self):
        fila = len(self.mapa)
        columna = len(self.mapa[0])
        for fil in range(fila):
            for col in range(columna):
                # ----------------------------
                if self.mapa[fil][col] == "E":
                    self.entrada = (col, fil)
                # ----------------------------
                if self.mapa[fil][col] == "S":
                    self.salida = (col, fil)
                # ---------------------------------
                if self.mapa[fil][col] == "C":
                    nombre = self.mapa[fil][col]
                    conejo = Conejo(nombre, self.mapa, col, fil, self.senal_mover_icono, self.senal_cambiar_spirte_conejo)
                    self.senal_enviar_entidad.emit(nombre, (col, fil), conejo.id)
                    self.conejo = conejo
                    self.entidades[0] = self.conejo
                # --------------------------------------
                if self.mapa[fil][col] in ["BM", "BC"]:
                    self.id_bombas += 1
                    nombre = self.mapa[fil][col]
                    self.senal_enviar_entidad.emit(nombre, (col, fil), self.id_bombas)
                    entidad = Bomba(self.id_bombas, nombre, self.mapa, col, fil)
                    self.bombas[self.id_bombas] = entidad
                    # CREAR TIMER QUE COMPRUEBE SI EL CONEJO ESTA ENCIMA DE LA BOMBA
                # ---------------------------------------------
                if self.mapa[fil][col] not in ["P", "-", "E", "S", "C", "BM", "BC"]:
                    nombre = self.mapa[fil][col]
                    entidad = EntidadNpc(nombre, self.mapa, col, fil , self.senal_mover_icono, self.senal_cambiar_spirte)
                    self.entidades[entidad.id] = entidad
                    self.senal_enviar_entidad.emit(nombre, (col, fil), entidad.id)
        
        self.keys = self.entidades.keys()            
        for key in self.keys:
            if self.entidades[key].nombre == "C":
                pass
            else: # ------- EMPEZAR LOS MOVIMIENTOS (NPC) --------
                self.entidades[key].start_timer()
        """ --- QTimer: Comprueba siempre que el conejo haya colisionado con una entidad ---"""
        self.timer_muerte = QTimer(self)
        self.timer_muerte.timeout.connect(self.comprobar_muerte)
        self.timer_muerte.setInterval(self.conejo.velocidad)
        self.timer_muerte.start()
        """ --- QTimer: Comprueba siempre que el conejo haya llegado a la salida ---"""
        self.timer_triunfo = QTimer(self)
        self.timer_triunfo.timeout.connect(self.comprobar_triunfo)
        self.timer_triunfo.setInterval(self.conejo.velocidad)
        self.timer_triunfo.start()

    def comprobar_muerte(self):
        """ --- Iniciada con QTimer ---"""
        keys = self.entidades.keys()
        for key in keys:
            if ( round(self.conejo.x) == round(self.entidades[key].x) and 
            round(self.conejo.y) == round(self.entidades[key].y) ) and (
                self.entidades[key].nombre != "C"):
                print("TOQUE UNA ENTIDAD -> DEBERIA MORIR")
                if self.vida_infinita == True:
                    self.conejo.volver_a_entrada(self.entrada[0], self.entrada[1])
                    self.senal_perdiste.emit()
                    self.start()
                else:
                    self.vidas -= 1
                    if self.vidas == 0:
                        self.senal_perdiste.emit()
                        self.senal_detener_juego.emit()
                        break
                    else:
                        self.conejo.volver_a_entrada(self.entrada[0], self.entrada[1])
                        self.senal_perdiste.emit()
                        self.start()

    def comprobar_triunfo(self):
        """ --- Iniciada con QTimer ---"""
        if ( round(self.conejo.x) == round(self.salida[0]) 
            and round(self.conejo.y) == round(self.salida[1]) ):
            self.timer_triunfo.stop()
            if int(self.nivel) == 3:
                self.reloj_juego.stop()
                self.senal_victoria.emit(int(4))
                self.senal_pasarse_el_juego.emit()
                self.senal_detener_juego.emit()
                self.nivel = 1
                self.avisar_backend_avanzar_nivel.emit(int(self.nivel), self.puntaje)
            else:
                self.reloj_juego.stop()
                keys = self.entidades.keys()
                for key in keys:
                    if self.entidades[key].nombre == "C":
                        self.entidades[key].detener_movimineto()
                    else:
                        self.entidades[key].stop_timer()
                self.entidades = {}
                self.nivel = int(self.nivel) + 1
                self.nivel = str(self.nivel)
                self.senal_victoria.emit(int(self.nivel))
                self.senal_backend_avanzar_nivel.emit(int(self.nivel))
                self.avanzar_nivel()

    def avanzar_nivel(self):
        self.avisar_backend_avanzar_nivel.emit(int(self.nivel), self.puntaje)
        self.abrir_mapa(self.nivel)
        self.start()
        
    def pausa(self): # Activada con PyqtSignal:
        llaves = self.entidades.keys()
        for key in llaves:
            if self.entidades[key].timer_movimiento.isActive():
                self.entidades[key].timer_movimiento.stop()
                self.conejo.timer_movimiento.stop()
                self.reloj_juego.stop()
                self.conejo.pausa = True
                self.pausa = True
            else:
                self.entidades[key].timer_movimiento.start()
                self.conejo.timer_movimiento.start()
                self.reloj_juego.start()
                self.conejo.pausa = False
                self.pausa = False

    def cheatcode(self, code: str):
        if code == "kil":
            self.timer_muerte.stop()
            keys = self.entidades.keys()
            for key in keys:
                if self.entidades[key].nombre == "C":
                    self.entidades[key].detener_movimineto()
                    aux = self.entidades[key]
                else:
                    self.entidades[key].stop_timer()
            self.entidades = {}
            self.entidades[0] = aux
            self.senal_matar_todos.emit()
        elif code == "inf":
            print("CHEATCODE: INF LLEGO AL BACKEND !!!! ----")
            #self.reloj_juego.stop()
            self.vida_infinita = True
            self.puntaje += parametros.PUNTAJE_INF