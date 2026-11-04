import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider


def ejecutar():
    # 1. Parámetros iniciales del modelo físico
    A_init = 1.0
    lam_init = 2.0
    f_init = 1.0

    k_init = 2 * np.pi / lam_init
    omega_init = 2 * np.pi * f_init

    # 2. Creación de la malla espacial
    x = np.linspace(0, 8.0, 500)
    y = A_init * np.sin(k_init * x)

    # 3. Configuración de la figura y ejes principales
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.25)  # Deja espacio inferior para los deslizadores[cite: 2]
    
    linea, = ax.plot(x, y)
    ax.set_ylim(-2.0, 2.0)
    ax.grid(True)

    # 4. Creación de ejes específicos para cada deslizador
    ax_amp = fig.add_axes([0.25, 0.15, 0.60, 0.03])
    ax_lam = fig.add_axes([0.25, 0.09, 0.60, 0.03])
    ax_freq = fig.add_axes([0.25, 0.03, 0.60, 0.03])

    # 5. Instanciación de los Sliders
    slider_A = Slider(ax_amp, "Amplitud (m)", 0.1, 1.5, valinit=A_init)
    slider_lam = Slider(ax_lam, "Longitud de onda", 1.0, 4.0, valinit=lam_init)
    slider_f = Slider(ax_freq, "Frecuencia (Hz)", 0.5, 5.0, valinit=f_init)

    # 6. Función de actualización integrada (Animación + Sliders)
    def actualizar(frame):
        t = frame * 0.04
        
        # Leer valores actuales de los deslizadores
        A_actual = slider_A.val
        f_actual = slider_f.val
        lam_actual = slider_lam.val

        # Recalcular constantes físicas
        k_actual = 2 * np.pi / lam_actual
        omega_actual = 2 * np.pi * f_actual

        # Calcular nuevo perfil de onda
        y_actual = A_actual * np.sin(k_actual * x - omega_actual * t)
        
        # Actualizar la gráfica
        linea.set_ydata(y_actual)
        return linea,

    # 7. Ejecución de la animación interactiva
    animacion = FuncAnimation(
        fig,
        actualizar,
        frames=200,
        interval=40,
        blit=False,
        cache_frame_data=False
    )

    plt.show()


if __name__ == "__main__":
    ejecutar()