import pygame
import sys
import datos_caballos as dc
from button import Button
from Inputbox import Caja
from config import *


clock = pygame.time.Clock()


class Usuario:
    def __init__(self, saldo):
        self.__saldo = saldo

    def apostar(self, apuesta):
        if 0 < apuesta <= self.__saldo: 
            self.__saldo -= apuesta
            return apuesta
        else:
            return 0 

    def mostrar_saldo(self):
        texto=f'{self.__saldo:.2f}'
        return texto

    def agregar_saldo(self, cantidad):
        if cantidad > 0:
            self.__saldo += cantidad


class Caballo:
    caballo_sprite = pygame.image.load("Recurso_generales/caballos/sprites/rival.png")
    caballo_sprite_elegido = pygame.image.load("Recurso_generales/caballos/sprites/jugador.png")
    
    def __init__(self, nombre_genero, peso, edad, altura, cuotas_saltos_velocidad, etiqueta, posicion_y):
        self.__nombre_genero = nombre_genero
        self.__peso = peso
        self.__edad = edad
        self.__altura = altura
        self.__cuotas_saltos_velocidad = cuotas_saltos_velocidad
        self.__etiqueta = etiqueta
        self.posicion_y = posicion_y

        self.spritesheet = self.caballo_sprite
        self.frames = self.cargar_frames(34, 34, 6)
        self.frame_actual = 0
        self.contador_animacion = 0

    def __str__(self):
        return f'CABALLO #{self.__etiqueta}'

    def get_etiqueta(self):
        return self.__etiqueta

    def get_cuota(self):
        return self.__cuotas_saltos_velocidad[0]

    def get_velocidad(self):
        return self.__cuotas_saltos_velocidad[2]

    def obtener_datos(self):
        return [f' Nombre: {self.__nombre_genero[0]}',
               f' Género: {self.__nombre_genero[1]}',
               f' Peso: {self.__peso} Kgs',
               f' Edad: {self.__edad} años',
               f' Altura: {self.__altura} mts',
               f' Velocidad: {self.__cuotas_saltos_velocidad[2]} Km/h',
               f' Cuota: {self.__cuotas_saltos_velocidad[0]}']

    def cargar_frames(self, ancho, alto, cantidad):

        frames = []
        for i in range(cantidad):
            frame = self.spritesheet.subsurface(pygame.Rect(i * ancho, 0, ancho, alto))
            frames.append(pygame.transform.scale(frame, (68, 68)))
        return frames

    def dibujar(self, caballo_apuesta):

        if str(self.__etiqueta) == str(caballo_apuesta): 
            if self.spritesheet != self.caballo_sprite_elegido:
                self.spritesheet = self.caballo_sprite_elegido
                self.frames = self.cargar_frames(34, 34, 6)
        else:
            if self.spritesheet != self.caballo_sprite:
                self.spritesheet = self.caballo_sprite
                self.frames = self.cargar_frames(34, 34, 6)  

        screen.blit(self.frames[self.frame_actual], (self.posicion, self.posicion_y))

    def correr(self):

        suma = self.posicion + dc.choice(self.__cuotas_saltos_velocidad[1])
        self.posicion = min(suma, META)

        self.contador_animacion += 1
        if self.contador_animacion >= 5:
            self.frame_actual = (self.frame_actual + 1) % 6
            self.contador_animacion = 0

    def reiniciar(self):
        self.posicion = 30
        self.frame_actual = 0


class Menu:
    def __init__(self, screen, usuario):
        self.screen = screen
        self.usuario = usuario
        self.fondo = pygame.image.load("Recurso_generales/caballos/images/cielo.jpg")
        self.sonido = GestorSonido()
        self.musica_menu = "Recurso_generales/caballos/sound/menu.mp3"
        self.sonido_click = "Recurso_generales/caballos/sound/click.mp3"

    def ejecutar(self):
        pass


