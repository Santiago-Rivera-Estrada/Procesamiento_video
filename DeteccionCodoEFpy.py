import cv2 as cv
import mediapipe as mp
import time
import  math
import numpy as np
class Detector_Pose():
    def __init__(self, mode=False, smooth=True, confianza_dete=0.5, confianza_segui=0.5):
        self.mode = mode
        self.smooth = smooth
        self.confianza_dete = confianza_dete
        self.confianza_segui = confianza_segui

        # Convertir smooth a bool
        self.smooth = bool(self.smooth)

        self.mpPose = mp.solutions.pose
        self.mpDraw = mp.solutions.drawing_utils
        self.pose = self.mpPose.Pose(
            static_image_mode=self.mode,
            model_complexity=0 if self.mode else 1,  # 0 para simple, 1 para complejo
            smooth_landmarks=self.smooth,
            min_detection_confidence=self.confianza_dete,
            min_tracking_confidence=self.confianza_segui)
    def Obtener_Pose(self, img, dibujar=True):
        
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        resul = self.pose.process(imgRGB)  
        self.trajectory_14 = []
        self.trajectory_12 = []
        self.trajectory_16 = []
    
        if resul.pose_landmarks:
            if dibujar:
                for iD, lm in enumerate(resul.pose_landmarks.landmark):
                    altura, ancho, canales = img.shape
                    
                    # Solo dibujar para los marcadores #14, #12 y #16
                    if iD == 14 or iD == 12 or iD == 16:
                        cx, cy = int(lm.x * ancho), int(lm.y * altura)
                        cv.circle(img, (cx, cy), 5, (255, 0, 255), cv.FILLED)
                        
                    # Almacenar las coordenadas en las listas de trayectoria
                    if iD == 14:
                        self.trajectory_14 = [cx, cy]
                    elif iD == 12:
                        self.trajectory_12 = [cx, cy]
                    elif iD == 16:
                        self.trajectory_16 = [cx, cy]
    
                # Dibujar la línea entre los puntos #12 y #14
                if self.trajectory_14 and self.trajectory_12:
                    cv.line(img, tuple(self.trajectory_12), tuple(self.trajectory_14), (0, 255, 0), thickness=2)
    
                # Dibujar la línea entre los puntos #14 y #16
                if self.trajectory_14 and self.trajectory_16:
                    cv.line(img, tuple(self.trajectory_14), tuple(self.trajectory_16), (0, 255, 0), thickness=2)
    
        return img
    def Obtener_posicion(self,img):
        self.lm_List=[]
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        resul = self.pose.process(imgRGB) 
        if resul.pose_landmarks:
            for iD, lm in enumerate(resul.pose_landmarks.landmark):
                altura, ancho, canales = img.shape
                if iD == 12 or iD == 14 or iD==16:
                    cx, cy = int(lm.x * ancho), int(lm.y * altura)
                    self.lm_List.append([iD,cx,cy])
        return self.lm_List
    def Obtener_Angulo(self, img, dibujar=True):
        lm_List = self.Obtener_posicion(img)  # Obtener la lista de coordenadas actualizada
        
        if len(lm_List) >= 3:  # Asegurarse de tener al menos tres puntos para calcular el ángulo
            x1, y1 = lm_List[0][1:]
            x2, y2 = lm_List[1][1:]
            x3, y3 = lm_List[2][1:]
            
            # Ajustar las coordenadas según la redimensión de la imagen
            x1, y1 = int(x1 * 400 / img.shape[1]), int(y1 * 400 / img.shape[0])
            x2, y2 = int(x2 * 400 / img.shape[1]), int(y2 * 400 / img.shape[0])
            x3, y3 = int(x3 * 400 / img.shape[1]), int(y3 * 400 / img.shape[0])
    
            angulo = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
            if angulo < 0:
                angulo += 360
            print(angulo)
    
            if dibujar:
                cv.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
                cv.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
                cv.circle(img, (x1, y1), 5, (255, 0, 0), cv.FILLED)
                cv.circle(img, (x2, y2), 5, (255, 0, 0), cv.FILLED)
                cv.circle(img, (x3, y3), 5, (255, 0, 0), cv.FILLED)
    
                # Ajustar la posición del texto y usar un tamaño y grosor de contorno más estéticos
                font = cv.FONT_HERSHEY_SIMPLEX
                cv.putText(img, str(int(angulo)), (x2-50, y2+50), font, 1, (255, 0, 255), 2, cv.LINE_AA)
    
        return angulo
