import pygame as py
from config import *

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
            text_surface = self.font2.render(self.mensaje, True, (BLANCO))
        else:
            text_surface = self.font.render(self.mensaje2, True, (BLANCO))
        

        screen.blit(text_surface, (self.rect.x+2, self.rect.y+6))

    def verificacion(self, var, opcion):
        if opcion == 1:
            if self.mensaje in var:
                if not self.cont:
                    caballo=self.mensaje
                    self.cont = True
                    self.active = False
                    self.mensaje=f'Eligió al Caballo #{caballo}'
                    return caballo
            else:
                self.mensaje2="No válido, intente de nuevo"
                self.mensaje=''
                
        else:
            try:
                monto = float(self.mensaje.strip())
                if 100 <= monto <= var:
                    if not self.cont:
                        self.cont = True
                        self.active = False
                        self.mensaje=f'Monto = {monto}$'
                        return monto
                else:
                    self.mensaje2="No válido, intente de nuevo"
                    self.mensaje=''
            except ValueError:
                self.mensaje2="No válido, intente de nuevo"
                self.mensaje=''