import pygame as py
import funciones_tkinter as tk

class Caja():

    def __init__(self, x, y, w, h, color_active, color_inactive, font, font2, active, cont, mensaje='', mensaje2="Elija y presione ENTER"):
        self.x_pos=x
        self.y_pos=y
        self.color_active=color_active
        self.color_inactive=color_inactive
        self.color=color_inactive
        self.font=font
        self.font2=font2
        self.w=w
        self.h=h
        self.active=active
        self.cont=cont
        self.rect=py.Rect(x, y, w, h)
        self.mensaje=mensaje
        self.mensaje2=mensaje2
    

    def activar(self, event):
        if self.rect.collidepoint(event.pos) and not self.cont:
            self.active=True
            self.mensaje2=''
        else: self.active=False

    def cambia_color(self):
        if self.active:
            self.color=self.color_active
        else: 
            self.color=self.color_inactive

    def dibujar(self, screen):

        py.draw.rect(screen, self.color, self.rect)

        if self.mensaje2=='':
            text_surface = self.font2.render(self.mensaje, True, (255, 255, 255))
        else:
            text_surface = self.font.render(self.mensaje2, True, (255, 255, 255))
        

        screen.blit(text_surface, (self.rect.x+5, self.rect.y+5))

    def verificacion(self, var, opcion):
        if opcion == 1:
            if self.mensaje in var:
                if not self.cont:
                    caballo=self.mensaje
                    tk.text_info(f'Ha elegido al caballo #{caballo}')
                    self.cont = True
                    self.active = False
                    return caballo
            else:
                tk.text_error('Error, ingrese un caballo válido.')
        else:
            try:
                monto = float(self.mensaje.strip())
                if 100 <= monto <= var:
                    if not self.cont:
                        tk.text_info(f'Ha hecho una apuesta de {monto}$')
                        self.cont = True
                        self.active = False
                        return monto
                    else:
                        tk.text_info(f'Ya ha realizado una apuesta de {monto}$')
                        return monto
                else:
                    tk.text_error('Error, ingrese un monto válido.')
                    return None

            except ValueError:
                tk.text_error('Error, ingrese un monto válido.')
                return None