from PyQt6.QtWidgets import (QMainWindow, QLabel, QPushButton, 
                            QApplication, QWidget, QLineEdit, 
                            QVBoxLayout, QHBoxLayout, QGridLayout,
                            QMessageBox)
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont, QFontDatabase, QPixmap
import sys
import os

class VentanaInicio(QWidget):

    senal_abrir_juego = pyqtSignal()
    senal_pedir_ranking = pyqtSignal(str)
    senal_procesar_usuario = pyqtSignal(str)
    senal_salir = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        # Definimos lo básico de la ventana
        self.setWindowTitle("DCCConejoChicho")
        self.setGeometry(450, 100, 550, 600)
        self.setStyleSheet("background-color: #F0E8F5;")
        self.ranking()
        self.pedir_ranking()
        self.init_gui()
        self.show()

    def init_gui(self):
        # Label: Logo
        self.imagen = QLabel(self)
        ruta_imagen = os.path.join('frontend', 'assets', 'sprites', 'logo.png')
        pixeles = QPixmap(ruta_imagen)
        self.imagen.setPixmap(pixeles)
        self.imagen.setScaledContents(True)
        self.imagen.resize(self.imagen.sizeHint())
        self.imagen.setMaximumSize(700 * 2 // 3, 119 * 2 // 3)
        self.imagen.setStyleSheet("border: 10px solid #F000AF; border-radius: 10px; background-color: #F0E8F5; color: #F000AF") 
        # LAYOUT
        hbox_imagen = QHBoxLayout()
        hbox_imagen.addWidget(self.imagen)
        
        # Label: ¿Una Partida?
        self.label1 = QLabel("¿Una partida?", self)
        font_label = QFont("PT Mono", 25)
        #font_label = QFont("Monaco", 30)
        font_label.setBold(True)
        self.label1.setFont(font_label)
        self.label1.setStyleSheet("color: #F000AF;")
        # LAYOUT
        hbox_label1 = QHBoxLayout()
        hbox_label1.addStretch(1)
        hbox_label1.addWidget(self.label1)
        hbox_label1.addStretch(1)

        # Labels Ingresar usuario:
        self.label2 = QLabel("Ingresa tu Username: ", self)
        font_label = QFont("PT Mono", 15)
        #self.label2.move(20,100)
        self.label2.setFont(font_label)
        self.label2.setStyleSheet("color: #F000AF;")
        # QLineEdit
        self.label_usuario = QLineEdit(self)
        self.label_usuario.setFont(QFont("PT Mono", 20))
        #self.label_usuario.resize(self.label_usuario.sizeHint())
        self.label_usuario.setStyleSheet("border: 2px solid #F000AF; border-radius: 8px; background-color: #F0E8F5; color: #F000AF") 
        self.label_usuario.setFixedWidth(200)
        self.label_usuario.setFixedHeight(25)
        #self.label_usuario.move(210,97)         # Quitar una vez se hagan los hBox y vBox
        # LAYOUT
        hbox_label_usuario = QHBoxLayout() 
        hbox_label_usuario.addStretch(1)
        hbox_label_usuario.addWidget(self.label2)
        hbox_label_usuario.addWidget(self.label_usuario)
        hbox_label_usuario.addStretch(1)

        self.boton_ingresar = QPushButton('&Ingresar', self)
        font_label.setBold(True)
        self.boton_ingresar.setFont(font_label)
        self.boton_ingresar.setStyleSheet("QPushButton { border: 1px solid #F000AF; border-radius: 15px; background-color: #F000AF; color: #F0E8F5} QPushButton:pressed {background-color: #FF559F}")
        self.boton_ingresar.resize(self.boton_ingresar.sizeHint())
        self.boton_ingresar.setFixedWidth(100)
        self.boton_ingresar.setFixedHeight(45)
        self.boton_ingresar.clicked.connect(self.procesar_usuario)

        self.boton_salir = QPushButton('&Salir', self)
        self.boton_salir.setFont(font_label)
        self.boton_salir.setStyleSheet("QPushButton { border: 1px solid #F000AF; border-radius: 15px; background-color: #F000AF; color: #F0E8F5} QPushButton:pressed {background-color: #FF059F}")
        self.boton_salir.resize(self.boton_salir.sizeHint())
        self.boton_salir.setFixedWidth(100)
        self.boton_salir.setFixedHeight(45)
        self.boton_salir.clicked.connect(self.salir)
        # LAYOUT
        hbox_label_botones = QHBoxLayout() 
        hbox_label_botones.addStretch(1)
        hbox_label_botones.addWidget(self.boton_ingresar)
        hbox_label_botones.addStretch(1)
        hbox_label_botones.addWidget(self.boton_salir)
        hbox_label_botones.addStretch(1)

        self.label_salonfama = QLabel("------ Salón de la Fama Maxima ------", self)
        font_label = QFont("PT Mono", 20)
        font_label.setBold(True)
        self.label_salonfama.setFont(font_label)
        self.label_salonfama.setStyleSheet("border: 2px solid #F000AF; border-radius: 20px; background-color: #F0E8F5; color: #F000AF") 
        #self.label_salonfama.clicked.connect(self.pedir_ranking)
        # LAYOUT
        hbox_label_salon_fama = QHBoxLayout() 
        hbox_label_salon_fama.addStretch(1)
        hbox_label_salon_fama.addWidget(self.label_salonfama)
        hbox_label_salon_fama.addStretch(1)

        hbox_vbox_ranking = QHBoxLayout()
        hbox_vbox_ranking.addStretch(1)
        hbox_vbox_ranking.addLayout(self.vbox_ranking)
        hbox_vbox_ranking.addStretch(1)

        vbox_main = QVBoxLayout()
        vbox_main.addLayout(hbox_imagen)
        vbox_main.addStretch(1)
        vbox_main.addLayout(hbox_label1)
        vbox_main.addStretch(1)
        vbox_main.addLayout(hbox_label_usuario)
        vbox_main.addStretch(1)
        vbox_main.addLayout(hbox_label_botones)
        vbox_main.addStretch(1)
        vbox_main.addLayout(hbox_label_salon_fama)
        vbox_main.addStretch(1)
        vbox_main.addLayout(hbox_vbox_ranking)
        vbox_main.addStretch(1)

        self.setLayout(vbox_main)
    
    def ranking(self):
        self.vbox_ranking = QVBoxLayout()
        self.top_5 = []
        for i in range(5):
            jugador = QLabel(f"{i+1}.- ", self)
            font_label = QFont("PT Mono", 15)
            font_label.setBold(True)
            jugador.setFont(font_label)
            jugador.setStyleSheet("color: #F000AF;")
            self.top_5.append(jugador)
            self.vbox_ranking.addWidget(jugador)

    def pedir_ranking(self):
        self.senal_pedir_ranking.emit("3")

    def actualizar_ranking(self, top_5: str):
        top = top_5.split(";")
        ranking_nuevo = []
        for partida in top:
            ranking_nuevo.append( partida.split(",") )
        for i in range(5):
            jugador = ranking_nuevo[i]
            self.top_5[i].setText(f"{i+1}.- {jugador[0]} - lvl: {jugador[1]} >>> {jugador[2]} ptos")

    def salir(self):
        self.close()
        self.senal_salir.emit("0") # Recibir por el backend y cerrar conexion!

    def procesar_usuario(self):
        usuario = self.label_usuario.text()
        self.senal_procesar_usuario.emit(usuario)

    def recibir_info_usuario(self, mensaje: str): # Recibimos o no valido o partida
        # LLEGA LA INFO DESDE EL BACKEND
        if mensaje == "FORMATO NO VALIDO":
            print("Formato No valido")
            self.mostrar_mensaje("¡El formato no es valido 🥲! : Nombre Usuario: 3 < largo < 16 con Mayusculas y Numeros")
            # Desplegar ventana emergente explicando NO VALIDO + Formato correcto
        elif mensaje == "NO VALIDO":
            print("Usuario Bloqueado")
            self.mostrar_mensaje("¡Usuario Bloqueado 😭! : No puedes acceder con este username")
            # Desplegar ventana emergente explicando Usuario Bloqueado
        else:
            self.mostrar_mensaje(f"User: {mensaje} >>> EMPEZANDO PARTIDA!!!", partida_valida= True)

    def mostrar_mensaje(self, mensaje: str, partida_valida = None):
        if partida_valida == None:
            QMessageBox.warning(self, "Error", mensaje, 
                            QMessageBox.StandardButton.Close,
                            QMessageBox.StandardButton.Close )
        else:
            QMessageBox.warning(self, "EMPEZANDO EL JUEGO", mensaje, 
                            QMessageBox.StandardButton.Close,
                            QMessageBox.StandardButton.Close )
            self.senal_abrir_juego.emit()
            self.close()

    #def desconexion_servidor(self):
    #    QMessageBox.warning(self, "Desconexion", f"😭 Desconexión con el servidor 😭", 
    #                        QMessageBox.StandardButton.Close,
    #                        QMessageBox.StandardButton.Close )
    #    #self.close()

if __name__ == '__main__':
    def hook(type, value, traceback):
        print(type)
        print(traceback)
    sys.__excepthook__ = hook    
    app = QApplication([])

    ventana_inicio = VentanaInicio()

    sys.exit(app.exec())





