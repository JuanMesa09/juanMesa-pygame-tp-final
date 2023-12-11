

import json 

ANCHO_VENTANA = 800
ALTO_VENTANA = 600
FPS = 30
DEBUG = False
RUTA = './config/config.json'



def abrir_config():
    with open(RUTA, 'r', encoding= 'utf-8') as config:

        return json.load(config)


