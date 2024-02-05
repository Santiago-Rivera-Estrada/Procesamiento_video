# Importar las bibliotecas necesarias
import sys # La biblioteca sys ofrece funciones para interactuar con el sistema operativo
sys.path.append("C:/Users/santi/Downloads/Procesamiento_video") # Añadir la ruta donde se encuentra el archivo DeteccionCodoEFpy.py al sistema
import cv2 as cv # OpenCV es una biblioteca de visión por computadora que ofrece funciones para procesar imágenes y videos
import Modulo_EF_Codo as DC # Importar el archivo DeteccionCodoEFpy como DC, que contiene la clase Detector_Pose
import time # La biblioteca time ofrece funciones para medir el tiempo
import numpy as np # NumPy es una biblioteca para trabajar con matrices y operaciones numéricas

# Crear un objeto de la clase VideoCapture de OpenCV, que permite capturar imágenes de un video o una cámara
cap = cv.VideoCapture("C:/Users/santi/Downloads/Procesamiento_video/video1.mp4") # Pasar la ruta del video como argumento
# Crear un objeto de la clase Detector_Pose que definiste anteriormente
detector = DC.Detector_Pose()
# Inicializar una variable para almacenar el tiempo previo
ptime=0
# Inicializar una variable para contar el número de repeticiones
contador=0
# Inicializar una variable para indicar la dirección del movimiento del codo (0: bajando, 1: subiendo)
dir=0
# Crear un bucle infinito para procesar cada fotograma del video
while True:
    # Leer el fotograma actual del video y almacenar si se leyó correctamente y la imagen
    success, img = cap.read()
    # Redimensionar la imagen antes de procesarla, usando la función resize de OpenCV, que recibe la imagen, el tamaño deseado y el método de interpolación
    img = cv.resize(img, (400, 400), interpolation=cv.INTER_AREA)
    # Obtener el tiempo actual en segundos
    ctime = time.time()
    # Calcular los fotogramas por segundo (fps) dividiendo 1 por la diferencia entre el tiempo actual y el tiempo previo
    fps = 1 / (ctime - ptime)
    # Actualizar el tiempo previo con el tiempo actual
    ptime = ctime
    # Añadir los fps a la imagen antes de mostrarla, usando la función putText de OpenCV, que recibe la imagen, el texto, la posición, la fuente, el tamaño, el color y el grosor
    cv.putText(img, str(int(fps)), (10, 30), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
    # Utilizar el mismo objeto detector en cada iteración, llamando al método Obtener_Pose con la imagen y el parámetro dibujar en False, ya que solo nos interesa el ángulo del codo
    img = detector.Obtener_Pose(img,False)   
    # Llamar al método Obtener_posicion con la imagen y almacenar la lista con las coordenadas de los puntos de referencia de la pose
    lm_lista=detector.Obtener_posicion(img)

    # Verificar si la lista tiene algún elemento, lo que significa que se detectó la pose
    if len(lm_lista)!=0:
        # Llamar al método Obtener_Angulo con la imagen y el parámetro dibujar en True, ya que queremos ver el ángulo del codo en la imagen, y almacenar el ángulo calculado
        Angulo=detector.Obtener_Angulo(img,True)
        # Calcular el porcentaje de flexión del codo, usando la función interp de NumPy, que recibe el ángulo, el rango de ángulos posibles (190: brazo extendido, 80: brazo flexionado) y el rango de porcentajes correspondientes (100: brazo extendido, 0: brazo flexionado)
        per=np.interp(Angulo,(190,80),(100,0))
        # Verificar si el porcentaje de flexión es 100, lo que significa que el brazo está extendido
        if per==100:
            # Verificar si la dirección del movimiento es 0, lo que significa que el brazo estaba bajando
            if dir==0:
                # Aumentar el contador en 0.5, ya que se completó la mitad de una repetición
                contador+=0.5
                # Cambiar la dirección del movimiento a 1, lo que significa que el brazo está subiendo
                dir=1
        # Verificar si el porcentaje de flexión es 0, lo que significa que el brazo está flexionado
        if per==0:
            # Verificar si la dirección del movimiento es 1, lo que significa que el brazo estaba subiendo
            if dir==1:
                # Aumentar el contador en 0.5, ya que se completó la otra mitad de una repetición
                contador+=0.5
                # Cambiar la dirección del movimiento a 0, lo que significa que el brazo está bajando
                dir=0
        # Añadir el contador a la imagen, usando la función putText de OpenCV, que recibe la imagen, el texto, la posición, la fuente, el tamaño, el color y el grosor
        cv.putText(img, str(int((contador))), (50,100), cv.FONT_HERSHEY_PLAIN, 5, (255,0,255),5)

    # Mostrar la imagen con la pose, el ángulo, el porcentaje y el contador, usando la función imshow de OpenCV, que recibe el nombre de la ventana y la imagen
    cv.imshow("video", img)
    # Esperar a que el usuario presione una tecla, usando la función waitKey de OpenCV, que recibe el tiempo de espera en milisegundos
    if cv.waitKey(1) & 0xFF == ord('q'):
        # Si el usuario presiona la tecla q, salir del bucle
        break
# Liberar el objeto de la clase VideoCapture, usando el método release
cap.release()
# Destruir todas las ventanas creadas por OpenCV, usando la función destroyAllWindows
cv.destroyAllWindows()