class MenuModalidad(Menu):
    def __init__(self, screen, usuario):
        super().__init__(screen, usuario)
        self.sonido.reproducir_musica(self.musica_menu)

    def ejecutar(self):
        while True:
            mouse_menu = pygame.mouse.get_pos()
            self.screen.blit(self.fondo, (0, 0))

            title = Button(pygame.image.load('Recurso_generales/caballos/images/title_game.png'), (640, 90), None, FUENTE2, NEGRO, None)

            modalidades = [
                (2, "Recurso_generales/caballos/images/horse_2.png", (640, 200)),
                (4, "Recurso_generales/caballos/images/horse_4.png", (640, 375)),
                (8, "Recurso_generales/caballos/images/horse_8.png", (640, 550))
            ]
            modalidad_buttons = [Button(pygame.image.load(img), pos, None, FUENTE2, NEGRO, None) for _, img, pos in modalidades]

            button_saldo = Button(pygame.image.load('Recurso_generales/caballos/images/saldo_image.png'), (640, 680), f'SALDO: {self.usuario.mostrar_saldo()}', FUENTE1, NEGRO, None)
            back_button = Button(pygame.transform.scale(pygame.image.load("Recurso_generales/caballos/images/back_button.png"), (200, 80)), (1180, 675), None, FUENTE1, NEGRO, None)

            for btn in modalidad_buttons + [title, button_saldo, back_button]:
                btn.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for i, (modalidad, _, _) in enumerate(modalidades):
                        if modalidad_buttons[i].checkForInput(mouse_menu):
                            self.sonido.reproducir_sonido(self.sonido_click, 0.6)
                            self.caballos = generar_caballos(modalidad)
                            return MenuApuesta(self.screen, self.usuario, self.caballos).ejecutar()

                        elif back_button.checkForInput(mouse_menu):
                            self.sonido.detener_musica()
                            return            

            pygame.display.flip()


class MenuApuesta(Menu):
    def __init__(self, screen, usuario, caballos):
        super().__init__(screen, usuario)
        self.caballos = caballos
        self.caballo_apuesta = [None, None]

    def ejecutar(self):
        input_caballo = Caja(760, 200, 260, 40, ROJO, NEGRO, FUENTE_INPUT, FUENTE_INPUT, False, False)
        input_monto = Caja(760, 500, 260, 40, ROJO, NEGRO, FUENTE_INPUT, FUENTE_INPUT, False, False)
        caballo = None
        monto = 0
        activar_carrera=False

        while True:
            self.screen.blit(self.fondo, (0, 0))
            mostrar_caballos(self.caballos, self.screen)
            mouse_menu = pygame.mouse.get_pos()

            apuesta_button = Button(pygame.transform.scale(pygame.image.load("Recurso_generales/caballos/images/boton_caballo.png"), (610, 90)),(870, 100), None, FUENTE1, NEGRO, None)
            monto_button = Button(pygame.transform.scale(pygame.image.load("Recurso_generales/caballos/images/boton_monto.png"), (610, 90)), (870, 400), None, FUENTE1, NEGRO, None)
            
            if activar_carrera:
                carrera_salir_button = Button(pygame.transform.scale(pygame.image.load("Recurso_generales/caballos/images/carrera_button.png"), (310, 90)), (1110, 675), None, FUENTE1, NEGRO, None)
            else:
                carrera_salir_button = Button(pygame.transform.scale(pygame.image.load("Recurso_generales/caballos/images/back_button.png"), (200, 80)), (1180, 675), None, FUENTE1, NEGRO, None)
            button_saldo = Button(pygame.image.load('Recurso_generales/caballos/images/saldo_image.png'), (680, 680), f'SALDO: {float(self.usuario.mostrar_saldo()) - monto:.2f}', FUENTE1, NEGRO, None)

            for btn in [apuesta_button, monto_button, carrera_salir_button, button_saldo]:
                btn.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    input_caballo.activar(event)
                    input_monto.activar(event)

                    if carrera_salir_button.checkForInput(mouse_menu):
                        if activar_carrera:
                            self.sonido.reproducir_sonido(self.sonido_click, 0.6)
                            self.sonido.detener_musica()
                            apuesta = self.usuario.apostar(monto)
                            self.caballo_apuesta.extend([caballo, apuesta])
                            self.ha_apostado = True
                            return Carrera(self.screen, self.usuario, self.caballos, self.caballo_apuesta).ejecutar()
                        else:
                            self.sonido.reproducir_sonido(self.sonido_click, 0.6)
                            return MenuModalidad(self.screen, self.usuario).ejecutar()


                elif event.type == pygame.KEYDOWN:

                    if input_caballo.active and not input_caballo.cont:

                        if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                            caballo = input_caballo.verificacion(self.caballos, 1)
                            if caballo:
                                self.caballo_apuesta[0] = caballo

                        elif event.key == pygame.K_BACKSPACE:
                            input_caballo.mensaje = input_caballo.mensaje[:-1]
                        else:
                            input_caballo.mensaje += event.unicode

                    elif input_monto.active and not input_monto.cont:
                        if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                            
                            monto = input_monto.verificacion(float(self.usuario.mostrar_saldo()), 2) or 0
                            self.caballo_apuesta[1] = monto

                        elif event.key == pygame.K_BACKSPACE:
                            input_monto.mensaje = input_monto.mensaje[:-1]
                        else:
                            input_monto.mensaje += event.unicode

                    elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8):
                        self.sonido.reproducir_sonido(self.sonido_click, 0.6)
                        opcion = event.unicode
                        if opcion in self.caballos and not activar_carrera:
                            return MenuDatos(self.screen, self.usuario, self.caballos, opcion).ejecutar()                        

            for i in [input_caballo, input_monto]:
                i.cambia_color()
                i.dibujar(self.screen)

            if input_caballo.cont:
                check_button = Button(pygame.transform.scale(pygame.image.load("Recurso_generales/caballos/images/right.png"), (100, 100)), (1060, 220), None, FUENTE1, NEGRO, None)
                check_button.update(screen)

            if input_monto.cont:
                check_button2 = Button(pygame.transform.scale(pygame.image.load("Recurso_generales/caballos/images/right.png"), (100, 100)), (1060, 520), None, FUENTE1, NEGRO, None)
                check_button2.update(screen)

            if monto >= 100 and caballo in self.caballos:

                activar_carrera = True
                notificacion = Button(pygame.image.load("Recurso_generales/caballos/images/notificacion.png"), (610, 360), None, FUENTE1, NEGRO, None)
                notificacion.update(screen)        

            pygame.display.flip()


