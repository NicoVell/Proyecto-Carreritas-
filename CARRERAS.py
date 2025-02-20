import pygame
import random

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
ANCHO, ALTO = 900, 700
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Carreras Retro")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)

# Cargar imágenes y sonidos
fondo = pygame.image.load("fondo_carretera.png")
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO * 2))  # Doble de altura para efecto de movimiento
coche_jugador = pygame.image.load("coche.png")
coche_jugador = pygame.transform.scale(coche_jugador, (50, 100))
coche_oponente = pygame.image.load("coche_oponente.png")
coche_oponente = pygame.transform.scale(coche_oponente, (50, 100))
sonido_colision = pygame.mixer.Sound("colision.wav")
sonido_fondo = pygame.mixer.Sound("musica_fondo.wav")
sonido_fondo.play(-1)

# Clase Jugador
class Jugador:
    def __init__(self, x, y, imagen):
        self.x = x
        self.y = y
        self.velocidad = 5
        self.imagen = imagen
        self.puntaje = 0

    def mover(self, teclas, izq, der):
        if teclas[izq] and self.x > 0:
            self.x -= self.velocidad
        if teclas[der] and self.x < ANCHO - 50:
            self.x += self.velocidad
    
    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, (self.x, self.y))

# Clase Obstáculo
class Obstaculo:
    def __init__(self, velocidad):
        self.x = random.randint(0, ANCHO - 50)
        self.y = -100
        self.velocidad = velocidad
        self.ancho = 50
        self.alto = 100

    def mover(self):
        self.y += self.velocidad

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, ROJO, (self.x, self.y, self.ancho, self.alto))

# Pantalla de inicio
def pantalla_inicio():
    pantalla.fill(NEGRO)
    fuente = pygame.font.Font(None, 50)
    texto = fuente.render("Presiona ENTER para comenzar", True, BLANCO)
    pantalla.blit(texto, (ANCHO // 6, ALTO // 2))
    pygame.display.flip()
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    esperando = False

# Pantalla de Game Over
def game_over():
    pantalla.fill(NEGRO)
    fuente = pygame.font.Font(None, 50)
    texto = fuente.render("¡Game Over! Presiona R para reiniciar", True, BLANCO)
    pantalla.blit(texto, (ANCHO // 10, ALTO // 2))
    pygame.display.flip()
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    esperando = False

# Función principal del juego
def juego():
    reloj = pygame.time.Clock()
    jugador1 = Jugador(ANCHO // 3 - 25, ALTO - 150, coche_jugador)
    jugador2 = Jugador(2 * ANCHO // 3 - 25, ALTO - 150, coche_oponente)
    nivel = 1
    velocidad_obstaculos = 5
    obstaculos = [Obstaculo(velocidad_obstaculos)]
    corriendo = True
    pantalla_inicio()
    tiempo_inicio = pygame.time.get_ticks()
    
    fondo_y = 0  # Posición inicial del fondo

    while corriendo:
        pantalla.blit(fondo, (0, fondo_y))
        pantalla.blit(fondo, (0, fondo_y - ALTO))
        fondo_y += 5  # Velocidad de desplazamiento del fondo
        if fondo_y >= ALTO:
            fondo_y = 0  # Reinicio del fondo para efecto infinito
        
        teclas = pygame.key.get_pressed()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
        
        jugador1.mover(teclas, pygame.K_a, pygame.K_d)
        jugador2.mover(teclas, pygame.K_LEFT, pygame.K_RIGHT)
        
        jugador1.dibujar(pantalla)
        jugador2.dibujar(pantalla)
        
        for obstaculo in obstaculos:
            obstaculo.mover()
            obstaculo.dibujar(pantalla)
            if obstaculo.y > ALTO:
                obstaculos.remove(obstaculo)
                obstaculos.append(Obstaculo(velocidad_obstaculos))
                jugador1.puntaje += 1
                jugador2.puntaje += 1
                if jugador1.puntaje % 5 == 0:
                    nivel += 1
                    velocidad_obstaculos += 1

            if ((jugador1.y < obstaculo.y + obstaculo.alto and jugador1.y + 100 > obstaculo.y and
                jugador1.x < obstaculo.x + obstaculo.ancho and jugador1.x + 50 > obstaculo.x) or
                (jugador2.y < obstaculo.y + obstaculo.alto and jugador2.y + 100 > obstaculo.y and
                jugador2.x < obstaculo.x + obstaculo.ancho and jugador2.x + 50 > obstaculo.x)):
                sonido_colision.play()
                game_over()
                return juego()
        
        tiempo_transcurrido = (pygame.time.get_ticks() - tiempo_inicio) // 1000
        fuente = pygame.font.Font(None, 36)
        texto_tiempo = fuente.render(f"Tiempo: {tiempo_transcurrido}s", True, BLANCO)
        texto_puntaje = fuente.render(f"Puntaje J1: {jugador1.puntaje}  J2: {jugador2.puntaje}", True, BLANCO)
        texto_nivel = fuente.render(f"Nivel: {nivel}", True, BLANCO)
        pantalla.blit(texto_tiempo, (10, 10))
        pantalla.blit(texto_puntaje, (10, 50))
        pantalla.blit(texto_nivel, (10, 90))
        
        pygame.display.flip()
        reloj.tick(30)
    
    pygame.quit()

if __name__ == "__main__":
    juego()
