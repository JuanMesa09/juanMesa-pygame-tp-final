
import pygame as pg 


class Puntaje():
    
    def __init__(self):
        super().__init__()
        self.puntaje = 0
    
    
    def muerte_enemiga(self, puntuacion):
        self.puntaje += puntuacion
        return self.puntaje
    
    def agarrar_item(self, puntuacion):
        self.puntaje += puntuacion
        return  self.puntaje

    def  obtener_puntaje(self):
        return self.puntaje

    def destruir_trampa(self, puntuacion):

        self.puntaje += puntuacion

