import sys
import subprocess
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox
from PySide6.QtCore import Slot

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ejecutar Código")
        
        # Crear el botón
        self.button = QPushButton("Abrir script.py")
        
        # Conectar el clic al método que ejecuta el código
        self.button.clicked.connect(self.ejecutar_codigo)
        
        self.setCentralWidget(self.button)

    @Slot()
    def ejecutar_codigo(self):
        # Ruta al archivo que deseas abrir/ejecutar
        ruta_archivo = "script_destino.py"
        
        try:
            # subprocess.run ejecuta el archivo en un nuevo proceso
            # use os.startfile en Windows para abrirlo en el editor predeterminado
            # o subprocess para ejecutarlo.
            
            # Opción 1: Ejecutar como script de Python
            subprocess.run([sys.executable, ruta_archivo], check=True)
            
            # Opción 2: Abrir el archivo en el editor de código (ej. VS Code, Notepad)
            # import os
            # os.startfile(ruta_archivo) # Solo en Windows
            # subprocess.Popen(['xdg-open', ruta_archivo]) # Solo en Linux
            
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", f"El archivo {ruta_archivo} no se encontró.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())   