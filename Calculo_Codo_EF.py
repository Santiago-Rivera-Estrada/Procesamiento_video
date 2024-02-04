import sys
sys.path.append("C:/Users/santi/Downloads/")
import cv2 as cv
import DeteccionCodoEFpy as DC
import time
import numpy as np
cap = cv.VideoCapture("C:/Users/santi/Downloads/video1.mp4")
detector = DC.Detector_Pose()
ptime=0
contador=0
dir=0
while True:
    success, img = cap.read()
    # Redimensionar la imagen antes de procesarla
    img = cv.resize(img, (400, 400), interpolation=cv.INTER_AREA)
    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime
    # Añadir los fps a la imagen antes de mostrarla
    cv.putText(img, str(int(fps)), (10, 30), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
    # Utilizar el mismo objeto detector en cada iteración
    img = detector.Obtener_Pose(img,False)   
    lm_lista=detector.Obtener_posicion(img)

    if len(lm_lista)!=0:
        Angulo=detector.Obtener_Angulo(img,True)
        per=np.interp(Angulo,(190,80),(100,0))
        altura_ventana = 400
        rango_inferior = 80
        rango_superior = 190
        bar = np.interp(Angulo, (rango_superior, rango_inferior), (0, altura_ventana))

        if per==100:
            if dir==0:
                contador+=0.5
                dir=1
        if per==0:
            if dir==1:
                contador+=0.5
                dir=0
        cv.putText(img, str(int((contador))), (50,100), cv.FONT_HERSHEY_PLAIN, 5, (255,0,255),5)
        # cv.rectangle(img, (5,200),(80,300),(0,255,255),cv.FILLED)
        # cv.rectangle(img, (5,int(bar)), (80,20),(0,255,0),cv.FILLED)
        # cv.putText(img, str(int((per)))+"%", (10,75), cv.FONT_HERSHEY_PLAIN, 4, (255,0,255),4)

    cv.imshow("video", img)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv.destroyAllWindows()
