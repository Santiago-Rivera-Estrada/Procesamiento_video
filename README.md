# Procesamiento de Videos para Detección de Poses y Cálculo de Ángulos

## Descripción

Este proyecto está orientado al procesamiento de videos utilizando técnicas de visión por computadora y la biblioteca **Mediapipe** para detectar poses humanas y calcular ángulos en movimientos específicos (hombro, codo, muñeca). Los resultados son analizados para extraer métricas como la trayectoria y velocidad angular, y se almacenan en archivos CSV para su posterior análisis.

---

## Características
- 🧍‍♂️ **Detección de poses**: Usa Mediapipe para identificar puntos clave del cuerpo en los videos.
- 📐 **Cálculo de ángulos**: Calcula el ángulo entre el hombro, codo y muñeca, permitiendo el análisis del movimiento.
- 📊 **Trayectorias**: Obtiene y grafica las trayectorias de los puntos relevantes del cuerpo.
- 🕐 **Velocidad angular**: Calcula la velocidad angular a partir de los ángulos detectados.
- 💾 **Resultados**: Almacena los datos en archivos CSV y genera gráficas para visualización de los resultados.

---

## Requisitos
- Python 3.7+
- OpenCV
- Numpy
- Matplotlib
- Pandas
- Mediapipe

### Instalación de dependencias

```bash
pip install opencv-python numpy matplotlib pandas mediapipe
