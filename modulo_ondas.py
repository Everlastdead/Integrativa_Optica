import sys
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, RadioButtons
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLabel,
    QGridLayout,
    QHBoxLayout,
    QDoubleSpinBox
)


class MOndas(QWidget):
    def __init__(self, main_window=None):
        super().__init__()

        self.main_window = main_window
        self.setWindowTitle("Módulo A: Ondas y Superposición")
        self.resize(900, 680)

        layout = QGridLayout()

        # Botón para regresar al menú principal
        btn_volver = QPushButton("Regresar al principio")
        btn_volver.clicked.connect(self.volver)

        # Etiqueta para mostrar los cálculos físicos en tiempo real (Pruebas 1 y 2)
        self.lbl_datos = QLabel()
        self.lbl_datos.setStyleSheet("font-weight: bold; font-size: 13px; padding: 4px;")

        # Configuración de la figura embebida en PySide6
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.fig.subplots_adjust(bottom=0.36)
        self.canvas = FigureCanvasQTAgg(self.fig)

        # 1. Parámetros iniciales configurados para Prueba 1 (v = 4 m/s, f = 2 Hz -> λ = 2 m)
        self.A_init = 1.0
        self.v_init = 4.0
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
        ax_vel = self.fig.add_axes([0.30, 0.17, 0.55, 0.03])
        ax_freq = self.fig.add_axes([0.30, 0.11, 0.55, 0.03])
        ax_fase = self.fig.add_axes([0.30, 0.05, 0.55, 0.03])
        ax_dir = self.fig.add_axes([0.03, 0.05, 0.16, 0.18])

        # 4. Instanciación de Sliders y RadioButtons
        self.slider_A = Slider(ax_amp, "Amplitud A (m)", 0.1, 1.5, valinit=self.A_init)
        self.slider_v = Slider(ax_vel, "Rapidez v (m/s)", 1.0, 10.0, valinit=self.v_init)
        self.slider_f = Slider(ax_freq, "Frecuencia f (Hz)", 0.5, 5.0, valinit=self.f_init)
        self.slider_fase = Slider(ax_fase, "Desfase Δφ (rad)", 0.0, 2 * np.pi, valinit=self.fase_init)
        self.radio_dir = RadioButtons(ax_dir, ("Mismo sentido", "Sentido opuesto"))

        # 5. Panel de entrada manual precisa (QDoubleSpinBox)
        panel_manual = QHBoxLayout()

        self.spin_A = self._crear_spinbox(0.1, 1.5, 0.05, self.A_init, " m")
        self.spin_v = self._crear_spinbox(1.0, 10.0, 0.1, self.v_init, " m/s")
        self.spin_f = self._crear_spinbox(0.5, 5.0, 0.1, self.f_init, " Hz")
        self.spin_fase = self._crear_spinbox(0.0, round(2 * np.pi, 4), 0.05, self.fase_init, " rad", decimales=4)

        panel_manual.addWidget(QLabel("A(m):"))
        panel_manual.addWidget(self.spin_A)
        panel_manual.addWidget(QLabel("v (m/s):"))
        panel_manual.addWidget(self.spin_v)
        panel_manual.addWidget(QLabel("f (Hz):"))
        panel_manual.addWidget(self.spin_f)
        panel_manual.addWidget(QLabel("Δφ (rad):"))
        panel_manual.addWidget(self.spin_fase)

        # 6. Sincronización bidireccional (Slider <-> SpinBox)
        self.slider_A.on_changed(lambda val: self._sync_spin(self.spin_A, val))
        self.slider_v.on_changed(lambda val: self._sync_spin(self.spin_v, val))
        self.slider_f.on_changed(lambda val: self._sync_spin(self.spin_f, val))
        self.slider_fase.on_changed(lambda val: self._sync_spin(self.spin_fase, val))

        self.spin_A.valueChanged.connect(lambda val: self.slider_A.set_val(val))
        self.spin_v.valueChanged.connect(lambda val: self.slider_v.set_val(val))
        self.spin_f.valueChanged.connect(lambda val: self.slider_f.set_val(val))
        self.spin_fase.valueChanged.connect(lambda val: self.slider_fase.set_val(val))

        # Ubicar widgets en el layout de PySide6
        layout.addWidget(btn_volver, 0, 0)
        layout.addWidget(self.lbl_datos, 0, 1, 1, 2)
        layout.addLayout(panel_manual, 1, 0, 1, 3)
        layout.addWidget(self.canvas, 2, 0, 3, 3)
        self.setLayout(layout)

        # 7. Guardar la animación en self para mantenerla en memoria
        self.animacion = FuncAnimation(
            self.fig,
            self.actualizar,
            frames=200,
            interval=40,
            blit=False,
            cache_frame_data=False,
        )

    def _crear_spinbox(self, minimo, maximo, paso, valor_init, sufijo, decimales=2):
        spin = QDoubleSpinBox()
        spin.setRange(minimo, maximo)
        spin.setSingleStep(paso)
        spin.setDecimals(decimales)
        spin.setValue(valor_init)
        spin.setSuffix(sufijo)
        return spin

    def _sync_spin(self, spinbox, valor):
        spinbox.blockSignals(True)
        spinbox.setValue(valor)
        spinbox.blockSignals(False)

    def actualizar(self, frame):
        t = frame * 0.04

        A = self.slider_A.val
        v = self.slider_v.val
        f = self.slider_f.val
        d_phi = self.slider_fase.val

        # Calcular magnitudes físicas derivadas (λ = v / f)
        lam = v / f
        k = 2 * np.pi / lam
        omega = 2 * np.pi * f

        y1 = A * np.sin(k * self.x - omega * t)

        if self.radio_dir.value_selected == "Mismo sentido":
            y2 = A * np.sin(k * self.x - omega * t + d_phi)
        else:
            y2 = A * np.sin(k * self.x + omega * t + d_phi)

        y_total = y1 + y2

        self.linea1.set_ydata(y1)
        self.linea2.set_ydata(y2)
        self.linea_res.set_ydata(y_total)

        amp_max_obs = np.max(np.abs(y_total))
        self.lbl_datos.setText(
            f"Long. onda λ = v/f = {lam:.2f} m  |  k = {k:.2f} rad/m  |  "
            f"ω = {omega:.2f} rad/s  |  Amplitud máx. resultante ≈ {amp_max_obs:.2f} m"
        )

        return (self.linea1, self.linea2, self.linea_res)

    def volver(self):
        self.animacion.event_source.stop()
        self.close()
        if self.main_window is not None:
            self.main_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MOndas()
    ventana.show()
    sys.exit(app.exec())