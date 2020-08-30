# configuraciones para el microfono
RATE = 16000 # tasa de muestreo en Hz
CHUNK = int(RATE / 10)  # 100ms --> tamaño en tiempo del fragmento del audio que se envia al buffer


# -------------------------- Configuraciones Api Speech Recognition Google ----------------------------------------
# See http://g.co/cloud/speech/docs/languages
# for a list of supported languages.
#language_code = 'es-CO'  # a BCP-47 language tag
language_code = 'en-US'
path_json = "path_from_key (json) of GCP"


# -------------------------- Face Recognition ----------------------------------------
# path imagenes folder
path_images = "images"


# -------------------------- Configuracion subtitulos ----------------------------------------
# formatear subtitulos 
font_size = 1
font_thickness = 2
import cv2
font = cv2.FONT_HERSHEY_SIMPLEX