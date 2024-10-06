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

## Uso

Para ejecutar el proyecto, abre una IDE compatible con Python y especifica la carpeta principal que contiene las subcarpetas con el conjunto de videos.

## Contribuciones
Las contribuciones son bienvenidas. Si deseas colaborar, por favor sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (git checkout -b feature/nueva-caracteristica).
3. Realiza tus cambios y confírmalos (git commit -m 'Agregada nueva característica').
4. Haz push a la rama (git push origin feature/nueva-caracteristica).
5. Crea un nuevo Pull Request.

## Agradecimientos
Queremos agradecer a todos aquellos que han contribuido con su tiempo y esfuerzo al desarrollo de este proyecto. Su apoyo y dedicación han sido fundamentales para su éxito.

**TRABAJO HECHO POR SANTIAGO RIVERA ESTRADA, ESTUDIANTE DE BIOINGENIERÍA**  
**ASESORES:** JULIANA MORENO Y JOHN FREDY OCHOA, PROFESORES DE BIOINGENIERÍA.  
**NEUROCO (GRUPO DE NEUROCIENCIAS COMPUTACIONALES) - UNIVERSIDAD DE ANTIOQUIA - MEDELLÍN, COLOMBIA.**
