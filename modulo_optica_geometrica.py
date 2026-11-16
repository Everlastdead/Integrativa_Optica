import sys
import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.widgets import Slider
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLabel,
    QGridLayout,
    QHBoxLayout,
    QDoubleSpinBox
)


class GeoOp(QWidget):
    def __init__(self, main_window=None):
        super().__init__()

        self.main_window = main_window
        self.setWindowTitle("Módulo B: Óptica Geométrica (Reflexión y Refracción)")
        self.resize(900, 680)

        layout = QGridLayout()

        # Botón para regresar al menú principal
        btn_volver = QPushButton("Regresar al principio")
        btn_volver.clicked.connect(self.volver)

        # Etiqueta superior para validación numérica en tiempo real (Pruebas 3, 4 y 5)
        self.lbl_datos = QLabel()
        self.lbl_datos.setStyleSheet("font-weight: bold; font-size: 13px; padding: 4px;")

        # Configuración de la figura embebida en PySide6
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.fig.subplots_adjust(bottom=0.30)
        self.canvas = FigureCanvasQTAgg(self.fig)

        # 1. Parámetros iniciales (Prueba 4: n1=1.0, n2=1.5, θi=30°)
        self.theta_i_init = 30.0
        self.n1_init = 1.0
        self.n2_init = 1.5

        # 2. Dibujar elementos estáticos de la interfaz óptica
        self.ax.axhspan(0, 1.5, color="#e8f4f8", alpha=0.5, label="Medio 1 ($n_1$)")
        self.ax.axhspan(-1.5, 0, color="#d0e1f9", alpha=0.6, label="Medio 2 ($n_2$)")
        self.ax.axhline(0, color="black", linewidth=1.8, label="Interfaz plana")
        self.ax.axvline(0, color="gray", linestyle="--", linewidth=1.2, label="Normal")

        # Inicializar las líneas de los 3 rayos
        (self.rayo_inc,) = self.ax.plot([], [], color="red", linewidth=2.2, label="Rayo Incidente ($\\theta_i$)")
        (self.rayo_ref,) = self.ax.plot([], [], color="orange", linewidth=2.0, linestyle="-.", label="Rayo Reflejado ($\\theta_r$)")
        (self.rayo_tra,) = self.ax.plot([], [], color="blue", linewidth=2.2, label="Rayo Refractado ($\\theta_t$)")

        self.ax.set_xlim(-1.2, 1.2)
        self.ax.set_ylim(-1.2, 1.2)
        self.ax.set_aspect("equal")
        self.ax.set_xlabel("Posición horizontal x")
        self.ax.set_ylabel("Posición vertical y")
        self.ax.set_title("Simulación de Reflexión, Ley de Snell y Reflexión Total Interna")
        self.ax.grid(True, linestyle=":", alpha=0.6)
        self.ax.legend(loc="upper right", fontsize=8)

        # 3. Ejes para los deslizadores interactivos
        ax_theta = self.fig.add_axes([0.28, 0.17, 0.58, 0.03])
        ax_n1 = self.fig.add_axes([0.28, 0.11, 0.58, 0.03])
        ax_n2 = self.fig.add_axes([0.28, 0.05, 0.58, 0.03])

        # 4. Instanciación de Sliders
        self.slider_theta = Slider(ax_theta, "Ángulo incidencia θi (°)", 0.0, 89.0, valinit=self.theta_i_init)
        self.slider_n1 = Slider(ax_n1, "Índice Medio 1 (n1)", 1.0, 2.5, valinit=self.n1_init)
        self.slider_n2 = Slider(ax_n2, "Índice Medio 2 (n2)", 1.0, 2.5, valinit=self.n2_init)

        # 5. Panel de entrada manual precisa (QDoubleSpinBox)
        panel_manual = QHBoxLayout()

        self.spin_theta = self._crear_spinbox(0.0, 89.0, 0.5, self.theta_i_init, " °", decimales=2)
        self.spin_n1 = self._crear_spinbox(1.0, 2.5, 0.05, self.n1_init, "", decimales=3)
        self.spin_n2 = self._crear_spinbox(1.0, 2.5, 0.05, self.n2_init, "", decimales=3)

        panel_manual.addWidget(QLabel("Ángulo θi:"))
        panel_manual.addWidget(self.spin_theta)
        panel_manual.addWidget(QLabel("Índice n1:"))
        panel_manual.addWidget(self.spin_n1)
        panel_manual.addWidget(QLabel("Índice n2:"))
        panel_manual.addWidget(self.spin_n2)

        # 6. Sincronización bidireccional (Slider <-> SpinBox)
        self.slider_theta.on_changed(self._on_slider_changed)
        self.slider_n1.on_changed(self._on_slider_changed)
        self.slider_n2.on_changed(self._on_slider_changed)

        self.spin_theta.valueChanged.connect(lambda val: self.slider_theta.set_val(val))
        self.spin_n1.valueChanged.connect(lambda val: self.slider_n1.set_val(val))
        self.spin_n2.valueChanged.connect(lambda val: self.slider_n2.set_val(val))

        # Ubicar widgets en el layout de PySide6
        layout.addWidget(btn_volver, 0, 0)
        layout.addWidget(self.lbl_datos, 0, 1, 1, 2)
        layout.addLayout(panel_manual, 1, 0, 1, 3)
        layout.addWidget(self.canvas, 2, 0, 3, 3)
        self.setLayout(layout)

        # Ejecutar primer cálculo y dibujo
        self.actualizar_simulacion()

    def _crear_spinbox(self, minimo, maximo, paso, valor_init, sufijo, decimales=2):
        spin = QDoubleSpinBox()
        spin.setRange(minimo, maximo)
        spin.setSingleStep(paso)
        spin.setDecimals(decimales)
        spin.setValue(valor_init)
        spin.setSuffix(sufijo)
        return spin

    def _on_slider_changed(self, val):
        # Sincronizar los spinboxes sin disparar eventos recursivos
        for spin, slider in (
            (self.spin_theta, self.slider_theta),
            (self.spin_n1, self.slider_n1),
            (self.spin_n2, self.slider_n2),
        ):
            spin.blockSignals(True)
            spin.setValue(slider.val)
            spin.blockSignals(False)

        self.actualizar_simulacion()

    def actualizar_simulacion(self):
        theta_i_deg = self.slider_theta.val
        n1 = self.slider_n1.val
        n2 = self.slider_n2.val

        theta_i_rad = np.radians(theta_i_deg)
        L = 1.1

        # 1. Rayo Incidente
        x_inc = [-L * np.sin(theta_i_rad), 0.0]
        y_inc = [L * np.cos(theta_i_rad), 0.0]
        self.rayo_inc.set_data(x_inc, y_inc)

        # 2. Ley de Reflexión: θr = θi
        theta_r_deg = theta_i_deg
        x_ref = [0.0, L * np.sin(theta_i_rad)]
        y_ref = [0.0, L * np.cos(theta_i_rad)]
        self.rayo_ref.set_data(x_ref, y_ref)

        # 3. Cálculo de Ángulo Crítico (si n1 > n2)
        if n1 > n2:
            theta_c_deg = np.degrees(np.arcsin(n2 / n1))
            texto_critico = f"θc = {theta_c_deg:.2f}°"
        else:
            theta_c_deg = None
            texto_critico = "No existe θc (n1 ≤ n2)"

        # 4. Ley de Snell: n1 * sin(θi) = n2 * sin(θt)
        sin_theta_t = (n1 / n2) * np.sin(theta_i_rad)

        if sin_theta_t <= 1.0:
            theta_t_rad = np.arcsin(sin_theta_t)
            theta_t_deg = np.degrees(theta_t_rad)

            x_tra = [0.0, L * np.sin(theta_t_rad)]
            y_tra = [0.0, -L * np.cos(theta_t_rad)]
            self.rayo_tra.set_data(x_tra, y_tra)

            estado_texto = f"θt = {theta_t_deg:.2f}°  |  {texto_critico}"
        else:
            self.rayo_tra.set_data([], [])
            estado_texto = f"¡REFLEXIÓN TOTAL INTERNA! (θi > {texto_critico})"

        self.lbl_datos.setText(
            f"θi = {theta_i_deg:.2f}°  |  θr = {theta_r_deg:.2f}°  |  {estado_texto}"
        )

        self.canvas.draw_idle()

    def volver(self):
        self.close()
        if self.main_window is not None:
            self.main_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = GeoOp()
    ventana.show()
    sys.exit(app.exec())