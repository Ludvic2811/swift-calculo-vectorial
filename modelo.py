"""Modelo matemático del proyecto Swift de Cálculo Vectorial.

Unidades: km, s, km/s y km/s² salvo indicación contraria.
La trayectoria es didáctica, NO una predicción real de reentrada.
"""

from dataclasses import asdict, dataclass
from math import cos, exp, expm1, hypot, log, pi, sin, sqrt

RADIO_TIERRA_KM = 6371.0
ALTURA_INICIAL_KM = 275.0
ALTURA_FINAL_KM = 120.0
TIEMPO_TOTAL_S = 8.0 * 3600.0
MU_TIERRA_KM3_S2 = 398600.44

R0_KM = RADIO_TIERRA_KM + ALTURA_INICIAL_KM
RF_KM = RADIO_TIERRA_KM + ALTURA_FINAL_KM
K_S = log(R0_KM / RF_KM) / TIEMPO_TOTAL_S
OMEGA0_RAD_S = sqrt(MU_TIERRA_KM3_S2 / R0_KM**3)
PERIODO0_MIN = (2 * pi / OMEGA0_RAD_S) / 60
TIEMPO_150KM_S = log(R0_KM / (RADIO_TIERRA_KM + 150.0)) / K_S

MODELO_CONSTANTE = "Velocidad angular constante"
MODELO_CUASICIRCULAR = "Cuasicircular"


@dataclass(frozen=True)
class Estado:
    t_s: float
    t_h: float
    radio_km: float
    altura_km: float
    angulo_rad: float
    omega_rad_s: float
    x_km: float
    y_km: float
    vx_km_s: float
    vy_km_s: float
    ax_m_s2: float
    ay_m_s2: float
    rapidez_km_s: float
    aceleracion_m_s2: float
    ar_m_s2: float
    atheta_m_s2: float
    at_m_s2: float
    an_m_s2: float


def estado(t_s: float, modelo: str = MODELO_CONSTANTE) -> Estado:
    """Evalúa la posición, velocidad y aceleración sin alterar parámetros."""
    if not 0 <= t_s <= TIEMPO_TOTAL_S:
        raise ValueError("El tiempo debe estar entre 0 y 28800 segundos.")
    if modelo not in (MODELO_CONSTANTE, MODELO_CUASICIRCULAR):
        raise ValueError(f"Modelo desconocido: {modelo}")

    radio = R0_KM * exp(-K_S * t_s)
    radio_p = -K_S * radio
    radio_pp = K_S**2 * radio
    if modelo == MODELO_CONSTANTE:
        omega = OMEGA0_RAD_S
        theta = OMEGA0_RAD_S * t_s
        omega_p = 0.0
    else:
        # Modelo cuasicircular: omega(t)=sqrt(mu/r(t)^3).
        # La velocidad radial -kr se conserva; no se impone órbita circular exacta.
        omega = sqrt(MU_TIERRA_KM3_S2 / radio**3)
        theta = (2 * OMEGA0_RAD_S / (3 * K_S)) * expm1(1.5 * K_S * t_s)
        omega_p = 1.5 * K_S * omega

    c, s = cos(theta), sin(theta)
    x, y = radio * c, radio * s
    v_r, v_th = radio_p, radio * omega
    vx, vy = v_r * c - v_th * s, v_r * s + v_th * c
    a_r = radio_pp - radio * omega**2
    a_th = radio * omega_p + 2 * radio_p * omega
    ax, ay = a_r * c - a_th * s, a_r * s + a_th * c
    rapidez = hypot(vx, vy)
    magnitud_a = hypot(ax, ay)
    a_t = (vx * ax + vy * ay) / rapidez
    a_n = sqrt(max(0.0, magnitud_a**2 - a_t**2))

    return Estado(
        t_s=t_s,
        t_h=t_s / 3600.0,
        radio_km=radio,
        altura_km=radio - RADIO_TIERRA_KM,
        angulo_rad=theta,
        omega_rad_s=omega,
        x_km=x,
        y_km=y,
        vx_km_s=vx,
        vy_km_s=vy,
        ax_m_s2=ax * 1000,
        ay_m_s2=ay * 1000,
        rapidez_km_s=rapidez,
        aceleracion_m_s2=magnitud_a * 1000,
        ar_m_s2=a_r * 1000,
        atheta_m_s2=a_th * 1000,
        at_m_s2=a_t * 1000,
        an_m_s2=a_n * 1000,
    )


def datos_para_csv(paso_s: int = 120) -> list[dict]:
    """Dos modelos, tiempos iguales: exportación comparativa."""
    rows = []
    for modo in (MODELO_CONSTANTE, MODELO_CUASICIRCULAR):
        for t in range(0, int(TIEMPO_TOTAL_S) + 1, paso_s):
            row = asdict(estado(float(t), modo))
            rows.append({"modelo": modo, **row})
    return rows
