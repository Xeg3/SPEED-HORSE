import pygame

pygame.init()

from clases_juego import MenuModalidad, Usuario
from config import *


def correr_juego():
    
    usuario = Usuario(1000)
    MenuModalidad(screen, usuario).ejecutar()

correr_juego()