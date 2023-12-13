

import random
import pygame as pg 
from constantes import *
from clase_jugador import Jugador
from clase_nivel import Nivel
from clase_puntaje import Puntaje





class Game():

    def __init__(self) :
        super().__init__()
    
    # def pausa(self):
    #     pausa = True
        

    #     while pausa:
    #         self.pantalla.fill((0, 0, 0))
    #         for event in pg.event.get():
                
    #             if event.type == pg.QUIT:
    #                 pausa = False
    #                 self.juego_ejecutandose = False
    #                 pg.quit()
    #             if event.type == pg.K_p:
    #                 pausa = False
    #                 self.juego_ejecutandose = True
                
    def correr_nivel(self, nombre_nivel):
    
        self.icono_vida =pg.transform.scale(pg.image.load(r'./imagenes\vidas\vida_mate.png'), (25,25))
        self.rect = self.icono_vida.get_rect()
        pg.init()
        pg.mixer.init()
        self.sonido_item_vida = pg.mixer.Sound(r"./sonidos/audio_mate.mp3")
        self.puntaje_jugador = 0
        self.total_vidas = 0
        self.sonido_item_puntos = pg.mixer.Sound(r"./sonidos/audio_item_1.mp3")
        self.pantalla = pg.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        
        titulo = pg.display.set_caption("El paseo de Luffy")
        font = pg.font.Font(None, 36)
        self.juego = Nivel(self.pantalla, ANCHO_VENTANA, ALTO_VENTANA, nombre_nivel)
        
        
        retardo = pg.time.Clock()

        juego_ejecutandose = True
        
        self.puntaje = Puntaje()
        self.tiempo_inicial = pg.time.get_ticks()//1000 
        self.duracion_game =  40
    


                        
        while juego_ejecutandose:
            lista_eventos = []
            
            delta_ms = retardo.tick(FPS)
            pg.time.delay(30)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    juego_ejecutandose = False
                    break
                # if event.type == pg.K_p:
                #     self.pausa()
                    
                lista_eventos.append(event)
            #tiempo transcurrido
            tiempo_actual =  pg.time.get_ticks() // 1000
            tiempo_transcurrido = tiempo_actual - self.tiempo_inicial
            tiempo_restante = max(0, self.duracion_game - tiempo_transcurrido)
            
            if tiempo_transcurrido >= self.duracion_game:
                juego_ejecutandose =  False
                self.pantalla.fill((0, 0, 0))
                texto_victoria = font.render(f"Tiempo Terminado DERRORTA", True, (255,255,255))
                texto_puntaje_victoria = font.render(f"Puntaje: {self.puntaje.obtener_puntaje()}", True, (255,255,255))
                self.pantalla.blit(texto_puntaje_victoria,(100, ALTO_VENTANA // 2))
                self.pantalla.blit(texto_victoria, (ANCHO_VENTANA // 2 - texto_victoria.get_width() // 1, ALTO_VENTANA // 2 - texto_victoria.get_height() // 1))
                pg.display.flip()
                pg.time.delay(3000)
            
            #tiempo de juego
            tiempo_juego = font.render(f"Tiempo Restante {tiempo_restante}", True, (0,0,0))
            texto_puntaje = font.render(f"Puntaje: {self.puntaje.obtener_puntaje()}", True, (0,0,0))
            texto_vidas = font.render(f"x: {self.juego.luffy.vidas}", True, (0,0,0))
            
            #colision enemigos con balas y estructuras
            for bala in self.juego.luffy.bala_grupo:
                colision_bala_con_enemigo = pg.sprite.spritecollide(bala, self.juego.grupo_enemigos, True)
                
                
                for enemigo in colision_bala_con_enemigo:
                    self.puntaje.muerte_enemiga(enemigo.puntaje)
                    bala.kill()
                    
                if  len(self.juego.grupo_enemigos) < 1 :
                    
                    self.juego = Nivel(self.pantalla, ANCHO_VENTANA, ALTO_VENTANA, "nivel_2")

                if len(self.juego.grupo_enemigos) < 1 and (tiempo_transcurrido <= self.duracion_game) :

                    self.juego = Nivel(self.pantalla, ANCHO_VENTANA, ALTO_VENTANA, "nivel_3")
                    
                    self.pantalla.fill((0, 0, 0))
                    texto_victoria = font.render(f"Has logrado la... VICTORIA SOS CRACK", True, (255,255,255))
                    texto_puntaje_victoria = font.render(f"Puntaje: {self.puntaje.obtener_puntaje()}", True, (255,255,255))
                    self.pantalla.blit(texto_puntaje_victoria,(0, ALTO_VENTANA // 2))
                    self.pantalla.blit(texto_victoria, (480 - texto_victoria.get_width() // 1, ALTO_VENTANA // 2 - texto_victoria.get_height() // 1))
                    pg.display.flip()
                    pg.time.delay(3000)
                
                #colision bala con estructura
                colision_bala_en_estructura =  pg.sprite.spritecollide(bala, self.juego.lista_estructuras,False)
                for estructura in colision_bala_en_estructura:
                    bala.kill()
                #colision bala con trampa
                colision_bala_trampa = pg.sprite.spritecollide(bala, self.juego.grupo_trampas, True)
                for trampa in colision_bala_trampa:
                    self.puntaje.destruir_trampa(trampa.puntaje)
                    bala.kill()
            #colision jugador con item
            colision_con_item_score = pg.sprite.spritecollide(self.juego.luffy, self.juego.grupo_items_puntos, True)
            for item in colision_con_item_score:
                
                self.puntaje_jugador += self.puntaje.agarrar_item(item.puntaje)
                
                self.sonido_item_puntos.set_volume(0.15)
                self.sonido_item_puntos.play()
            

            colision_con_item_vida = pg.sprite.spritecollide(self.juego.luffy, self.juego.grupo_items_vida, True)
            for item_1 in colision_con_item_vida:

                self.total_vidas +=self.juego.luffy.agarrar_vida()
                
                self.sonido_item_vida.set_volume(0.15)
                self.sonido_item_vida.play()
            
            #colision de personaje con estructuras
            for estructura in self.juego.lista_estructuras:
                if self.juego.luffy.verificar_colision([estructura]):
                    self.juego.luffy.ajustar_a_plataforma(estructura.get_rect())
            #vulnerabilidad de personaje
            if self.juego.luffy.invulnerable:
                tiempo_transcurrido = pg.time.get_ticks() - self.juego.luffy.tiempo_invulnerable_actual
                if tiempo_transcurrido >= self.juego.luffy.tiempo_invulnerable:
                    self.juego.luffy.invulnerable = False
                
            #persona con enemigo colision
            colision_personaje_con_enemigo = pg.sprite.spritecollide(self.juego.luffy, self.juego.grupo_enemigos, False)
            for colision in colision_personaje_con_enemigo:
                
                if not self.juego.luffy.invulnerable:
                    self.juego.luffy.perdida_de_vidas()
            if self.juego.luffy.vidas < 1:
                    juego_ejecutandose = False
                    self.pantalla.fill((0, 0, 0))
                    texto_victoria = font.render(f"Te han Matado... DERRORTA", True, (255,255,255))
                    texto_puntaje_victoria = font.render(f"Puntaje: {self.puntaje.obtener_puntaje()}", True, (255,255,255))
                    self.pantalla.blit(texto_puntaje_victoria,(100, ALTO_VENTANA // 2))
                    self.pantalla.blit(texto_victoria, (ANCHO_VENTANA // 2 - texto_victoria.get_width() // 1, ALTO_VENTANA // 2 - texto_victoria.get_height() // 1))
                    pg.display.flip()
                    pg.time.delay(3000)
            
            #colision jugador con trampa
            colision_jugador_con_trampa = pg.sprite.spritecollide(self.juego.luffy, self.juego.grupo_trampas, False)
            for trampa in colision_jugador_con_trampa:
                
                if not self.juego.luffy.invulnerable:
                    self.juego.luffy.perdida_de_vidas()
            if self.juego.luffy.vidas < 1:
                    juego_ejecutandose = False
                    self.pantalla.fill((0, 0, 0))
                    texto_victoria = font.render(f"Te han Matado... DERRORTA", True, (255,255,255))
                    texto_puntaje_victoria = font.render(f"Puntaje: {self.puntaje.obtener_puntaje()}", True, (255,255,255))
                    self.pantalla.blit(texto_puntaje_victoria,(100, ALTO_VENTANA // 2))
                    self.pantalla.blit(texto_victoria, (ANCHO_VENTANA // 2 - texto_victoria.get_width() // 1, ALTO_VENTANA // 2 - texto_victoria.get_height() // 1))
                    pg.display.flip()
                    pg.time.delay(3000)
            
            self.pantalla.blit(self.juego.fondo_carga,(0,0))
            self.pantalla.blit(tiempo_juego,(ANCHO_VENTANA//2, 10))
            self.juego.luffy.update(delta_ms, lista_eventos, self.pantalla, self.juego.lista_estructuras)
            self.juego.update(self.pantalla)
            self.juego.luffy.gravedad_activa()
            
            self.pantalla.blit(self.icono_vida,(0, 35))
            self.pantalla.blit(texto_puntaje, (10, 15))
            self.pantalla.blit(texto_vidas, (25,35))
            
            pg.display.update()
            
        #juego.parar_musica() 
    pg.quit()



