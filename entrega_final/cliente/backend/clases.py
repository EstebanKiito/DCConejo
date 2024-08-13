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

class Conejo(QObject):
    def __init__(self, nombre: str, mapa, x: float, y: float, senal_mover, senal_cambiar_spirte):
        super().__init__()
        self.id = 0
        self.nombre = nombre
        self.mapa = mapa
        self.x = x
        self.y = y
        self.velocidad = parametros.VELOCIDAD_CONEJO
        self.senal_mover = senal_mover
        self.senal_cambiar_spirte = senal_cambiar_spirte
        self.sprite = 0
        #muerto = False
        #self.direccion = 1
        self.sprite = 0
        self.velocidad = 10
        self.calcular_paredes()
        self.timer_movimiento = QTimer(self)
        self.timer_movimiento.timeout.connect(self.mover)
        self.timer_movimiento.setInterval(self.velocidad)
        self.tecla_direccion = "w" # WASD
        self.pausa = False

        #self.escuchar_movimiento = QTimer(self)

    def volver_a_entrada(self, x: int, y: int):
        self.x = x
        self.y = y
        self.detener_movimineto()
        self.senal_cambiar_spirte.emit(self.id, self.sprite, "BASE")
        self.calcular_paredes()

    def calcular_paredes(self):
        #print(self.x)
        #print(self.y)
        self.pared_izquierda = pared_left(self.mapa, round(self.x), round(self.y) )
        self.pared_derecha = pared_right(self.mapa, round(self.x), round(self.y))
        self.pared_arriba = pared_up(self.mapa, round(self.x), round(self.y))
        self.pared_abajo = pared_down(self.mapa, round(self.x), round(self.y))    


    def empezar_movimiento(self, tecla: str): # Viene de un pyqtSignal 
        # INCIA EL QTIMER Y SETEA : self.tecla_movimiento
        if not self.timer_movimiento.isActive() and self.pausa != True:
            self.tecla_direccion = tecla
            self.timer_movimiento.start() 

    def detener_movimineto(self):
        self.timer_movimiento.stop()

    def mover(self):
        
        """ ES UN QTIMER QUE MUEVE AL CONEJO A LA MAXIMA DIRECCION (self.tecla_direccion) posible """
        
        # ------ ARRIBA ------------
        if self.tecla_direccion == "w":
            #print(f"Pared cercana: {self.pared_arriba}")
            max_arriba = ( self.pared_arriba[0], self.pared_arriba[1] + 1 )
            if self.y <= max_arriba[1]:
                self.detener_movimineto()
                self.senal_cambiar_spirte.emit(self.id, self.sprite, "BASE")
                self.calcular_paredes()
            else:
                self.y -= 1/10
                # ------- CAMBIAR SPRITE -------> ANIMACION
                self.sprite += 1
                if self.sprite == 4:
                    self.sprite = 1
                self.senal_cambiar_spirte.emit(self.id, self.sprite, "ARRIBA")
        
        # ------ ABAJO ------------
        elif self.tecla_direccion == "s":
            #print(f"Pared cercana: {self.pared_abajo}")
            max_abajo  = ( self.pared_abajo[0], self.pared_abajo[1] - 1 )
            if self.y >= max_abajo[1]:
                self.detener_movimineto()
                self.senal_cambiar_spirte.emit(self.id, self.sprite, "BASE")
                self.calcular_paredes()
            else:
                self.y += 1/10
                # ------- CAMBIAR SPRITE -------> ANIMACION
                self.sprite += 1
                if self.sprite == 4:
                    self.sprite = 1
                self.senal_cambiar_spirte.emit(self.id, self.sprite, "ABAJO")

        # ------ IZQUIERDA ------------
        elif self.tecla_direccion == "a": 
            #print(f"Pared cercana: {self.pared_izquierda}")
            max_izquierda = ( self.pared_izquierda[0] + 1, self.pared_izquierda[1] )
            if self.x <= max_izquierda[0]:
                self.detener_movimineto()
                self.senal_cambiar_spirte.emit(self.id, self.sprite, "BASE")
                self.calcular_paredes()
            else:
                self.x -= 1/10
                # ------- CAMBIAR SPRITE -------> ANIMACION
                self.sprite += 1
                if self.sprite == 4:
                    self.sprite = 1
                self.senal_cambiar_spirte.emit(self.id, self.sprite, "IZQ")
        
        # ------ DERECHA ------------
        elif self.tecla_direccion == "d":
            #print(f"Pared cercana: {self.pared_derecha}")
            max_derecha   = ( self.pared_derecha[0] - 1, self.pared_derecha[1] )
            if self.x >= max_derecha[0]: # Revisar cuando este en las paredes
                self.detener_movimineto()
                self.senal_cambiar_spirte.emit(self.id, self.sprite, "BASE")
                self.calcular_paredes()
            else:
                self.x += 1/10
                # ------- CAMBIAR SPRITE -------> ANIMACION
                self.sprite += 1
                if self.sprite == 4:
                    self.sprite = 1
                self.senal_cambiar_spirte.emit(self.id, self.sprite, "DER")
            
        self.senal_mover.emit(self.id, (self.x, self.y))

