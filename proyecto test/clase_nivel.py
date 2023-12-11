

import pygame as pg, random
from constantes import *  
from clase_jugador import Jugador 
from clase_enemigo import Enemigo
from clase_item import Item
from clase_estructuras import Estructura 
from clase_trampas import Trampa



class Nivel:
    def __init__(self, pantalla: pg.surface.Surface, ancho_pantalla, alto_pantalla, nombre_lvl):
        self.configuraciones = abrir_config().get(nombre_lvl)
        if self.configuraciones:
            self.nombre_nivel = self.configuraciones['nivel']

        else:
            # Puedes manejar la falta de configuración según tus necesidades
            print(f"No hay configuración para el nivel {nombre_lvl}")
            self.configuraciones = {}
        
        self.fondo = self.nombre_nivel['fondo']
        self.music_path = self.nombre_nivel['musica_fondo']
        self.cantidad_trampas = self.nombre_nivel['cantidad_trampas']
        self.cantidad_enemigos =  self.nombre_nivel['cantidad_enemigos']
        self.cantidad_trampas =  self.nombre_nivel['tiempo_nivel_1']
        
        self.pantalla = pantalla
        #-------------------------------------------------------------------------
        self.luffy = Jugador(self.configuraciones['jugador']['posicion_x'],
                                self.configuraciones['jugador']['posicion_y'],
                                self.configuraciones['jugador']['velocidad_caminar'],
                                self.configuraciones['jugador']['cuadros_por_seg'])
        #-------------------------------------------------------------------------
        #estructura
        self.estructura  = self.configuraciones["estructuras"]
        self.lista_estructuras = []
        #-------------------------------------------------------------------------

        self.enemigo = self.configuraciones["enemigo"]
        #-------------------------------------------------------------------------
        #trampa
        self.trampa = self.configuraciones["trampas"]

        #-------------------------------------------------------------------------
        self.item_puntaje = self.configuraciones['item_puntos']
        self.item_vida = self.configuraciones['item_vida']
        #grupos sprites
        self.grupo_enemigos = pg.sprite.Group()
        self.grupo_items = pg.sprite.Group()
        self.grupo_trampas = pg.sprite.Group()
    
    def generador_enemigos(self):
        enemigos = self.cantidad_enemigos
        for _ in range(enemigos):
            x =  random.randint(self.enemigo["posicion_x"]["x_1"], self.enemigo["posicion_x"]["x_2"])
            y =  self.enemigo["posicion_y"]
            enemigos = Enemigo((x,y))
            self.grupo_enemigos.add(enemigos)

        for enemigo in self.grupo_enemigos:
            enemigo.draw(self.pantalla)

    def crear_items_puntaje(self):
        items = self.nombre_nivel["cantidad_item_puntos"]
        if self.item_puntaje:
            imagen = self.item_puntaje["imagen_item"]
            ancho = self.item_puntaje["ancho"]
            alto = self.item_puntaje["alto"]
            for i in range(1, items + 1):
                x = self.item_puntaje[f"items_{i}"]["x"]
                y = self.item_puntaje[f"items_{i}"]["y"]
                objetivo = Item(imagen, x, y, ancho, alto)
                
                self.grupo_items.add(objetivo)
        for item in self.grupo_items:
            item.draw(self.pantalla)
    
    def crear_items_vida(self):

        items = self.nombre_nivel["cantidad_items_vida"]
        if self.item_vida:
            imagen = self.item_vida["imagen"]
            ancho = self.item_vida["ancho"]
            alto = self.item_vida["alto"]
            for i in range(1, items + 1):
                x = self.item_vida[f"item_vida_{i}"]["x"]
                y = self.item_vida[f"item_vida_{i}"]["y"]
                objetivo = Item(imagen, x, y, ancho, alto)
                
                self.grupo_items.add(objetivo)
        for item_vida in self.grupo_items:
            item_vida.draw(self.pantalla)
    
    def crear_plataformas(self):
        imagen = self.estructura["imagen"]
        ancho = self.estructura["ancho"]
        alto = self.estructura["alto"]

        
        for nombre, datos in self.estructura.items():
            if nombre.startswith("estructura"):#verifica si la cadena comienza con un prefijo específico
                x = datos["x"]
                y = datos["y"]
                plataforma = Estructura(x, y, ancho, alto, imagen)
                self.lista_estructuras.append(plataforma)
        for plataforma in self.lista_estructuras:
            plataforma.draw(self.pantalla)
    
    def crear_trampas(self):

        imagen = self.trampa["imagen"]
        ancho = self.trampa["ancho"]
        alto = self.trampa["alto"]
        for nombre, datos in self.trampa.items():
            if nombre.startswith("trampa"):#verifica si la cadena comienza con un prefijo específico
                x = datos["x"]
                y = datos["y"]
                trampa = Trampa(imagen,x, y, ancho, alto )
                self.grupo_trampas.add(trampa)

        for trampa in self.grupo_trampas:
            trampa.draw(self.pantalla)


    def cargar_music(self):

        nivel_config = self.configuraciones.get('nivel')
        self.music_path = nivel_config.get('musica_fondo')

        if self.music_path:
            
            pg.mixer.music.load(self.music_path)
            pg.mixer.music.set_volume(0.10)
    
    def correr_musica(self):
        if self.music_path:
            pg.mixer.music.play(-1)  

    def parar_musica(self):
        pg.mixer.music.stop()
    
    def cargar_fondo(self):
        self.fondo_carga = pg.image.load(self.fondo)
        self.fondo_carga_1= pg.transform.scale(self.fondo_carga,(ANCHO_VENTANA, ALTO_VENTANA))
        

    def draw(self):

        self.luffy.draw(self.pantalla)



    def update(self, pantalla):
        
        self.generador_enemigos()
        self.crear_items_puntaje()
        self.crear_items_vida()
        self.crear_plataformas()
        self.cargar_music()
        self.crear_trampas()
        self.cargar_fondo()
        self.luffy.draw(pantalla)
        