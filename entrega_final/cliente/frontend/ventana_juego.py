from PyQt6.QtWidgets import (QMainWindow, QLabel, QPushButton, 
                            QApplication, QWidget, QLineEdit, 
                            QVBoxLayout, QHBoxLayout, QGridLayout,
                            QMessageBox)
from PyQt6.QtCore import pyqtSignal, Qt, QUrl
from PyQt6.QtGui import QFont, QFontDatabase, QPixmap, QIcon
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput, QSoundEffect
import sys
import os
from frontend.rutas import Rutas 

class VentanaJuego(QWidget):
    ## Señales
    senal_abrir_juego = pyqtSignal()
    senal_salir = pyqtSignal(str)
    senal_detener_tiempo = pyqtSignal()
    senal_parar_entidad = pyqtSignal(int)
    senal_empezar_a_mover = pyqtSignal(int)
    senal_tecla = pyqtSignal(str)
    senal_pausa = pyqtSignal()
    senal_avanzar_nivel = pyqtSignal()
    senal_cheatcode = pyqtSignal(str) # kil o inf

    def __init__(self):
        super().__init__()
        """ --- Aqui pondremos un diccionario con lo necesario, 
        los Qlabels con Imagenes que moveremos con señales desde el backend ---"""
        self.entidades = {}
        self.sprites = {}
        self.input_teclas = ""
        self.cargar_sprites()
        self.setWindowTitle("DCConejoChicho")
        self.setGeometry(200, 75, 970, 650)
        self.setStyleSheet("background-color: #F0E8F5;")
        self.init_gui()
        self.setFixedSize(970,670)

    def keyPressEvent(self, event):
        """ --- Manejamos WASD en la logica, ademas de p (pausa) --- """ 
        #print(f"Recibi {event.text()}")
        if event.text().lower() in ["a","s","d","w"]:
            self.senal_tecla.emit(event.text())
        elif event.text().lower() == "p":
            self.pausa()
        else:
            self.input_teclas += event.text().lower()
            if "kil" in self.input_teclas:
                print("USASTE EL CHEATCODE KILL")
                self.mandar_senal("kil")
                self.input_teclas = ""

            if "inf" in self.input_teclas.lower():
                print("USASTE EL CHEATCODE INF")
                self.mandar_senal("inf")
                self.input_teclas = ""

    def mandar_senal(self, mensaje):
        self.senal_cheatcode.emit(mensaje)

    def matar_todos(self):
        #self.entidades = {}
        keys = self.entidades.keys()
        for key in keys:
            if self.entidades[key][1] in ["C", "BM", "BC"]:
                pass
            else:
                self.entidades[key][0].hide()


    def pausa(self):
        self.senal_pausa.emit()

    def mostrar_ventana_juego(self):
        self.show()

    def reset_entidades(self, nivel: int):
        """ --- Metodo Util para cambiar de nivel -> Tablero y Entidades ---"""
        self.entidades = {}
        self.nivel = nivel
        self.cargar_mapa(self.nivel)

    def setear_nivel(self, usuario: str, nivel: int):
        """---Metodo para setear los niveles, cargando los mapas---"""
        self.nivel = nivel
        self.usuario = usuario
        self.setWindowTitle(f"Jugador: {usuario} - Nivel {nivel}")
        self.cargar_mapa(self.nivel)

    def cargar_sprites(self):
        """---De aquí sacaremos las rutas para concretar las animaciones de las entidades,
        vienen de otra clase llamada RUTAS"""
        rutas = Rutas()
        self.sprites["LH"] = rutas.rutas_sprites["LH"]
        self.sprites["LV"] = rutas.rutas_sprites["LV"]
        self.sprites["C"] = rutas.rutas_sprites["C"]
        
    def init_gui(self):
        """---Definimos todos los Qlabels, Sonidos, y Botones necesarios en la Ventana del juego---"""
        self.victoria_mp3 = QMediaPlayer(self)
        self.victoria_mp3.setAudioOutput(QAudioOutput(self))
        file_url = QUrl.fromLocalFile(os.path.join('frontend', 'assets', 'sonidos', 'victoria.mp3'))
        self.victoria_mp3.setSource(file_url)
        #-------------------------------------
        self.derrota_mp3 = QMediaPlayer(self)
        self.derrota_mp3.setAudioOutput(QAudioOutput(self))
        file_2_url = QUrl.fromLocalFile(os.path.join('frontend', 'assets', 'sonidos', 'derrota.mp3'))
        self.derrota_mp3.setSource(file_2_url)
        # -------------------------------------
        self.label_tiempo = QLabel("Tiempo restante: ", self)
        font_label = QFont("PT Mono", 15)
        font_label.setBold(True)
        self.label_tiempo.setFont(font_label)
        self.label_tiempo.setStyleSheet("color: #F000AF;")
        self.label_tiempo.move(20, 20)
        # -------------------------------------
        self.label_vidas = QLabel("Vidas restantes: ", self)
        self.label_vidas.setFont(font_label)
        self.label_vidas.setStyleSheet("color: #F000AF;")
        self.label_vidas.move(20, 45)
        # -------------------------------------
        self.boton_salir = QPushButton('&Salir', self)
        self.boton_salir.setFont(font_label)
        self.boton_salir.setStyleSheet("""QPushButton { border: 1px solid #F000AF;
                                    border-radius: 15px; background-color: #F000AF;
                                    color: #F0E8F5} QPushButton:pressed {background-color: #FF059F}""")
        self.boton_salir.resize(self.boton_salir.sizeHint())
        self.boton_salir.setFixedWidth(100)
        self.boton_salir.setFixedHeight(45)
        self.boton_salir.clicked.connect(self.salir)
        self.boton_salir.move(20, 75)
        # -------------------------------------
        self.boton_pausa = QPushButton('&Pausa', self)
        self.boton_pausa.setFont(font_label)
        self.boton_pausa.setStyleSheet("""QPushButton { border: 1px solid #F000AF; 
                                       border-radius: 15px; background-color: #F000AF; 
                                       color: #F0E8F5} QPushButton:pressed {background-color: #FF059F}""")
        self.boton_pausa.resize(self.boton_salir.sizeHint())
        self.boton_pausa.setFixedWidth(100)
        self.boton_pausa.setFixedHeight(45)
        self.boton_pausa.move(150, 75)   
        self.boton_pausa.clicked.connect(self.pausa)
        # -------------------------------------
        hbox_botones = QHBoxLayout()
        hbox_botones.addStretch(1)
        hbox_botones.addWidget(self.boton_salir) 
        #hbox_botones.addStretch(1)
        hbox_botones.addWidget(self.boton_pausa) 
        hbox_botones.addStretch(1)
        # -------------------------------------
        self.label_inventario = QLabel("Inventario: ", self)
        self.label_inventario.setFont(font_label)
        self.label_inventario.setStyleSheet("color: #F000AF;")
        self.label_inventario.move(20, 140)
        # -------------------------------------
        self.label_box_inventario = QLabel(self)
        self.label_box_inventario.setFont(font_label)
        self.label_box_inventario.setStyleSheet("""border: 2px solid #F000AF; 
                                                border-radius: 10px; 
                                                background-color: #F0E8FF; color: #F0E8F5""")
        self.label_box_inventario.resize(self.boton_salir.sizeHint())
        self.label_box_inventario.setFixedWidth(250)
        self.label_box_inventario.setFixedHeight(400)
        self.label_box_inventario.move(20, 170)    
        # -------------------------------------
        self.label_puntaje = QLabel("Puntaje Actual: ", self)
        font_label = QFont("PT Mono", 15)
        font_label.setBold(True)
        self.label_puntaje.setFont(font_label)
        self.label_puntaje.setStyleSheet("color: #F000AF;")
        """---Aqui generaremos la barra izquierda, 
        con el inventario los mensajes y botones!---"""
        vbox_lateral = QVBoxLayout()
        vbox_lateral.addWidget(self.label_tiempo)
        vbox_lateral.addStretch(1)
        vbox_lateral.addWidget(self.label_vidas)
        vbox_lateral.addStretch(1)
        vbox_lateral.addLayout(hbox_botones)
        vbox_lateral.addStretch(1)
        vbox_lateral.addWidget(self.label_inventario)
        vbox_lateral.addStretch(1)
        vbox_lateral.addWidget(self.label_box_inventario)
        vbox_lateral.addStretch(1)
        vbox_lateral.addWidget(self.label_puntaje)
        vbox_lateral.addStretch(1)
        # ------- MAPA (GRILLA) --------
        self.layout_mapa = QGridLayout()
        #self.layout_mapa.setContentsMargins(0, 0, 0, 0)
        self.layout_mapa.setHorizontalSpacing(0)
        self.layout_mapa.setVerticalSpacing(0)
        # LAYOUT PRINCIPAL DE LA VENTANA JUEGO
        hbox_main = QHBoxLayout()
        hbox_main.addLayout(vbox_lateral)
        hbox_main.addStretch(1)
        hbox_main.addLayout(self.layout_mapa)
        self.setLayout(hbox_main)
        # -------- BOTONES DEL INVENTARIO ---------
        self.boton_bomba_manzana = QPushButton(self)
        self.boton_bomba_manzana.setStyleSheet("""QPushButton { border: 1px solid #F000AF; 
                                               border-radius: 10px; background-color:#F0E8FF; 
                                               color: #F0E8F5} QPushButton:pressed {background-color: #FF09aF}""")
        ruta_imagen = os.path.join('frontend', 'assets', 'sprites', 'manzana.png')
        pixeles = QPixmap(ruta_imagen)
        pixeles = pixeles.scaled(60, 60)
        self.boton_bomba_manzana.resize(self.boton_bomba_manzana.sizeHint())
        icono = QIcon(pixeles)
        self.boton_bomba_manzana.setIcon(icono)
        self.boton_bomba_manzana.setIconSize(pixeles.size())
        self.boton_bomba_manzana.setFixedSize(80, 80) 
        self.boton_bomba_manzana.move(100, 250)   
        self.boton_bomba_manzana = QPushButton(self)
        self.boton_bomba_manzana.setStyleSheet("""QPushButton { border: 1px solid #F000AF; 
                                               border-radius: 10px; background-color:#F0E8FF; 
                                               color: #F0E8F5} QPushButton:pressed {background-color: #FF09aF}""")
        ruta_imagen = os.path.join('frontend', 'assets', 'sprites', 'congelacion.png')
        pixeles = QPixmap(ruta_imagen)
        pixeles = pixeles.scaled(60, 60)
        self.boton_bomba_manzana.resize(self.boton_bomba_manzana.sizeHint())
        icono = QIcon(pixeles)
        self.boton_bomba_manzana.setIcon(icono)
        self.boton_bomba_manzana.setIconSize(pixeles.size())
        self.boton_bomba_manzana.setFixedSize(80, 80) 
        self.boton_bomba_manzana.move(100, 400)  

    def salir(self):
        """---Metodo para detener el reloj, y salir de la partida---"""
        self.senal_detener_tiempo.emit()
        self.close()
        self.senal_salir.emit("0") # Recibir por el backend y cerrar conexion!

    """A CONTINUACION: MENSAJES QUE SALTAN AL USUARIO"""
    def pasar_nivel(self, nivel):
        self.entidades[0][0].hide()
        self.victoria_mp3.play()
        QMessageBox.warning(self, "Nivel Pasado", 
                            f"⭐️ Felicidades, pasaste el nivel: {int(nivel) - 1} ⭐️", 
                            QMessageBox.StandardButton.Close,
                            QMessageBox.StandardButton.Close )
        
    def pasar_juego(self):
        QMessageBox.warning(self, "Nivel Pasado", 
                            f"😎 Felicidades! Terminaste el Juego, Eres todo un DCConejoGRANDE🐰", 
                            QMessageBox.StandardButton.Close,
                            QMessageBox.StandardButton.Close )
    def desconexion_servidor(self):
        QMessageBox.warning(self, "Desconexion", 
                            f"😭 Desconexión con el servidor 😭", 
                            QMessageBox.StandardButton.Close,
                            QMessageBox.StandardButton.Close )
        self.close()
    def perdiste(self):
        self.derrota_mp3.play()
        QMessageBox.warning(self, "Perdiste", 
                            f"😭 DCConejito ha perdido la vida 😭", 
                            QMessageBox.StandardButton.Close,
                            QMessageBox.StandardButton.Close )

    def cargar_mapa(self, nivel):
        """---Carga el mapa y llama a la funcion mostrar mapa -> entidades---"""
        with open( os.path.join('frontend', 'assets', 'laberintos', 
                                f'tablero_{nivel}.txt'), "r") as archivo:
            mapa = archivo.readlines()
        laberinto = []
        for i in mapa:
            laberinto.append(i.strip(",\n").split(","))
        self.mostrar_mapa(laberinto)

    def mostrar_mapa(self, mapa: list[list]):
        """---Metodo inicial para rellenar el mapa de solo bloques de fondo y paredes---"""
        elementos = []
        for elem in mapa:
            for e in elem:
                elementos.append(e)
        imagenes = {
            "-": os.path.join('frontend', 'assets', 'sprites', 'bloque_fondo.jpeg'),
            "P": os.path.join('frontend', 'assets', 'sprites', 'bloque_pared.jpeg')
        }
        posiciones = [(i,j) for i in range(16) for j in range(16)]
        for posicion, valor in zip(posiciones, elementos):
            if valor == "P":
                imagen = QLabel(valor ,self)
                ruta_imagen = imagenes["P"]
                pixeles = QPixmap(ruta_imagen)
                imagen.setPixmap(pixeles)
                imagen.setScaledContents(True)
                imagen.resize(imagen.sizeHint())
                imagen.setMaximumSize(40, 40)
                self.layout_mapa.addWidget(imagen, *posicion)
            else:
                imagen_2 = QLabel(valor, self)
                ruta_imagen = imagenes["-"]
                pixeles = QPixmap(ruta_imagen)
                imagen_2.setPixmap(pixeles)
                imagen_2.setScaledContents(True)
                imagen_2.resize(imagen.sizeHint())
                imagen_2.setMaximumSize(40, 40)
                self.layout_mapa.addWidget(imagen_2, *posicion)
