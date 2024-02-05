# Importar las bibliotecas necesarias
import cv2 as cv # OpenCV es una biblioteca de visión por computadora que ofrece funciones para procesar imágenes y videos
import mediapipe as mp # MediaPipe es un marco de trabajo para construir pipelines de aprendizaje automático para procesar datos de series temporales como video, audio, etc.
import math # La biblioteca math ofrece funciones matemáticas
# Definir la clase Detector_Pose
class Detector_Pose():
    # Definir el método constructor
    def _init_(self, mode=False, smooth=True, confianza_dete=0.5, confianza_segui=0.5):
        # Establecer los atributos de la clase con los parámetros del constructor
        self.mode=mode # El modo indica si se procesa una imagen estática o un video. Por defecto es False, lo que significa que se procesa un video
        self.smooth=smooth # El suavizado indica si se aplican filtros de suavizado a los puntos de referencia de la pose. Por defecto es True, lo que significa que se aplican los filtros
        self.confianza_dete=confianza_dete # La confianza de detección indica el umbral de confianza mínimo para detectar la pose en una imagen. Por defecto es 0.5, lo que significa que se requiere al menos un 50% de confianza
        self.confianza_segui=confianza_segui # La confianza de seguimiento indica el umbral de confianza mínimo para seguir la pose en un video. Por defecto es 0.5, lo que significa que se requiere al menos un 50% de confianza
        self.smooth=bool(self.smooth) # Convertir el valor de suavizado a un valor booleano
        self.mpPose=mp.solutions.pose # Crear un objeto de la clase pose de MediaPipe, que ofrece un modelo preentrenado para detectar y estimar la pose humana
        self.mpDraw=mp.solutions.drawing_utils # Crear un objeto de la clase drawing_utils de MediaPipe, que ofrece funciones para dibujar los puntos de referencia y las conexiones de la pose
        self.pose=self.mpPose.Pose(static_image_mode=self.mode, model_complexity=0 if self.mode else 1, smooth_landmarks=self.smooth, min_detection_confidence=self.confianza_dete, min_tracking_confidence=self.confianza_segui) # Crear un objeto de la clase Pose con los atributos de la clase como argumentos. El modelo de complejidad indica el nivel de detalle de la pose, siendo 0 el más simple y 2 el más complejo. Por defecto se usa el nivel 1 para el video y el nivel 0 para la imagen estática

    # Definir el método Obtener_Pose, que recibe una imagen y un parámetro opcional para indicar si se quiere dibujar la pose o no
    def Obtener_Pose(self, img, dibujar=True):
        # Convertir la imagen de BGR a RGB, ya que el modelo de MediaPipe usa el formato RGB
        imgRGB=cv.cvtColor(img, cv.COLOR_BGR2RGB)
        # Procesar la imagen con el objeto pose y obtener el resultado, que contiene los puntos de referencia de la pose
        resul=self.pose.process(imgRGB)
        # Inicializar unas listas vacías para almacenar las coordenadas de algunos puntos de referencia de interés
        self.trajectory_14=[]
        self.trajectory_12=[]
        self.trajectory_16=[]
        # Verificar si el resultado contiene puntos de referencia de la pose
        if resul.pose_landmarks:
            # Verificar si se quiere dibujar la pose
            if dibujar:
                # Recorrer los puntos de referencia de la pose con sus índices
                for iD, lm in enumerate(resul.pose_landmarks.landmark):
                    # Obtener las dimensiones de la imagen
                    altura, ancho, canales=img.shape
                    # Verificar si el índice del punto de referencia es 14, 12 o 16, que corresponden al codo derecho, el hombro derecho y la muñeca derecha respectivamente
                    if iD==14 or iD==12 or iD==16:
                        # Calcular las coordenadas del punto de referencia en píxeles, multiplicando su valor normalizado por el ancho y la altura de la imagen
                        cx, cy=int(lm.x*ancho), int(lm.y*altura)
                        # Dibujar un círculo en la imagen con el centro en las coordenadas del punto de referencia, un radio de 5 píxeles, un color morado y un grosor relleno
                        cv.circle(img, (cx, cy), 5, (255, 0, 255), cv.FILLED)
                    # Verificar si el índice del punto de referencia es 14, que corresponde al codo derecho
                    if iD==14:
                        # Almacenar las coordenadas del punto de referencia en la lista correspondiente
                        self.trajectory_14=[cx, cy]
                    # Verificar si el índice del punto de referencia es 12, que corresponde al hombro derecho
                    elif iD==12:
                        # Almacenar las coordenadas del punto de referencia en la lista correspondiente
                        self.trajectory_12=[cx, cy]
                    # Verificar si el índice del punto de referencia es 16, que corresponde a la muñeca derecha
                    elif iD==16:
                        # Almacenar las coordenadas del punto de referencia en la lista correspondiente
                        self.trajectory_16=[cx, cy]
                # Verificar si se tienen las coordenadas del codo derecho y el hombro derecho
                if self.trajectory_14 and self.trajectory_12:
                    # Dibujar una línea en la imagen que conecte los puntos de referencia del codo derecho y el hombro derecho, con un color verde y un grosor de 2 píxeles
                    cv.line(img, tuple(self.trajectory_12), tuple(self.trajectory_14), (0, 255, 0), thickness=2)
                # Verificar si se tienen las coordenadas del codo derecho y la muñeca derecha
                if self.trajectory_14 and self.trajectory_16:
                    # Dibujar una línea en la imagen que conecte los puntos de referencia del codo derecho y la muñeca derecha, con un color verde y un grosor de 2 píxeles
                    cv.line(img, tuple(self.trajectory_14), tuple(self.trajectory_16), (0, 255, 0), thickness=2)
        # Devolver la imagen con la pose dibujada
        return img

    # Definir el método Obtener_posicion, que recibe una imagen y devuelve una lista con las coordenadas de algunos puntos de referencia de la pose
    def Obtener_posicion(self,img):
        # Inicializar una lista vacía para almacenar las coordenadas de los puntos de referencia
        self.lm_List=[]
        # Convertir la imagen de BGR a RGB, ya que el modelo de MediaPipe usa el formato RGB
        imgRGB=cv.cvtColor(img, cv.COLOR_BGR2RGB)
        # Procesar la imagen con el objeto pose y obtener el resultado, que contiene los puntos de referencia de la pose
        resul=self.pose.process(imgRGB) 
        # Verificar si el resultado contiene puntos de referencia de la pose
        if resul.pose_landmarks:
            # Recorrer los puntos de referencia de la pose con sus índices
            for iD, lm in enumerate(resul.pose_landmarks.landmark):
                # Obtener las dimensiones de la imagen
                altura, ancho, canales=img.shape
                # Verificar si el índice del punto de referencia es 12, 14 o 16, que corresponden al hombro derecho, el codo derecho y la muñeca derecha respectivamente
                if iD==12 or iD==14 or iD==16:
                    # Calcular las coordenadas del punto de referencia en píxeles, multiplicando su valor normalizado por el ancho y la altura de la imagen
                    cx, cy=int(lm.x*ancho), int(lm.y*altura)
                    # Añadir el índice y las coordenadas del punto de referencia a la lista
                    self.lm_List.append([iD,cx,cy])
        # Devolver la lista con las coordenadas de los puntos de referencia
        return self.lm_List
