import f_transcriber
import threading
import cv2 
import time
import re
import imutils
import f_main
import numpy as np
import config as cfg
import textwrap

def bounding_box(img,box,match_name=[]):
    for i in np.arange(len(box)):
        y0,x1,y1,x0 = box[i]
        img = cv2.rectangle(img,
                      (x0,y0),
                      (x1,y1),
                      (0,255,0),3);
        if not match_name:
            continue
        else:
            cv2.putText(img, match_name[i], (x0, y0-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)
    return img

def print_subtitles(subtitles,frame):
    wrapped_text = textwrap.wrap(subtitles, width=40)
    num_phrases = len(wrapped_text)
    for i,line in enumerate(wrapped_text):
        # devuelve el ancho y el alto de una cadena de texto
        w_text, h_text = cv2.getTextSize(line, cfg.font, cfg.font_size, cfg.font_thickness)[0]
        # espacio entre break line y break line
        gap = h_text + 10
        y = int(frame.shape[0]) - (num_phrases - i) * gap
        x = int((frame.shape[1] - w_text) / 2)
        cv2.putText(frame, line, (x, y), cfg.font,
                    cfg.font_size, 
                    (0,255,0), 
                    cfg.font_thickness, 
                    lineType = cv2.LINE_AA)
    return frame


name_asisstant = "Alfred"
# instancio camara
cam = cv2.VideoCapture(0)
cv2.namedWindow(name_asisstant)


# instancio microfono
my_mic = f_transcriber.MicrophoneStream()
# intancio transcriber
my_trans = f_transcriber.Transcriber(name_asisstant)
# instanciar reconocedor de rostros
rec_face = f_main.rec()
# inicio a transcribir audio en un hilo
t1 = threading.Thread(target=my_trans.go_transcriber, args=(my_mic,))
# al colocarlo en modo demonior todos los threads se eliminan cuando se cierra el proceso
t1.daemon = True 
t1.start()

# obtengo las resolucion de la webcam
_,frame = cam.read()
frame = imutils.resize(frame,width=720)
w,h,_= frame.shape

# Configuracion inicial
activate_subtitles = False
activate_recognition = False
max_frames = 30
count_frames = 0
subtitles_ant = ""
print_none = False
# bucle principal
while True:
    # read the frame from the camera and send it to the server
    ret, frame = cam.read()
    frame = imutils.resize(frame,width=720)
    
    # obtener transcripcion
    subtitles = my_trans.transcriber_data

    # ----------------------------- Inicio instrucciones ------------------------------------
    # ---------------------------------------------------------------------------------------
    # salir o adios: termina la ejecucion 
    if re.search(r'\b({}|{})\b'.format("adiós","salir"), subtitles, re.I):
        print('Exiting..')
        break
    # nombre_asistente + salir o adios: termina la ejecucion 
    if re.search(r'\b({}|{})\b'.format(name_asisstant+" "+"adiós",name_asisstant+" "+"salir"), subtitles, re.I):
        print('Exiting..')
        break
    
    # nombre_asistente + activar subtitulos: termina la ejecucion 
    if re.search(r'\b({})\b'.format(name_asisstant+" "+"activar subtítulos",), subtitles, re.I):
        activate_subtitles = True

    # nombre_asistente + activar subtitulos: termina la ejecucion 
    if re.search(r'\b({})\b'.format(name_asisstant+" "+"activar reconocimiento",), subtitles, re.I):
        activate_recognition = True

    # funciones en ingles ingles
    # nombre_asistente + salir o adios: termina la ejecucion 
    if re.search(r'\b({}|{})\b'.format(name_asisstant+" "+"bye",name_asisstant+" "+"exit"), subtitles, re.I):
        print('Exiting..')
        break
    
    # nombre_asistente + activar subtitulos: termina la ejecucion 
    if re.search(r'\b({})\b'.format(name_asisstant+" "+"activate subtitles",), subtitles, re.I):
        activate_subtitles = True

    # nombre_asistente + activar subtitulos: termina la ejecucion 
    if re.search(r'\b({})\b'.format(name_asisstant+" "+"activate recognition",), subtitles, re.I):
        activate_recognition = True

    # ----------------------------- Fin instrucciones ---------------------------------------
    # ---------------------------------------------------------------------------------------
    
    # realizar reconocimiento facial
    if activate_recognition:
        res = rec_face.recognize_face(frame)
        bounding_box(frame,res["faces"],res["names"])
    # Borrar subtitulos viejos
    if subtitles_ant == subtitles:
        count_frames += 1
    else:
        count_frames = 0
        print_none = False
    if count_frames == max_frames:
        print_none = True
        count_frames = 0
    subtitles_ant = subtitles
    # imprimir subtitulos
    if activate_subtitles:
        if print_none:
            cv2.putText(frame,"",(10,w-20),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
        else:
            #cv2.putText(frame,subtitles,(10,w-20),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
            frame = print_subtitles(subtitles,frame)
    cv2.imshow(name_asisstant,frame)
    if cv2.waitKey(1) &0xFF == ord('q'):
        break

# matar thread
t1.join()