import pygame


# Configuración de pantalla

ANCHO, ALTO = 1280, 720
FPS = 60

screen=pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Carrera de Caballos')


# Colores

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)


# Fuentes globales para textos

FUENTE_INPUT = pygame.font.Font(None, 24)
FUENTE1 = pygame.font.Font("Recurso_generales/caballos/fonts/Race Sport.ttf", 28)
FUENTE2 = pygame.font.Font("Recurso_generales/caballos/fonts/Race Sport.ttf", 15)
FUENTE_CONTEO = pygame.font.Font("Recurso_generales/caballos/fonts/Race Sport.ttf", 200)


#Variables de juego

META = ANCHO-80