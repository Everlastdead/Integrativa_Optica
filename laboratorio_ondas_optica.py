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


class VentanaPrincipal(QWidget):

	def __init__(self):
		super().__init__()

		
		self.setWindowTitle("Laboratoria Onda Optica")
		self.resize(800,500)

		layout = QHBoxLayout()

		Button2 = QPushButton("Modulo Ondas")
		Button2.setFixedSize(400,100)

		
		Button1 = QPushButton("Modulo Optica Geometrica")
		Button1.setFixedSize(400,100)
		Button1.clicked.connect(self.modulo_ondas)
		layout.addWidget(Button1)
		layout.addWidget(Button2)
		
	

		self.setLayout(layout)

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