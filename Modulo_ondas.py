import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, RadioButtons
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLabel,
    QGridLayout
)


class MOndas(QWidget):
    def __init__(self, main_window=None):
        super().__init__()

        self.main_window = main_window
        self.setWindowTitle("Módulo A: Ondas y Superposición")
        self.resize(850, 620)

        layout = QGridLayout()

        # Botón para regresar al menú principal
        btn_volver = QPushButton("Regresar al principio")
        btn_volver.clicked.connect(self.volver)

        # Etiqueta para mostrar los cálculos físicos en tiempo real (Prueba 1 y 2)
        self.lbl_datos = QLabel()
        self.lbl_datos.setStyleSheet("font-weight: bold; font-size: 13px; padding: 4px;")

        # Configuración de la figura embebida en PySide6
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.fig.subplots_adjust(bottom=0.36)
        self.canvas = FigureCanvasQTAgg(self.fig)

        # 1. Parámetros iniciales del modelo físico
        self.A_init = 1.0
        self.lam_init = 2.0
        self.f_init = 2.0
        self.fase_init = 0.0

        self.x = np.linspace(0, 8.0, 500)
        y_cero = np.zeros_like(self.x)

        # 2. Tres curvas: Onda 1, Onda 2 y Onda Resultante
        (self.linea1,) = self.ax.plot(self.x, y_cero, "--", alpha=0.65, label="Onda 1 ($y_1$)")
        (self.linea2,) = self.ax.plot(self.x, y_cero, "--", alpha=0.65, label="Onda 2 ($y_2$)")
        (self.linea_res,) = self.ax.plot(
            self.x, y_cero, linewidth=2.2, color="black", label="Resultante ($y_1 + y_2$)"
        )

        self.ax.set_ylim(-3.2, 3.2)
        self.ax.set_xlabel("Posición x (m)")
        self.ax.set_ylabel("Desplazamiento y (m)")
        self.ax.set_title("Simulación de Ondas Armónicas y Superposición")
        self.ax.grid(True)
        self.ax.legend(loc="upper right")

        # 3. Ejes para los controles interactivos dentro de la figura
        ax_amp = self.fig.add_axes([0.30, 0.23, 0.55, 0.03])
        ax_lam = self.fig.add_axes([0.30, 0.17, 0.55, 0.03])
        ax_freq = self.fig.add_axes([0.30, 0.11, 0.55, 0.03])
        ax_fase = self.fig.add_axes([0.30, 0.05, 0.55, 0.03])
        ax_dir = self.fig.add_axes([0.03, 0.05, 0.16, 0.18])

        # 4. Instanciación de Sliders y RadioButtons
        self.slider_A = Slider(ax_amp, "Amplitud A (m)", 0.1, 1.5, valinit=self.A_init)
        self.slider_lam = Slider(ax_lam, "Long. onda λ (m)", 0.5, 4.0, valinit=self.lam_init)
        self.slider_f = Slider(ax_freq, "Frecuencia f (Hz)", 0.5, 5.0, valinit=self.f_init)
        self.slider_fase = Slider(ax_fase, "Desfase Δφ (rad)", 0.0, 2 * np.pi, valinit=self.fase_init)
        self.radio_dir = RadioButtons(ax_dir, ("Mismo sentido", "Sentido opuesto"))

        # Ubicar widgets en el layout de PySide6
        layout.addWidget(btn_volver, 0, 0)
        layout.addWidget(self.lbl_datos, 0, 1, 1, 2)
        layout.addWidget(self.canvas, 1, 0, 3, 3)
        self.setLayout(layout)

        # 5. Guardar la animación en self para mantenerla en memoria
        self.animacion = FuncAnimation(
            self.fig,
            self.actualizar,
            frames=200,
            interval=40,
            blit=False,
            cache_frame_data=False,
        )

    def actualizar(self, frame):
        t = frame * 0.04

        # Leer valores actuales de los controles
        A = self.slider_A.val
        lam = self.slider_lam.val
        f = self.slider_f.val
        d_phi = self.slider_fase.val

        # Calcular magnitudes físicas derivadas (v = λ * f)
        k = 2 * np.pi / lam
        omega = 2 * np.pi * f
        v = lam * f

        # Onda 1 viajando hacia +x
        y1 = A * np.sin(k * self.x - omega * t)

        # Onda 2 según dirección seleccionada
        if self.radio_dir.value_selected == "Mismo sentido":
            y2 = A * np.sin(k * self.x - omega * t + d_phi)
        else:
            y2 = A * np.sin(k * self.x + omega * t + d_phi)

        # Principio de superposición
        y_total = y1 + y2

        # Actualizar curvas
        self.linea1.set_ydata(y1)
        self.linea2.set_ydata(y2)
        self.linea_res.set_ydata(y_total)

        # Actualizar texto de validación física en pantalla
        amp_max_obs = np.max(np.abs(y_total))
        self.lbl_datos.setText(
            f"Rapidez v = λ·f = {v:.2f} m/s  |  k = {k:.2f} rad/m  |  "
            f"ω = {omega:.2f} rad/s  |  Amplitud máx. resultante ≈ {amp_max_obs:.2f} m"
        )

        return (self.linea1, self.linea2, self.linea_res)

    def volver(self):
        self.close()
        if self.main_window is not None:
            self.main_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MOndas()
    ventana.show()
    sys.exit(app.exec())

    from modulo_ondas import MOndas

# Dentro de VentanaPrincipal:
def abrir_ondas(self):
    self.hide()
    self.ventana_ondas = MOndas(self)
    self.ventana_ondas.show()