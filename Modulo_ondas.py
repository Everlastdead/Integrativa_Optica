import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import sys
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

from laboratorio_ondas_optica import VentanaPrincipal 

class MOndas(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.setWindowTitle("Modulo_ondas")
        self.resize(700,500)

        layout = QGridLayout()

        btn_volver = QPushButton("Regresar al principio")
        btn_volver.clicked.connect(self.volver)

        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.fig.subplots_adjust(bottom=0.25)
        #plt.subplots_adjust(bottom=0.25)  # Deja espacio inferior para los deslizadores[cite: 2]



        self.canvas = FigureCanvasQTAgg(self.fig)
            
        # 1. Parámetros iniciales del modelo físico
        self.A_init = 1.0
        self.lam_init = 2.0
        self.f_init = 1.0

        k_init = 2 * np.pi / self.lam_init
        self.x = np.linspace(0, 8.0, 500)
        y = self.A_init * np.sin(k_init * self.x)


        # 3. Configuración de la figura y ejes principales
        #omega_init = 2 * np.pi * self.f_init
        #fig, ax = plt.subplots()
            
        (self.linea,) = self.ax.plot(self.x, y)
        self.ax.set_ylim(-2.0, 2.0)
        self.ax.grid(True)

            # 4. Creación de ejes específicos para cada deslizador
        ax_amp = self.fig.add_axes([0.25, 0.15, 0.60, 0.03])
        ax_lam = self.fig.add_axes([0.25, 0.09, 0.60, 0.03])
        ax_freq = self.fig.add_axes([0.25, 0.03, 0.60, 0.03])

            # 5. Instanciación de los Sliders
        self.slider_A = Slider(ax_amp, "Amplitud (m)", 0.1, 1.5, valinit=self.A_init)
        self.slider_lam = Slider(ax_lam, "Longitud de onda", 1.0, 4.0, valinit=self.lam_init)
        self.slider_f = Slider(ax_freq, "Frecuencia (Hz)", 0.5, 5.0, valinit=self.f_init)
            
        layout.addWidget(btn_volver,0,0)
        layout.addWidget(self.canvas, 1, 0, 3, 3)

        self.setLayout(layout)
# 7. Guardar la animación en self para que Python no la borre de la memoria
        self.animacion = FuncAnimation(
            self.fig,
            self.actualizar,
            frames=200,
            interval=40,
            blit=False,
            cache_frame_data=False,
        )

            # 6. Función de actualización integrada (Animación + Sliders)
    def actualizar(self, frame):
        t = frame * 0.04
                
            # Leer valores actuales de los deslizadores
        A_actual = self.slider_A.val
        f_actual = self.slider_f.val
        lam_actual = self.slider_lam.val

            #Recalcular constantes físicas
        k_actual = 2 * np.pi / lam_actual
        omega_actual = 2 * np.pi * f_actual

            # Calcular nuevo perfil de onda
        y_actual = A_actual * np.sin(k_actual * self.x - omega_actual * t)
                
            # Actualizar la gráfica
        self.linea.set_ydata(y_actual)
        return (self.linea,)

            

    def volver(self):
        self.close()
        self.main_window.show()
            