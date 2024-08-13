from PyQt6.QtWidgets import (QMainWindow, QLabel, QPushButton, 
                            QApplication, QWidget, QLineEdit, 
                            QVBoxLayout, QHBoxLayout, QGridLayout,
                            QMessageBox)
from PyQt6.QtGui import QPixmap
import os

class Rutas(QWidget):

    def __init__(self):
        super().__init__()
        self.rutas_sprites = {} 
        self.añadir()

    def añadir(self):
        self.rutas_sprites["LH"] = [
                        [QPixmap(os.path.join('frontend', 'assets', 'sprites', 'lobo_horizontal_derecha_1.png')),
                         QPixmap(os.path.join('frontend', 'assets', 'sprites', 'lobo_horizontal_derecha_2.png')),
                         QPixmap(os.path.join('frontend', 'assets', 'sprites', 'lobo_horizontal_derecha_3.png'))  ],
                        [QPixmap(os.path.join('frontend', 'assets', 'sprites', 'lobo_horizontal_izquierda_1.png')),
                         QPixmap(os.path.join('frontend', 'assets', 'sprites', 'lobo_horizontal_izquierda_2.png')),
                         QPixmap(os.path.join('frontend', 'assets', 'sprites', 'lobo_horizontal_izquierda_3.png'))  ] ]
        self.rutas_sprites["LV"] = [
                    [
                        QPixmap(os.path.join('frontend', 'assets', 'sprites', 'lobo_vertical_abajo_1.png')),
                        QPixmap(os.path.join('frontend', 'assets', 'sprites', 'lobo_vertical_abajo_2.png')),
                        QPixmap(os.path.join('frontend', 'assets', 'sprites', 'lobo_vertical_abajo_3.png'))],
                    [
                        QPixmap(os.path.join('frontend', 'assets', 'sprites', 'lobo_vertical_arriba_1.png')),
                        QPixmap(os.path.join('frontend', 'assets', 'sprites', 'lobo_vertical_arriba_2.png')),
                        QPixmap(os.path.join('frontend', 'assets', 'sprites', 'lobo_vertical_arriba_3.png'))]  ]
        self.rutas_sprites["C"] = [
                    [
                        QPixmap(os.path.join('frontend', 'assets', 'sprites', 'conejo_arriba_1.png')),
                        QPixmap(os.path.join('frontend', 'assets', 'sprites', 'conejo_arriba_2.png')),
                        QPixmap(os.path.join('frontend', 'assets', 'sprites', 'conejo_arriba_3.png'))],
                    [
                        QPixmap(os.path.join('frontend', 'assets', 'sprites', 'conejo_abajo_1.png')),
                        QPixmap(os.path.join('frontend', 'assets', 'sprites', 'conejo_abajo_2.png')),
                        QPixmap(os.path.join('frontend', 'assets', 'sprites', 'conejo_abajo_3.png'))],
                    [
                        QPixmap(os.path.join('frontend', 'assets', 'sprites', 'conejo_derecha_1.png')),
                        QPixmap(os.path.join('frontend', 'assets', 'sprites', 'conejo_derecha_2.png')),
                        QPixmap(os.path.join('frontend', 'assets', 'sprites', 'conejo_derecha_3.png'))],
                    [
                        QPixmap(os.path.join('frontend', 'assets', 'sprites', 'conejo_izquierda_1.png')),
                        QPixmap(os.path.join('frontend', 'assets', 'sprites', 'conejo_izquierda_2.png')),
                        QPixmap(os.path.join('frontend', 'assets', 'sprites', 'conejo_izquierda_3.png'))]  ]
        
        self.rutas_sprites["rutas_entidades"] = {
            "C":  os.path.join('frontend', 'assets', 'sprites', 'conejo.png'),
            "BM": os.path.join('frontend', 'assets', 'sprites', 'manzana_burbuja.png'),
            "BC": os.path.join('frontend', 'assets', 'sprites', 'congelacion_burbuja.png'),
            "LH": os.path.join('frontend', 'assets', 'sprites', 'lobo_horizontal_derecha_1.png'),
            "LV": os.path.join('frontend', 'assets', 'sprites', 'lobo_vertical_abajo_1.png'),
            "CU": os.path.join('frontend', 'assets', 'sprites', 'canon_arriba.png'),
            "CD": os.path.join('frontend', 'assets', 'sprites', 'canon_abajo.png'),
            "CL": os.path.join('frontend', 'assets', 'sprites', 'canon_izquierda.png'),
            "CR": os.path.join('frontend', 'assets', 'sprites', 'canon_derecha.png')
        }

        self.rutas_sprites["rutas_zanahorias"] = {
            "CU": os.path.join('frontend', 'assets', 'sprites', 'zanahoria_arriba.png'),
            "CD": os.path.join('frontend', 'assets', 'sprites', 'zanahoria_abajo.png'),
            "CL": os.path.join('frontend', 'assets', 'sprites', 'zanahoria_izquierda.png'),
            "CR": os.path.join('frontend', 'assets', 'sprites', 'zanahoria_derecha.png')
        }

        self.rutas_sprites["BM"] = QPixmap(os.path.join('frontend', 'assets', 'sprites', 'explosion.png'))
        self.rutas_sprites["BC"] = QPixmap(os.path.join('frontend', 'assets', 'sprites', 'congelacion.png'))
        