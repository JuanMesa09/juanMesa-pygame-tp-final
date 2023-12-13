import pygame as pg
import sys,os
from booton import Bootton
from input_box import InputBox

ruta= r"C:\Users\Juan\OneDrive\Escritorio\proyecto test"
sys.path.append(ruta)
from clase_game import Game

pg.init()

ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600






pantalla = pg.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pg.display.set_caption("Menu")

# Añadí una barra invertida adicional para la ruta de la fuente
fondo_menu = pg.transform.scale(pg.image.load(r"imagenes\img_fondo\fondo_menu.png"), (ANCHO_PANTALLA, ALTO_PANTALLA))

def get_font(tamanio):
    font_panth_1 = "./font\Silkscreen-Bold.ttf"
    font_panth_2 = "./font/Silkscreen-Regular.ttf"

    try:
        font_1 = pg.font.Font(font_panth_1, tamanio)
        font_2 = pg.font.Font(font_panth_2, tamanio)
        return font_1
    except pg.error:
        print("Error al cargar font")
        return None

def apreto_play():
    pg.display.set_caption("play")
    nombre_jugador = ""
    entrada_activa = False
    input_box = InputBox(300,300,200,40,get_font(30))

    while True:
        PLAY_MOUSE_POS = pg.mouse.get_pos()

        pantalla.blit(fondo_menu, (0,0))

        PLAY_TEXT = get_font(50).render("iniciar Juego", True, "Black")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(400,200))
        pantalla.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Bootton(image=None, pos=(700, 500), text_input="Atras", font=get_font(45),
                            base_color="Black", color="Red")
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(pantalla)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
            if event.type == pg.KEYDOWN:
                
                if entrada_activa:
                    
                    if event.key == pg.K_RETURN:
                        entrada_activa = False
                    
                    nivel_seleccionado = entrar_al_nivel(nombre_jugador)
                    if nivel_seleccionado is not None:

                        iniciar_juego(nombre_jugador, nivel_seleccionado)
                        return
                    elif event.key == pg.K_BACKSPACE:
                        nombre_jugador = nombre_jugador[:-1]
                    else:
                        nombre_jugador += event.unicode

                elif event.key == pg.K_RETURN:
                    entrada_activa = True

            if input_box.is_enter_pressed(event):
                entrada_activa = False
                nombre_jugador = input_box.text
                nivel_seleccionado = entrar_al_nivel(nombre_jugador)
                if nivel_seleccionado is not None:
                    iniciar_juego(nombre_jugador, nivel_seleccionado)
                    return

            input_box.handle_event(event)
    
        pantalla.blit(fondo_menu, (0,0))

        PLAY_TEXT = get_font(50).render("Iniciar Juego", True, "Black")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(400,200))
        pantalla.blit(PLAY_TEXT, PLAY_RECT)

        input_box.update()
        input_box.draw(pantalla)

        PLAY_BACK.changeColor(pg.mouse.get_pos())
        PLAY_BACK.update(pantalla)

        pg.display.update()

def entrar_al_nivel(jugador_nombre):
    nivel_seleccionado = None
    title_font = get_font(30)
    level_font = get_font(30)
    level_buttons = [
        Bootton(image=None, pos=(400, 300), text_input="Nivel 1", font=level_font, base_color="Black",
                color="Green"),
        Bootton(image=None, pos=(400, 345), text_input="Nivel 2", font=level_font, base_color="Black",
                color="Green"),
        Bootton(image=None, pos=(400, 390), text_input="Nivel 3", font=level_font, base_color="Black",
                color="Green")
            ]

    PLAY_BACK = Bootton(image=None, pos=(700, 500), text_input="Atras", font=get_font(45),
                        base_color="Black", color="Blue")

    while True:
        pantalla.blit(fondo_menu, (0, 0))

        title_text = title_font.render(f"Seleccion de nivel: {jugador_nombre}", True, "Black")
        title_rect = title_text.get_rect(center=(400, 200))
        pantalla.blit(title_text, title_rect)

        PLAY_BACK.changeColor(pg.mouse.get_pos())
        PLAY_BACK.update(pantalla)

        for button in level_buttons:
            button.changeColor(pg.mouse.get_pos())
            button.update(pantalla)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(pg.mouse.get_pos()):
                    return None

                for button in level_buttons:
                    if button.checkForInput(pg.mouse.get_pos()):
                        nivel_seleccionado = button.text_input
                        return nivel_seleccionado

        pg.display.update()

def apreto_opcion():
    pg.display.set_caption("Options")

    while True:
        OPTIONS_MOUSE_POS = pg.mouse.get_pos()

        pantalla.blit(fondo_menu, (0,0))
    
        OPTIONS_TEXT = get_font(45).render("Configuracion", True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(400,200))
        pantalla.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Bootton(image=None, pos=(700,500), text_input="Atras", font=get_font(45), base_color="White",
                            color="Blue")
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(pantalla)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
        pg.display.update()

def iniciar_juego(jugador_nombre, nivel_seleccionado):
    # Instancio de la clase Juego 
    juego = Game(jugador_nombre, nivel_seleccionado)
    
    juego.ejecutar_juego()
    
    print(f"Juego terminado para {jugador_nombre} en el nivel {nivel_seleccionado}")
def main_menu():

    while True:
        pantalla.blit(fondo_menu, (0,0))
        posicion_mouse = pg.mouse.get_pos()
        menu_texto = get_font(40).render("Menu de opciones", True, "Pink")
        menu_rect = menu_texto.get_rect(center=(400,200))

        PLAY_BOTOOM = Bootton(image=None, pos=(420,280),
                        text_input="PLAY", font=get_font(25), base_color="Blue", color="White")
        
        OPTIONS_BOTOOM = Bootton(image=None, pos=(420,340),
                                text_input="OPTIONS", font=get_font(25), base_color="Red", color="White")
        
        QUIT_BOTTOM = Bootton(image=None, pos=(415, 400),
                            text_input="QUIT", font=get_font(25), base_color="Green", color="White")
        
        pantalla.blit(menu_texto, menu_rect)

        for button in [PLAY_BOTOOM, OPTIONS_BOTOOM, QUIT_BOTTOM]:
            button.changeColor(posicion_mouse)
            button.update(pantalla)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if PLAY_BOTOOM.checkForInput(posicion_mouse):
                    apreto_play()
                if OPTIONS_BOTOOM.checkForInput(posicion_mouse):
                    apreto_opcion()
                if QUIT_BOTTOM.checkForInput(posicion_mouse):
                    pg.quit()
                    sys.exit()

        pg.display.update()

main_menu()
