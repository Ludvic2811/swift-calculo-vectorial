# 🛰️ Swift · Laboratorio orbital

**Proyecto de Unidad 3 — Cálculo Vectorial**  
**Simulación animada en Streamlit, lista para publicar gratis.**

Esta aplicación reproduce **las ecuaciones del proyecto didáctico** de descenso orbital de Swift y permite comparar dos aproximaciones: velocidad angular constante y modelo cuasicircular. **No es un modelo físico real de reentrada**, ni una aplicación oficial del observatorio Swift.

## Lo que incluye

- Animación 2D de la Tierra, la espiral y un satélite con controles de reproducción, pausa, reinicio, tiempo y velocidad.
- Dos modos: **ω constante** (el modelo principal del proyecto) y **cuasicircular** (comparación).
- Opción de **escala radial ilustrativa** (1×, 6×, 12×). Los cálculos se realizan siempre con las distancias físicas reales.
- Indicadores sincronizados de altura, rapidez y aceleración dentro del reproductor animado.
- Gráficas comparativas y consulta exacta para los ejercicios 13, 14 y 15.
- Tabla con las cuatro componentes de la aceleración y comprobación de magnitudes.
- Exportación de datos en formato CSV y apartado de fórmulas.
- Pruebas automatizadas de consistencia matemática en `tests/test_modelo.py`.

## Archivos importantes

```text
swift_streamlit/
├── app.py                     # Interfaz de Streamlit (archivo principal)
├── modelo.py                  # Ecuaciones y cálculos físicos/matemáticos
├── requirements.txt           # Dependencias para Cloud
├── assets/
│   └── orbital_view.html      # Animación HTML + JavaScript integrada
├── .streamlit/
│   └── config.toml            # Diseño oscuro
├── demo_animacion.html         # Vista previa sin instalar Python
├── tests/
│   └── test_modelo.py         # Pruebas matemáticas
└── README.md                  # Estas instrucciones
```

## 1. Probar en Windows (PowerShell o CMD)

1. Descomprime el archivo ZIP.
2. Abre una terminal dentro de la carpeta `swift_streamlit` (donde está `app.py`).
3. Ejecuta, en este orden:

```powershell
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

La dirección local aparecerá en la terminal (usualmente `http://localhost:8501`).

Si tienes Python instalado con el comando `python` en vez de `py`, sustituye `py` por `python`.

## 2. Publicar gratis con Streamlit Community Cloud

El código no necesita servidor pagado ni claves API.

1. En [GitHub](https://github.com/), crea un **repositorio público** nuevo, por ejemplo `swift-calculo-vectorial`.
2. **Descomprime el ZIP y sube sus archivos y carpetas** a la raíz del repositorio. **No subas solamente el ZIP**. Deben conservarse `assets/orbital_view.html`, `app.py`, `modelo.py`, `requirements.txt` y `.streamlit/config.toml`.
3. Ingresa a [Streamlit Community Cloud](https://share.streamlit.io/) con tu cuenta vinculada a GitHub.
4. Selecciona **Create app** → **Yup, I have an app**.
5. Selecciona tu repositorio y rama (`main`). En **Main file path** escribe `app.py`.
6. Selecciona **Deploy**. Tras publicarse, obtendrás una URL bajo `streamlit.app` que podrás agregar a tu entrega.

Referencia oficial: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy

> La publicación depende de tus cuentas y permisos de GitHub/Streamlit. **El ZIP entregado no implica que el sitio ya esté publicado**.

## 3. Datos exactos del enunciado

| Dato | Valor |
|---|---:|
| Radio de la Tierra | 6371 km |
| Altura inicial | 275 km |
| Altura final | 120 km |
| Radio orbital inicial | 6646 km |
| Radio orbital final | 6491 km |
| Tiempo total | 8 h = 28 800 s |
| μ | 398600.44 km³/s² |
| k | 8.193947180927438 × 10⁻⁷ s⁻¹ |
| ω₀ | 0.0011652748721205871 rad/s |
| Periodo inicial | 89.8669984 min |
| Tiempo para 150 km | 6.43680807 horas |

**Referencia, velocidad angular constante:**

| Magnitud | Inicio | 4 h |
|---|---:|---:|
| Radio (km) | 6646.000000 | 6568.042783 |
| Altura (km) | 275.000000 | 197.042783 |
| Rapidez (km/s) | 7.744419 | 7.653577 |
| Aceleración total (m/s²) | 9.024379 | 8.918523 |
| Aceleración radial (m/s²) | -9.024370 | -8.918514 |
| Aceleración transversal (m/s²) | -0.012691 | -0.012543 |
| Aceleración tangencial (m/s²) | -0.006346 | -0.006271 |
| Aceleración normal (m/s²) | 9.024377 | 8.918521 |

## 4. Cómo se construyó el modelo cuasicircular

Para comparar sin modificar la pérdida de altura que da el profesor, se mantiene
`r(t) = R₀ exp(-kt)` y se utiliza `ω(t) = √(μ / r(t)³)`.

Como `θ'(t)=ω(t)`, la posición utiliza la integral:

`θ(t) = [2ω₀/(3k)] [exp(3kt/2) − 1]`.

La magnitud de la velocidad es `√(k²r² + μ/r)`; aumenta gradualmente a medida que disminuye el radio.

Este es un **modelo didáctico cuasicircular**: el satélite todavía tiene velocidad radial `r'=-kr` y no se ha integrado una dinámica completa bajo gravedad y arrastre.

## 5. Limitaciones que debes declarar en tu presentación

- El PDF del profesor llama al modelo una aproximación de clase, no una reconstrucción de reentrada.
- El dibujo amplía las diferencias radiales a voluntad (puedes seleccionar 1× para escala real).
- Las flechas `v` y `a` señalan su **dirección**, pero no son longitudes vectoriales a escala.
- No se calculan **temperaturas**, **calentamiento aerodinámico**, **fricción atmosférica**, **ablación** ni **fragmentación**.
- Si el profesor exige comprobar visualmente el calentamiento en *su simulador Swift*, esa parte queda pendiente y no debe afirmarse que ya se comprobó.
- La simulación **complementa, no sustituye**, las operaciones manuscritas que solicita el proyecto.

## 6. Pruebas opcionales

Si tienes `pytest` instalado:

```powershell
py -m pip install pytest
py -m pytest -q
```

---

Desarrollo para fines educativos. Sin servicios de pago ni recursos externos de la NASA.