# -----------------------------------------------------------------------------
    def reloj(self, tiempo: int, vidas: int, puntaje: int):
        """ ---Este metodo funciona con un Timer desde el Backend 
        -> Actualiza parametros del frontend (QLabels)---"""
        self.label_tiempo.setText(f"Tiempo restante: {tiempo}")
        self.label_tiempo.resize(self.label_tiempo.sizeHint())
        self.label_vidas.setText(f"Vidas restantes: {vidas}")
        self.label_puntaje.setText(f"Puntaje Actual: {puntaje}")
# -----------------------------------------------------------------------------
    def colocar_entidad(self, entidad: str, posicion_inicial: tuple, id: int):
        """---Este metodo rellena el mapa con los assets principales de las Entidades del juego---"""
        rutas = Rutas()
        rutas_entidades = rutas.rutas_sprites["rutas_entidades"]
        rutas_zanahorias = rutas.rutas_sprites["rutas_zanahorias"]
        entidad_img = QLabel(entidad, self)
        ruta = rutas_entidades[entidad]
        pixeles = QPixmap(ruta)
        self.setear_imagen(entidad_img, pixeles)
        x, y = posicion_inicial
        if y < 10:
            entidad_img.move( 310 + (40 * x) , 20 + (40 * y) )
        else:
            entidad_img.move( 310 + (40 * x) , 10 + (40 * y) )
        self.entidades[id] = [entidad_img,entidad]
        entidad_img.show()
        # --- Para zanahorias : cambio la imagen del cañon por la zanahoria ----
        if entidad in ["CU","CD","CR","CL"]:
            zanahoria_img = QLabel(entidad, self)
            ruta = rutas_zanahorias[entidad]
            pixeles = QPixmap(ruta)
            self.setear_imagen(zanahoria_img, pixeles)
            self.entidades[id][0] = zanahoria_img
            x, y = posicion_inicial
            if y < 10:
                zanahoria_img.move( 310 + 40*x , 20 + 40*y )
            else:
                zanahoria_img.move( 310 + 40*x , 10 + 40*y )
            zanahoria_img.show()
        # --- Emitir señal para empezar a mover a los NPC en el mapa ---
        self.senal_empezar_a_mover.emit(id)

    def animacion(self, id: int, sprite: int, direccion: str):
        if self.entidades[id][1] == "LH":
            if direccion == "DER":
                pixeles = self.sprites["LH"][0][sprite-1]
                self.setear_imagen(self.entidades[id][0], pixeles)

            if direccion == "IZQ":
                pixeles = self.sprites["LH"][1][sprite-1]
                self.setear_imagen(self.entidades[id][0], pixeles)

        elif self.entidades[id][1] == "LV":
            if direccion == "ABAJO":
                pixeles = self.sprites["LV"][0][sprite-1]
                self.setear_imagen(self.entidades[id][0], pixeles)

            if direccion == "ARRIBA":
                pixeles = self.sprites["LV"][1][sprite-1]
                self.setear_imagen(self.entidades[id][0], pixeles)

    def animacion_conejo(self, id: int, sprite: int, direccion: str):
        if direccion == "BASE":
            pixeles = QPixmap(os.path.join('frontend', 'assets', 'sprites', 'conejo.png'))
            self.setear_imagen(self.entidades[id][0], pixeles)
        if direccion == "ARRIBA":
            pixeles = self.sprites["C"][0][sprite-1]
            self.setear_imagen(self.entidades[id][0], pixeles)
        if direccion == "ABAJO":
            pixeles = self.sprites["C"][1][sprite-1]
            self.setear_imagen(self.entidades[id][0], pixeles)
        if direccion == "DER":
            pixeles = self.sprites["C"][2][sprite-1]
            self.setear_imagen(self.entidades[id][0], pixeles)
        if direccion == "IZQ":
            pixeles = self.sprites["C"][3][sprite-1]
            self.setear_imagen(self.entidades[id][0], pixeles)

    """Metodo que mueve las entidades, controlado por el backend a traves de señales"""
    def mover_entidad(self, id, tupla):
        x, y = tupla
        label = self.entidades[id][0]
        if self.entidades[id][1] in ["CU","CD","CR","CL"]:
            label.move(  int(310 + (40 * x)), int(10 + (40 * y))  )
        else:
            label.move(  int(310 + (40 * x)), int(20 + (40 * y))  )

    def setear_imagen(self, label, pixeles):
            label.setPixmap(pixeles)
            label.setAutoFillBackground(False)
            label.setStyleSheet("background: transparent; border: none;")
            label.setMinimumSize(40, 40)
            label.setMaximumSize(40, 40)
            label.setScaledContents(True)
            label.resize(label.sizeHint())