class MenuDatos(Menu):
    def __init__(self, screen, usuario, caballos, opcion):
        super().__init__(screen, usuario)
        self.caballos = caballos
        self.opcion = opcion

    def ejecutar(self):
        while True:
            mouse_datos = pygame.mouse.get_pos()
            self.screen.blit(self.fondo, (0, 0))

            title=Button(pygame.transform.scale(pygame.image.load("Recurso_generales/caballos/images/running_horse_2.png"), (600, 60)), (640, 35), f"Datos del caballo #{self.opcion}", FUENTE1, BLANCO, None)
            back_button=Button(pygame.transform.scale(pygame.image.load("Recurso_generales/caballos/images/back_button.png"), (200, 80)), (1180, 675), None, FUENTE1, NEGRO, None)

            for btn in [title, back_button]:
                btn.update(self.screen)

            y = ALTO/7
            for data in self.caballos[self.opcion].obtener_datos():
                horse_button = Button(pygame.transform.scale(pygame.image.load(f"Recurso_generales/caballos/images/color_{self.opcion}.png"), (520, 70)), (640, y), data, FUENTE1, BLANCO, None)
                horse_button.update(self.screen)
                y += 95

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN: 
                    if back_button.checkForInput(mouse_datos):
                        self.sonido.reproducir_sonido(self.sonido_click, 0.6)
                        return MenuApuesta(self.screen, self.usuario, self.caballos).ejecutar()

            pygame.display.flip()


class PantallaResultado(Menu):
    def __init__(self, screen, usuario, caballos, caballo_apuesta):
        super().__init__(screen, usuario)
        self.caballos = caballos
        self.caballo_apuesta = caballo_apuesta
        self.sonido_victoria = "Recurso_generales/caballos/sound/victoria.mp3"
        self.sonido_derrota = "Recurso_generales/caballos/sound/derrota.mp3"
        
    def ejecutar(self):
        ganador = max(self.caballos.items(), key=lambda item: item[1].posicion)[0]
        mensaje = ""
        caballo_apostado = self.caballo_apuesta[0]
        monto_apostado = self.caballo_apuesta[1]
        cuota = self.caballos[caballo_apostado].get_cuota()
        victoria = pygame.transform.scale_by(pygame.image.load("Recurso_generales/caballos/sprites/ganas.png"), (3))
        derrota = pygame.transform.scale_by(pygame.image.load("Recurso_generales/caballos/sprites/pierdes.png"), (3))

        if ganador == caballo_apostado:
            ganancias = monto_apostado * cuota
            mensaje = f"¡FELICIDADES! Ganaste ${ganancias:.2f}"
            self.usuario.agregar_saldo(ganancias)
            sonido_a_reproducir = self.sonido_victoria

        else:
            mensaje = "Has perdido..."
            sonido_a_reproducir = self.sonido_derrota

        button_saldo = Button(pygame.image.load('Recurso_generales/caballos/images/saldo_image.png'), (640, 680), f'SALDO: {self.usuario.mostrar_saldo()}', FUENTE1, NEGRO, None)
        back_button = Button(pygame.transform.scale(pygame.image.load("Recurso_generales/caballos/images/back_button.png"), (200, 80)), (1180, 675), None, FUENTE1, NEGRO, None)

        self.caballo_apuesta.clear()

        sonido_reproducido = False

        while True:
            mouse_menu = pygame.mouse.get_pos()
            self.screen.blit(self.fondo, (0, 0))

            if not sonido_reproducido:  
                self.sonido.reproducir_sonido(sonido_a_reproducir, 0.4)
                sonido_reproducido = True
            
            if ganador == caballo_apostado:
                self.screen.blit(victoria, (440, 250))
            else:
                self.screen.blit(derrota, (480, 280))

            resultado_button = Button(pygame.transform.scale(pygame.image.load("Recurso_generales/caballos/images/running_horse_2.png"), (700, 80)), (ANCHO / 2, ALTO / 6), mensaje, FUENTE1, BLANCO, None)

            for btn in [resultado_button, button_saldo, back_button]:
                btn.update(self.screen)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.checkForInput(mouse_menu):
                        return MenuModalidad(self.screen, self.usuario).ejecutar()