# --------------------------------------------------------------
class EntidadNpc(QObject): 

    identificador = 1
    def __init__(self, nombre: str, mapa, x: float, y: float, senal_mover, senal_cambiar_spirte):
        super().__init__()
        self.id = EntidadNpc.identificador
        EntidadNpc.identificador += 1
        self.nombre = nombre
        self.mapa = mapa
        self.x = x
        self.y = y
        self.posicion_original()
        self.senal_mover = senal_mover
        self.senal_cambiar_spirte = senal_cambiar_spirte
        self.direccion = 1
        self.setear_velocidad(self.nombre)
        self.calcular_paredes()
        self.sprite = 0
        self.timer_movimiento = QTimer(self)
        self.timer_movimiento.timeout.connect(self.mover)
        self.timer_movimiento.setInterval(int(self.velocidad))
        #self.mapa_cargado = False
        #self.start_timer()
    def posicion_original(self):
        # Util para las zanahorias volver a su posicion antigua (cañon)
        self.x_original = self.x
        self.y_original = self.y

    def setear_direccion(self):
        if self.nombre in ["LH","CR","LV","CU"]:
            self.direccion = 1
        else:
            self.direccion = -1

    def setear_velocidad(self, nombre_entidad:str):
        if nombre_entidad in ["LH","LV"]:
            self.velocidad = (parametros.VELOCIDAD_LOBO * 13 )
        else:
            self.velocidad = (parametros.VELOCIDAD_ZANAHORIA )
        #print(self.velocidad)

    def calcular_paredes(self):
        if self.nombre in ["LH", "CL", "CR"]:
            self.pared_izquierda = pared_left(self.mapa, self.x, self.y)
            self.pared_derecha = pared_right(self.mapa, self.x, self.y)

        elif self.nombre in ["LV", "CU", "CD"]:
            self.pared_arriba = pared_up(self.mapa, self.x, self.y)
            self.pared_abajo = pared_down(self.mapa, self.x, self.y)