# Definir el método Obtener_Angulo, que recibe una imagen y un parámetro opcional para indicar si se quiere dibujar el ángulo o no
def Obtener_Angulo(self, img, dibujar=True):
    # Obtener la lista con las coordenadas de los puntos de referencia de la pose
    lm_List=self.Obtener_posicion(img)
    # Verificar si la lista tiene al menos tres elementos, que corresponden al hombro derecho, el codo derecho y la muñeca derecha
    if len(lm_List)>=3:
        # Extraer las coordenadas de los puntos de referencia de la lista
        x1, y1=lm_List[0][1:]
        x2, y2=lm_List[1][1:]
        x3, y3=lm_List[2][1:]
        # Ajustar las coordenadas de los puntos de referencia al tamaño de la imagen, multiplicando por un factor de 400 dividido por el ancho y la altura de la imagen
        x1, y1=int(x1*400/img.shape[1]), int(y1*400/img.shape[0])
        x2, y2=int(x2*400/img.shape[1]), int(y2*400/img.shape[0])
        x3, y3=int(x3*400/img.shape[1]), int(y3*400/img.shape[0])
        # Calcular el ángulo entre los tres puntos de referencia, usando la función atan2 de la biblioteca math y convirtiendo el resultado a grados
        angulo=math.degrees(math.atan2(y3-y2, x3-x2)-math.atan2(y1-y2, x1-x2))
        # Si el ángulo es negativo, sumarle 360 para obtener el ángulo positivo equivalente
        if angulo<0:
            angulo+=360
        # Imprimir el ángulo en la consola
        print(angulo)
        # Verificar si se quiere dibujar el ángulo
        if dibujar:
            # Dibujar dos líneas en la imagen que conecten el hombro derecho con el codo derecho y el codo derecho con la muñeca derecha, con un color blanco y un grosor de 3 píxeles
            cv.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            # Dibujar tres círculos en la imagen con el centro en los puntos de referencia, un radio de 5 píxeles, un color azul y un grosor relleno
            cv.circle(img, (x1, y1), 5, (255, 0, 0), cv.FILLED)
            cv.circle(img, (x2, y2), 5, (255, 0, 0), cv.FILLED)
            cv.circle(img, (x3, y3), 5, (255, 0, 0), cv.FILLED)
            # Definir una fuente para el texto
            font=cv.FONT_HERSHEY_SIMPLEX
            # Escribir el ángulo en la imagen, con el texto redondeado al entero más cercano, una posición desplazada 50 píxeles del codo derecho, la fuente definida, un tamaño de 1, un color morado y un grosor de 2 píxeles
            cv.putText(img, str(int(angulo)), (x2-50, y2+50), font, 1, (255, 0, 255), 2, cv.LINE_AA)
    # Devolver el ángulo calculado
    return angulo