class GestorSonido:
    def __init__(self):
        pygame.mixer.init()
        self.sonidos = {}

    def reproducir_musica(self, archivo, loop=-1):

        if pygame.mixer.music.get_busy():
            return  

        pygame.mixer.music.load(archivo)
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(loop)

    def detener_musica(self):

        pygame.mixer.music.stop()

    def reproducir_sonido(self, archivo, volumen):
        
        if archivo not in self.sonidos:
            self.sonidos[archivo] = pygame.mixer.Sound(archivo)
            self.sonidos[archivo].set_volume(volumen)

        self.sonidos[archivo].play()

    def detener_sonido(self, archivo):
        
        if archivo in self.sonidos:
            self.sonidos[archivo].stop()


class Carrera:
    def __init__(self, screen, usuario, caballos, caballo_apuesta):
        self.screen = screen
        self.usuario = usuario
        self.caballos = caballos
        self.caballo_apuesta = caballo_apuesta
        self.fondo_carrera = pygame.transform.scale_by(pygame.image.load("Recurso_generales/caballos/sprites/fondo.png"),(2))
        self.sonido = GestorSonido()
        self.sonido_gradas = "Recurso_generales/caballos/sound/gradas.mp3"
        self.sonido_galope = "Recurso_generales/caballos/sound/galope.mp3"
        self.sonido_fincarrera = "Recurso_generales/caballos/sound/fin_carrera.mp3"
        

    def dibujar_escenario(self, screen):

        screen.blit(self.fondo_carrera, (0, 0))

        for caballo in self.caballos.values():  
            caballo.dibujar(self.caballo_apuesta[0]) 

        pygame.display.flip()


    def cuenta_regresiva(self, screen):
        
        for i in range(3, 0, -1):
            self.dibujar_escenario(screen)
            texto = FUENTE_CONTEO.render(str(i), True, BLANCO)
            rect = texto.get_rect(center=(ANCHO / 2, ALTO / 2))
            screen.blit(texto, rect) 

            pygame.display.flip()
            esperar(800)


    def ejecutar(self):
        for caballo in self.caballos.values():
            caballo.reiniciar()

        self.sonido.reproducir_sonido(self.sonido_gradas, 0.2)  
        self.cuenta_regresiva(screen)
        self.sonido.reproducir_sonido(self.sonido_galope, 0.2)   

        while True:
            
            self.screen.fill(BLANCO)
            self.screen.blit(self.fondo_carrera, (0, 0))

            for caballo in self.caballos.values():
                caballo.correr()
                caballo.dibujar(self.caballo_apuesta[0])

                if caballo.posicion >= META:
                    self.sonido.detener_sonido(self.sonido_gradas)
                    self.sonido.detener_sonido(self.sonido_galope)
                    self.sonido.reproducir_sonido(self.sonido_fincarrera, 0.6)
                    esperar(1750)
                    return PantallaResultado(self.screen, self.usuario, self.caballos, self.caballo_apuesta).ejecutar()

            pygame.display.flip()
            clock.tick(FPS)


def mostrar_caballos(caballos, screen):
    
    x=220
    y=125

    frame=Button(pygame.transform.scale(pygame.image.load("Recurso_generales/caballos/images/frame_list.png"), (400, 480)), (220, 280), None, FUENTE1, NEGRO, None)
    list_button=Button(None, (220, 80), 'CABALLOS - CUOTA', FUENTE1, BLANCO, None)
    info_button=Button(pygame.transform.scale(pygame.image.load("Recurso_generales/caballos/images/message.png"), (400, 150)), (220, 620), None, FUENTE1, NEGRO, None)

    for i in [frame, list_button, info_button]:
        i.update(screen)

    for c in caballos.values():
        texto=f'({c.get_etiqueta()}) {c} - {c.get_cuota():.2f}'
        button_carrera=Button(None, (x, y), texto, FUENTE1, BLANCO, None)
        button_carrera.update(screen)
        y+=50


def generar_caballos(cantidad):

    margen = 155
    return {str(i + 1): Caballo(dc.nombre_genero(), dc.peso(), dc.edad(), dc.altura(), dc.cuota_saltos_velocidad(modalidad=cantidad), i + 1, margen + i * 45)
            for i in range(cantidad)}


def esperar(tiempo):

    inicio_espera = pygame.time.get_ticks()
    while pygame.time.get_ticks() - inicio_espera < tiempo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()