import pygame
import random


pygame.init()


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Carrera de Coches-Grupo2")


WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
YELLOW = (255, 255, 0)
LIGHT_YELLOW = (255, 255, 153)

font = pygame.font.Font(None, 50)

background_image = pygame.image.load("fondo.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    
def show_menu():
    screen.fill(GRAY)
    screen.blit(background_image, (0, 0))
    title_text = font.render("Carrera de Coches", True, BLACK)
    
    start_text = font.render("Presiona ENTER para iniciar", True, BLACK)
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//3))
    screen.blit(start_text, (WIDTH//2 - start_text.get_width()//2, HEIGHT//2))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False



def restart_game():
    global car_x, obstacles, score, level, next_level_score, obstacle_speed
    car_x = WIDTH // 2 - car_width // 2
    obstacles = []
    for _ in range(num_obstacles):
        obstacles.append([random.randint(WIDTH//4, 3*WIDTH//4 - obstacle_width), random.randint(-HEIGHT, 0)])
    score = 0
    level = 1
    next_level_score = 5
    obstacle_speed = 5


car_width, car_height = 50, 80
car_x = WIDTH // 2 - car_width // 2
car_y = HEIGHT - car_height - 20
car_speed = 5


obstacle_width, obstacle_height = 20, 50
obstacles = []
obstacle_speed = 4
num_obstacles = 4
for _ in range(num_obstacles):
    obstacles.append([random.randint(WIDTH//4, 3*WIDTH//4 - obstacle_width), random.randint(-HEIGHT, 0)])

score = 0

# Niveles
level = 1
next_level_score = 5


show_menu()


running = True
clock = pygame.time.Clock()
while running:
    screen.fill(GRAY)
    

    pygame.draw.rect(screen, BLACK, (WIDTH//4, 0, WIDTH//2, HEIGHT))
    for i in range(0, HEIGHT, 40):
        pygame.draw.rect(screen, YELLOW, (WIDTH//2 - 5, i, 10, 30))
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
 
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and car_x > WIDTH//4:
        car_x -= car_speed
    if keys[pygame.K_RIGHT] and car_x < 3*WIDTH//4 - car_width:
        car_x += car_speed
    

    for obstacle in obstacles:
        obstacle[1] += obstacle_speed
        if obstacle[1] > HEIGHT:
            obstacle[1] = random.randint(-HEIGHT, 0)
            obstacle[0] = random.randint(WIDTH//4, 3*WIDTH//4 - obstacle_width)
            score += 1
            obstacle_speed += 0.2
    

    car_rect = pygame.Rect(car_x, car_y, car_width, car_height)
    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], obstacle_width, obstacle_height)
        if car_rect.colliderect(obstacle_rect):
            print(f"¡Has chocado! Puntuación final: {score}")
            screen.fill(BLACK)
            game_over_text = font.render("¡Has chocado! Presiona R para reiniciar", True, WHITE)
            screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2))
            pygame.display.flip()
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        restart_game()
                        waiting = False
    

    if score >= next_level_score:
        level += 1
        next_level_score += 5
        num_obstacles += 0.2
        obstacles.append([random.randint(WIDTH//4, 3*WIDTH//4 - obstacle_width), random.randint(-HEIGHT, 0)])
        obstacle_speed += 0.3

    pygame.draw.rect(screen, BLUE, (car_x, car_y, car_width, car_height), border_radius=5)
    pygame.draw.polygon(screen, LIGHT_YELLOW, [(car_x + 5, car_y), (car_x, car_y - 10), (car_x + 10, car_y)])
    pygame.draw.polygon(screen, LIGHT_YELLOW, [(car_x + car_width - 5, car_y), (car_x + car_width, car_y - 10), (car_x + car_width - 10, car_y)])

    for obstacle in obstacles:
        pygame.draw.rect(screen, RED, (obstacle[0], obstacle[1], obstacle_width, obstacle_height), border_radius=10)


    score_text = font.render(f"Puntos: {score}  Nivel: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