# ---------------------------------------------------------------------
    def mover(self):
        # -------------------------------------------
        if self.nombre in ["LH", "CL", "CR"]:
            max_izquierda = ( self.pared_izquierda[0] + 1, self.pared_izquierda[1] )
            max_derecha   = ( self.pared_derecha[0] - 1, self.pared_derecha[1] )
            
            if self.nombre == "LH": 
                #---------- VA A LA DERECHA --------------
                if self.direccion == 1: 
                    if self.x >= max_derecha[0]: # Revisar cuando este en las paredes
                        self.direccion = -1
                        self.x -= 1/10
                        # ------- CAMBIAR SPRITE -------> ANIMACION
                        self.sprite += 1
                        if self.sprite == 4:
                            self.sprite = 1
                        self.senal_cambiar_spirte.emit(self.id, self.sprite, "IZQ")
                    else:
                        self.x += 1/10
                        # ------- CAMBIAR SPRITE -------> ANIMACION
                        self.sprite += 1
                        if self.sprite == 4:
                            self.sprite = 1
                        self.senal_cambiar_spirte.emit(self.id, self.sprite, "DER")
                #-------- VA A LA IZQUIERDA ---------------
                elif self.direccion == -1: 
                    if self.x <= max_izquierda[0] :
                    #or self.x - max_izquierda[0] < 0.1:
                        self.direccion = 1
                        self.x += 1/10
                        # ------- CAMBIAR SPRITE -------> ANIMACION
                        self.sprite += 1
                        if self.sprite == 4:
                            self.sprite = 1
                        self.senal_cambiar_spirte.emit(self.id, self.sprite, "DER")
                    else:
                        self.x -= 1/10
                        # ------- CAMBIAR SPRITE -------> ANIMACION
                        self.sprite += 1
                        if self.sprite == 4:
                            self.sprite = 1
                        self.senal_cambiar_spirte.emit(self.id, self.sprite, "IZQ")

            elif self.nombre == "CL":
                if self.x <= max_izquierda[0]:
                    # RESTABLECER POSICION
                    self.x = self.x_original
                    self.y = self.y_original
                else:
                    self.x -= 1/40
            elif self.nombre == "CR":
                if self.x >= max_derecha[0]:
                    # RESTABLECER POSICION
                    self.x = self.x_original
                    self.y = self.y_original
                else:
                    self.x += 1/40
        # ------------------------------------------
        elif self.nombre in ["LV", "CU", "CD"]:
            max_arriba = ( self.pared_arriba[0], self.pared_arriba[1] + 1 )
            max_abajo  = ( self.pared_abajo[0], self.pared_abajo[1] - 1 )
            
            if self.nombre == "LV":
                if self.direccion == 1: # VA A ABAJO
                    if self.y >= max_abajo[1]:
                        #or self.y - max_arriba[1] < 0.1:
                        self.direccion = -1
                        self.y -= 1/10
                        # ------- CAMBIAR SPRITE -------> ANIMACION
                        self.sprite += 1
                        if self.sprite == 4:
                            self.sprite = 1
                        self.senal_cambiar_spirte.emit(self.id, self.sprite, "ARRIBA")
                    else:
                        self.y += 1/10
                        # ------- CAMBIAR SPRITE -------> ANIMACION
                        self.sprite += 1
                        if self.sprite == 4:
                            self.sprite = 1
                        self.senal_cambiar_spirte.emit(self.id, self.sprite, "ABAJO")

                elif self.direccion == -1 : # VA A ARRIBA
                    if self.y <= max_arriba[1]:
                        self.direccion = 1
                        self.y += 1/10
                        # ------- CAMBIAR SPRITE -------> ANIMACION
                        self.sprite += 1
                        if self.sprite == 4:
                            self.sprite = 1
                        self.senal_cambiar_spirte.emit(self.id, self.sprite, "ABAJO")
                    else:
                        self.y -= 1/10
                        # ------- CAMBIAR SPRITE -------> ANIMACION
                        self.sprite += 1
                        if self.sprite == 4:
                            self.sprite = 1
                        self.senal_cambiar_spirte.emit(self.id, self.sprite, "ARRIBA")

            elif self.nombre == "CU":
                if self.y <= max_arriba[1]:
                    # RESTABLECER POSICION
                    self.x = self.x_original
                    self.y = self.y_original
                else:
                    self.y -= 1/40

            elif self.nombre == "CD":
                if self.y >= max_abajo[1]:
                    # RESTABLECER POSICION
                    self.x = self.x_original
                    self.y = self.y_original
                else:
                    self.y += 1/40

        self.senal_mover.emit(self.id, (self.x, self.y))

    def start_timer(self):
        self.timer_movimiento.start()
    
    def stop_timer(self):
        self.timer_movimiento.stop()

class Bomba(QObject):
    def __init__(self, id: int, nombre: str, mapa, x: float, y: float):
        super().__init__()
        self.id = id
        self.nombre = nombre
        self.mapa = mapa
        self.x = x
        self.y = y
        self.tecla = None
    #    self.calcular_paredes()

    #def calcular_paredes(self):
    #    self.pared_arriba = pared_up(self.mapa, self.x, self.y)
    #    self.pared_abajo = pared_down(self.mapa, self.x, self.y)
    #    self.pared_izquierda = pared_left(self.mapa, self.x, self.y)
    #    self.pared_derecha = pared_right(self.mapa, self.x, self.y)
    """ Revisar Cuando hacer al llamado -> hacerse segun los pixeles del frontend"""