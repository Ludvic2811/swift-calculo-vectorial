"""Sitio interactivo de Cálculo Vectorial: Satélite Swift.

Ejecutar: streamlit run app.py
Publicación: GitHub -> Streamlit Community Cloud.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

from modelo import (
    ALTURA_FINAL_KM,
    ALTURA_INICIAL_KM,
    K_S,
    MODELO_CONSTANTE,
    MODELO_CUASICIRCULAR,
    MU_TIERRA_KM3_S2,
    OMEGA0_RAD_S,
    PERIODO0_MIN,
    R0_KM,
    RADIO_TIERRA_KM,
    RF_KM,
    TIEMPO_150KM_S,
    TIEMPO_TOTAL_S,
    datos_para_csv,
    estado,
)

BASE = Path(__file__).resolve().parent

st.set_page_config(
    page_title="Swift | Laboratorio orbital · Cálculo Vectorial",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    .block-container{padding-top:1.65rem;max-width:1250px;padding-bottom:4rem}
    h1,h2,h3{letter-spacing:-.02em}
    .eyebrow{letter-spacing:.2em;color:#54d1fc;font-size:.77rem;font-weight:750}
    .app-hero{padding:1.4rem 0 .6rem}
    .app-hero h1{font-size:clamp(2rem,4vw,3.1rem);margin:.25rem 0 .5rem;line-height:1.1;color:#f2f8ff}
    .app-hero p{color:#a8bfd9;max-width:840px;line-height:1.7}
    .project-tag{display:inline-block;background:#123c4c;color:#8bead9;border:1px solid #225c65;padding:.3rem .67rem;border-radius:20px;font-size:.73rem;font-weight:650}
    div[data-testid='stMetric']{background:#11233b;border:1px solid #253d5b;border-radius:12px;padding:13px 16px}
    div[data-testid='stMetricLabel']{color:#c3d6eb}
    [data-testid='stTabs'] button p{font-weight:650}
    </style>
    <section class="app-hero">
      <div class="eyebrow">PROYECTO DE UNIDAD · CÁLCULO VECTORIAL</div>
      <h1>Movimiento orbital del satélite Swift</h1>
      <p>Explora una trayectoria en espiral, compara un modelo de velocidad angular constante
      con uno cuasicircular y verifica posiciones, velocidades y aceleraciones usando derivadas vectoriales.</p>
      <span class="project-tag">● Simulación educativa · 8 horas · 6371 km de radio terrestre</span>
    </section>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("📐 Parámetros del profesor")
    st.caption("Son fijos para que la entrega coincida con el enunciado.")
    st.write(f"**Radio terrestre:** {RADIO_TIERRA_KM:.0f} km")
    st.write(f"**Altura inicial:** {ALTURA_INICIAL_KM:.0f} km")
    st.write(f"**Altura final:** {ALTURA_FINAL_KM:.0f} km")
    st.write("**Tiempo simulado:** 8 h = 28 800 s")
    st.write(f"**μ terrestre:** {MU_TIERRA_KM3_S2:.2f} km³/s²")
    st.divider()
    st.write("**Constantes calculadas**")
    st.code(f"R0 = {R0_KM:.0f} km\nRf = {RF_KM:.0f} km\nk  = {K_S:.10e} s⁻¹\nω0 = {OMEGA0_RAD_S:.12f} rad/s")
    st.caption("El radio decrece exponencialmente en ambos modelos.")

tab_anim, tab_analisis, tab_formulas = st.tabs(
    ["🛰️ Simulación animada", "📈 Análisis y datos", "🧮 Desarrollo matemático"]
)

with tab_anim:
    st.caption("Presiona **Reproducir** y cambia entre los modelos. Cuando termine la fase orbital, puedes usar **☄ Reentrada** para mostrar el descenso final ilustrativo, con calentamiento y fragmentación visual.")
    config = {
        "R": RADIO_TIERRA_KM,
        "r0": R0_KM,
        "rf": RF_KM,
        "h0": ALTURA_INICIAL_KM,
        "k": K_S,
        "omega": OMEGA0_RAD_S,
        "mu": MU_TIERRA_KM3_S2,
        "T": TIEMPO_TOTAL_S,
    }
    html = (BASE / "assets" / "orbital_view.html").read_text(encoding="utf-8")
    html = html.replace("__SWIFT_CONFIG__", json.dumps(config, ensure_ascii=False))
    components.html(
        html,
        height=860,
        scrolling=False,
    )
    st.info(
        "La opción **6× o 12×** exagera solamente la separación radial en el dibujo, "
        "para hacer visible una caída de 155 km frente a un radio terrestre de 6371 km. "
        "Todos los valores numéricos siguen utilizando el modelo sin exageración. La fase de reentrada es una representación visual adicional para la entrega."
    )

with tab_analisis:
    st.subheader("Consulta precisa de posición, velocidad y aceleración")
    col_mode, col_time = st.columns([1, 2])
    with col_mode:
        selected_mode = st.radio(
            "Modelo a consultar",
            [MODELO_CONSTANTE, MODELO_CUASICIRCULAR],
            key="inspect_mode",
        )
    with col_time:
        minute = st.slider(
            "Tiempo de consulta (minutos)",
            min_value=0,
            max_value=480,
            value=240,
            step=5,
            help="240 minutos son exactamente cuatro horas.",
        )
    p = estado(float(minute * 60), selected_mode)
    st.caption("El tiempo de consulta de esta pestaña es independiente del reproductor animado.")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Altura", f"{p.altura_km:,.3f} km")
    m2.metric("Radio orbital", f"{p.radio_km:,.3f} km")
    m3.metric("Rapidez", f"{p.rapidez_km_s:,.6f} km/s")
    m4.metric("Aceleración total", f"{p.aceleracion_m_s2:,.6f} m/s²")

    st.markdown("#### Componentes de la aceleración")
    comps = pd.DataFrame(
        {
            "Componente": ["Radial (aᵣ)", "Transversal (aθ)", "Tangencial (aₜ)", "Normal (aₙ)"],
            "Valor (m/s²)": [p.ar_m_s2, p.atheta_m_s2, p.at_m_s2, p.an_m_s2],
            "Interpretación": [
                "Hacia el centro si es negativa",
                "Opuesta al giro si es negativa",
                "Cambio de rapidez (con signo)",
                "Cambio de dirección (magnitud)",
            ],
        }
    )
    st.dataframe(comps.style.format({"Valor (m/s²)": "{:+.8f}"}), hide_index=True, width="stretch")
    st.caption(
        f"Comprobación: √(aᵣ² + aθ²) = {p.aceleracion_m_s2:.8f} m/s²; "
        f"√(aₜ² + aₙ²) = {p.aceleracion_m_s2:.8f} m/s²."
    )

    st.markdown("#### Evolución durante las ocho horas")
    samples = [float(120 * i) for i in range(241)]
    curve_0 = [estado(t, MODELO_CONSTANTE) for t in samples]
    curve_1 = [estado(t, MODELO_CUASICIRCULAR) for t in samples]
    c1, c2 = st.columns(2)
    chart_config = dict(displaylogo=False, scrollZoom=False)

    def chart_series(metric: str, ylabel: str, selected: float) -> go.Figure:
        fig = go.Figure()
        for rows, name, color in (
            (curve_0, "ω constante", "#49ccff"),
            (curve_1, "Cuasicircular", "#ffbc65"),
        ):
            fig.add_trace(
                go.Scatter(
                    x=[q.t_h for q in rows],
                    y=[getattr(q, metric) for q in rows],
                    mode="lines",
                    line={"width": 3, "color": color},
                    name=name,
                    hovertemplate="Tiempo: %{x:.2f} h<br>Valor: %{y:.6f}<extra>%{fullData.name}</extra>",
                )
            )
        fig.add_vline(x=selected, line_dash="dot", line_color="#a7b7c8", opacity=0.8)
        fig.update_layout(
            height=350,
            margin=dict(l=20, r=10, t=28, b=18),
            paper_bgcolor="#0a162a",
            plot_bgcolor="#0a162a",
            font={"color": "#c3d6ea", "size": 12},
            legend={"orientation": "h", "y": 1.15, "x": 0},
            xaxis={"title": "Tiempo (horas)", "gridcolor": "#263754", "range": [0, 8]},
            yaxis={"title": ylabel, "gridcolor": "#263754"},
        )
        return fig

    with c1:
        st.plotly_chart(chart_series("rapidez_km_s", "Rapidez (km/s)", p.t_h),
                        width="stretch", config=chart_config)
    with c2:
        st.plotly_chart(chart_series("aceleracion_m_s2", "Aceleración total (m/s²)", p.t_h),
                        width="stretch", config=chart_config)

    st.markdown("#### Exportación para la entrega")
    dataframe = pd.DataFrame(datos_para_csv())
    st.download_button(
        "⬇️ Descargar CSV de los dos modelos (cada 2 minutos)",
        data=dataframe.to_csv(index=False).encode("utf-8-sig"),
        file_name="swift_resultados_ambos_modelos.csv",
        mime="text/csv",
        use_container_width=True,
    )

with tab_formulas:
    st.subheader("Ecuaciones utilizadas")
    st.markdown("**Datos del enunciado:** Rₜ = 6371 km, h₀ = 275 km, h₍f₎ = 120 km, T = 28 800 s y μ = 398600.44 km³/s².")
    st.latex(r"R_0=R_T+h_0=6646\ \mathrm{km},\quad R_f=R_T+h_f=6491\ \mathrm{km}")
    st.latex(r"k=\frac{\ln(R_0/R_f)}{T}=8.19394718\times10^{-7}\ \mathrm{s}^{-1}")
    st.latex(r"\omega_0=\sqrt{\frac{\mu}{R_0^3}}=0.001165274872\ \mathrm{rad/s}")
    st.latex(r"r(t)=R_0e^{-kt},\qquad r'(t)=-kr(t),\qquad r''(t)=k^2r(t)")
    st.markdown("**Modelo principal — velocidad angular constante:**")
    st.latex(r"\theta(t)=\omega_0t")
    st.latex(r"\vec{r}(t)=r(t)[\cos(\omega_0t)\hat\imath+\sin(\omega_0t)\hat\jmath]")
    st.latex(r"\vec{v}(t)=r(t)[(-k\cos\theta-\omega_0\sin\theta)\hat\imath+(-k\sin\theta+\omega_0\cos\theta)\hat\jmath]")
    st.latex(r"a_r=r(k^2-\omega_0^2),\qquad a_\theta=-2kr\omega_0")
    st.latex(r"|v|=r\sqrt{k^2+\omega_0^2},\qquad |a|=r(k^2+\omega_0^2)")
    st.latex(r"a_T=-kr\sqrt{k^2+\omega_0^2},\qquad a_N=r\omega_0\sqrt{k^2+\omega_0^2}")
    st.markdown("**Modelo cuasicircular — comparación didáctica:**")
    st.latex(r"\omega_c(t)=\sqrt{\frac{\mu}{r(t)^3}}=\omega_0 e^{3kt/2}")
    st.latex(r"\theta_c(t)=\frac{2\omega_0}{3k}\left(e^{3kt/2}-1\right)")
    st.latex(r"|v_c|=\sqrt{k^2r^2+\frac{\mu}{r}}")
    st.latex(r"a_r=k^2r-\frac{\mu}{r^2},\qquad a_\theta=-\frac12 kr\omega_c")
    st.caption(
        "En el modelo cuasicircular mantenemos r′ = −kr y usamos la velocidad angular "
        "de referencia circular. Por eso la trayectoria conserva una componente radial y no es una órbita circular exacta."
    )
    st.markdown("#### Parámetros y resultados de control")
    control = []
    for t in (0.0, 14400.0):
        p = estado(t, MODELO_CONSTANTE)
        control.append({
            "Tiempo": "0 h" if t == 0 else "4 h",
            "Radio (km)": p.radio_km,
            "Altura (km)": p.altura_km,
            "Rapidez (km/s)": p.rapidez_km_s,
            "|a| (m/s²)": p.aceleracion_m_s2,
            "aᵣ (m/s²)": p.ar_m_s2,
            "aθ (m/s²)": p.atheta_m_s2,
            "aₜ (m/s²)": p.at_m_s2,
            "aₙ (m/s²)": p.an_m_s2,
        })
    st.dataframe(pd.DataFrame(control).style.format(precision=6), hide_index=True, width="stretch")
    st.success(
        f"Periodo inicial: **{PERIODO0_MIN:.4f} minutos**. "
        f"Altura de 150 km alcanzada a las **{TIEMPO_150KM_S / 3600:.4f} horas** "
        f"({TIEMPO_150KM_S:.2f} s)."
    )


st.divider()
st.caption(
    "SWIFT · LABORATORIO ORBITAL | Parámetros derivados del proyecto de Cálculo Vectorial. "
    "Simulación independiente de propósito educativo; no afiliada a NASA ni al proyecto científico Swift."
)
