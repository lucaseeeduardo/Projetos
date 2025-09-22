# tocando um MP3
import pygame
# verifique abaixo que, se eu inicializar o mixer depois do pygame, não funciona kk n sei pq
# mas o correto é o mixer init e dps o pygame init, procurar o motivo
# --------------------------------------------------------------------------------------------
# aqui inicializo o mixer do PyGame
pygame.mixer.init()
# aqui inicializo o PyGame
pygame.init()

pygame.mixer.music.load('ex021music.mp3')
pygame.mixer.music.play()
pygame.event.wait()
