import math

from modelo import (
    K_S,
    MODELO_CONSTANTE,
    MODELO_CUASICIRCULAR,
    OMEGA0_RAD_S,
    PERIODO0_MIN,
    RF_KM,
    R0_KM,
    TIEMPO_150KM_S,
    TIEMPO_TOTAL_S,
    estado,
)


def test_parametros_proyecto():
    assert R0_KM == 6646
    assert RF_KM == 6491
    assert math.isclose(K_S, 8.193947180927438e-7, rel_tol=1e-12)
    assert math.isclose(OMEGA0_RAD_S, 0.0011652748721205871, rel_tol=1e-12)
    assert math.isclose(PERIODO0_MIN, 89.8669984439714, rel_tol=1e-12)
    assert math.isclose(TIEMPO_150KM_S / 3600, 6.436808069719359, rel_tol=1e-12)


def test_constante_inicio_y_4h():
    a = estado(0, MODELO_CONSTANTE)
    b = estado(14400, MODELO_CONSTANTE)
    assert math.isclose(a.rapidez_km_s, 7.7444187147582655, rel_tol=1e-11)
    assert math.isclose(b.rapidez_km_s, 7.6535771062894975, rel_tol=1e-11)
    assert math.isclose(a.aceleracion_m_s2, 9.024378758576296, rel_tol=1e-11)
    assert math.isclose(b.aceleracion_m_s2, 8.918523288714082, rel_tol=1e-11)
    assert a.ar_m_s2 < 0 and b.atheta_m_s2 < 0 and a.at_m_s2 < 0
    assert math.isclose(math.hypot(a.ar_m_s2, a.atheta_m_s2), a.aceleracion_m_s2, rel_tol=1e-12)


def test_cuasicircular_aumenta_rapidez():
    a, b, c = (estado(t, MODELO_CUASICIRCULAR) for t in [0, 14400, 28800])
    assert a.rapidez_km_s < b.rapidez_km_s < c.rapidez_km_s
    assert math.isclose(b.rapidez_km_s, 7.790242986142753, rel_tol=1e-11)
    assert a.at_m_s2 > 0 and b.at_m_s2 > 0
    assert math.isclose(c.radio_km, RF_KM, rel_tol=1e-12)


def test_via_polares_y_cartesianas_coinciden():
    for mode in (MODELO_CONSTANTE, MODELO_CUASICIRCULAR):
        for t in (0, 4800, 14400, 24500, TIEMPO_TOTAL_S):
            p = estado(t, mode)
            assert math.isclose(math.hypot(p.vx_km_s, p.vy_km_s), p.rapidez_km_s, rel_tol=1e-12)
            assert math.isclose(math.hypot(p.ax_m_s2, p.ay_m_s2), p.aceleracion_m_s2, rel_tol=1e-12)
            assert math.isclose(math.hypot(p.ar_m_s2, p.atheta_m_s2), p.aceleracion_m_s2, rel_tol=1e-12)
            assert math.isclose(math.hypot(p.at_m_s2, p.an_m_s2), p.aceleracion_m_s2, rel_tol=1e-12)
