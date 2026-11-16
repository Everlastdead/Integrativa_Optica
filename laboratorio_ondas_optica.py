import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QHBoxLayout,
    QMessageBox
)


class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Laboratorio de Ondas y Óptica")
        self.resize(800, 500)

        layout = QHBoxLayout()

        # Botón para abrir el Módulo de Óptica Geométrica
        ButtonGeo = QPushButton("Módulo Óptica Geométrica")
        ButtonGeo.setFixedSize(350, 100)
        ButtonGeo.clicked.connect(self.abrir_GeoOp)

        # Botón para abrir el Módulo de Ondas
        ButtonOnda = QPushButton("Módulo Ondas")
        ButtonOnda.setFixedSize(350, 100)
        ButtonOnda.clicked.connect(self.abrir_MOndas)

        layout.addWidget(ButtonGeo)
        layout.addWidget(ButtonOnda)
        self.setLayout(layout)

    def abrir_GeoOp(self):
        try:
            from modulo_optica_geometrica import GeoOp
            self.hide()
            self.sec = GeoOp(self)
            self.sec.show()
        except ImportError as e:
            QMessageBox.critical(
                self,
                "Error de importación",
                f"No se pudo cargar 'modulo_optica_geometrica.py'. Verifica que esté en la misma carpeta.\n\nDetalle: {e}"
            )

    def abrir_MOndas(self):
        try:
            from modulo_ondas import MOndas
            self.hide()
            self.ter = MOndas(self)
            self.ter.show()
        except ImportError as e:
            QMessageBox.critical(
                self,
                "Error de importación",
                f"No se pudo cargar 'modulo_ondas.py'. Verifica que esté en la misma carpeta.\n\nDetalle: {e}"
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())