from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QPushButton,
    QLabel,
    QLineEdit,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QFormLayout,
    QMessageBox,
    QDialog
    
    
)

from PySide6.QtCore import Qt , Slot
from PySide6.QtGui import QFont

import sys
import subprocess
import os


class GeoOp(QWidget):
	def __init__(self, main_window):
		super().__init__()

		self.main_window = main_window

		self.setWindowTitle("Onda Geometrica")

		self.resize(400,300)

		layout =QVBoxLayout()
		btn_volver = QPushButton("Regresa al principio")
		btn_volver.clicked.connect(self.volver)
		layout.addWidget(btn_volver)
		self.setLayout(layout)

	def volver(self):
		self.close()
		self.main_window.show()

class VentanaPrincipal(QWidget):

	def __init__(self):
		super().__init__()

		
		self.setWindowTitle("Laboratoria Onda Optica")
		self.resize(800,500)

		layout = QHBoxLayout()

		#manejo de button a menu de ondas
		ButtonOnda = QPushButton("Modulo Ondas")
		ButtonOnda.setFixedSize(400,100)
		#ButtonOnda.clicked.connect(VentanaSecundaria())
		ButtonOnda.clicked.connect(self.abrir_MOndas)


		#majeno de button menu de Optica Geometrica
		ButtonGeo = QPushButton("Modulo Optica Geometrica")
		ButtonGeo.setFixedSize(400,100)
		ButtonGeo.clicked.connect(self.abrir_GeoOp)

		layout.addWidget(ButtonGeo)
		layout.addWidget(ButtonOnda)
		self.setLayout(layout)


	def abrir_GeoOp(self):
		self.hide()
		self.sec = GeoOp(self)
		self.sec.show()

	def abrir_MOndas(self):
		from Modulo_ondas import MOndas
		self.hide()
		self.ter = MOndas(self)
		self.ter.show()

	@Slot()
	def modulo_ondas(self):
		directorio = os.path.dirname(os.path.abspath(__file__))
		ruta_archivo = os.path.join(directorio, "int.py")

		try:
			subprocess.Popen([sys.executable, ruta_archivo])
		except FileNotFoundError:
			QMessageBox.warning(self, "Error", f"El archivo {ruta_archivo} no se encontró.")
		except Exception as e:
			QMessageBox.critical(self, "Error", f"Ocurrió un error: {e}")

if __name__ == "__main__":

	app = QApplication(sys.argv)
	ventana = VentanaPrincipal()
	ventana.show()
	sys.exit(app.exec())

