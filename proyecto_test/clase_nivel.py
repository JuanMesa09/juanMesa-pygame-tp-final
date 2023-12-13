

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
        self.ancho_ventana = ancho_pantalla
        self.alto_ventana = alto_pantalla
        #----------------------------------------------------------------
        self.fondo_carga = pg.image.load(self.fondo)
        self.fondo_carga= pg.transform.scale(self.fondo_carga,(self.ancho_ventana, self.alto_ventana))
        #-------------------------------------------------------------------------
        self.luffy = Jugador(self.configuraciones['jugador']['posicion_x'],
                                self.configuraciones['jugador']['posicion_y'],
                                self.configuraciones['jugador']['velocidad_caminar'],
                                self.configuraciones['jugador']['cuadros_por_seg'])
        #-------------------------------------------------------------------------
        #estructura
        self.estructura  = self.configuraciones["estructuras"]
        self.plataformas_ordenadas = self.configuraciones["plataformas"]
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
        self.grupo_items_puntos = pg.sprite.Group()
        self.grupo_items_vida = pg.sprite.Group()
        self.grupo_trampas = pg.sprite.Group()
        self.generador_enemigos()
        self.crear_items_puntaje()
        self.crear_items_vida()
        self.crear_plataformas()
        self.crear_trampas()


    def generador_enemigos(self):
        enemigos = self.cantidad_enemigos
        for _ in range(enemigos):
            x =  random.randint(self.enemigo["posicion_x"]["x_1"], self.enemigo["posicion_x"]["x_2"])
            y =  self.enemigo["posicion_y"]
            enemigos = Enemigo((x,y))
            self.grupo_enemigos.add(enemigos)


    def dibujar_enemigos(self):
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
                
                self.grupo_items_puntos.add(objetivo)
    
    def dibujar_items(self):
        for item in self.grupo_items_puntos:
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
                
                self.grupo_items_vida.add(objetivo)
    
    def dibujar_items_vida(self):
        for item_vida in self.grupo_items_vida:
            item_vida.draw(self.pantalla)
    
    def crear_plataformas(self):
        imagen = self.estructura["imagen"]
        ancho = self.estructura["ancho"]
        alto = self.estructura["alto"]
        
        for p in self.plataformas_ordenadas:
            
            x = p["x"]
            y = p["y"]

            plataforma = Estructura(x, y, ancho, alto, imagen)
            self.lista_estructuras.append(plataforma)
        
    def dibujar_estructuras(self):

        for plataforma in self.lista_estructuras:
            plataforma.draw(self.pantalla)
    
    def crear_trampas(self):

        imagen = self.trampa["imagen"]
        ancho = self.trampa["ancho"]
        alto = self.trampa["alto"]
        for nombre, datos in self.trampa.items():
            if nombre.startswith("trampa"):
                x = datos["x"]
                y = datos["y"]
                trampa = Trampa(imagen,x, y, ancho, alto )
                self.grupo_trampas.add(trampa)
    def dibujar_trampas(self):
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
    
    

    def draw(self):

        self.luffy.draw(self.pantalla)



    def update(self, pantalla):
        
        self.dibujar_enemigos()
        self.grupo_enemigos.update()
        self.dibujar_items()
        self.grupo_items_puntos.update()
        self.dibujar_items_vida()
        self.grupo_items_vida.update()
        self.dibujar_estructuras()
        self.dibujar_trampas()
        self.cargar_music()
        self.luffy.draw(pantalla)
        