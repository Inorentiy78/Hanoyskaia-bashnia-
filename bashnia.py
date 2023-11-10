не закончен
import pygame
import sys

# Инициализация Pygame
pygame.init()

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Размеры окна
WIDTH, HEIGHT = 800, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ханойская башня")

# Размеры дисков
BASE_WIDTH = 100 # Базовая ширина для самого большого диска
DISK_HEIGHT = 20
DISK_SPACING = 5

# Словарь для хранения текущих позиций дисков
disk_positions = {
    "A": [],
    "B": [],
    "C": [],
    "D": [],
    "E": [],
    "F": []
}

# Функция для создания начальных позиций дисков на башнях
def initialize_positions():
    for tower, disks in towers.items():
        x = 0
        if tower == "A":
            x = WIDTH // 12
        elif tower == "B":
            x = WIDTH // 12 * 3
        elif tower == "C":
            x = WIDTH // 12 * 5
        elif tower == "D":
            x = WIDTH // 12 * 7
        elif tower == "E":
            x = WIDTH // 12 * 9
        elif tower == "F":
            x = WIDTH // 12 * 11

        y = HEIGHT - DISK_HEIGHT
        for disk in disks:
            disk_positions[tower].append((x - disk * 2, y, BASE_WIDTH + disk * 4, DISK_HEIGHT))
            y -= DISK_HEIGHT + DISK_SPACING

# Функция отрисовки башен и дисков
def draw():
    WIN.fill(WHITE)

    for tower, disks in towers.items():
        for pos in disk_positions[tower]:
            pygame.draw.rect(WIN, RED, pos)

    pygame.display.update()

towers = {
    "A": [i for i in range(6, 0, -1)],
    "B": [],
    "C": [],
    "D": [],
    "E": [],
    "F": []
}

initialize_positions()

selected_tower = None
selected_disk = None

# Основной цикл игры
running = True
while running:
    draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            for tower, pos_list in disk_positions.items():
                for pos in pos_list:
                    disk_rect = pygame.Rect(pos)
                    if disk_rect.collidepoint(x, y):
                        if not selected_tower:
                            selected_tower = tower
                            selected_disk = towers[tower].pop()
                            break
                        else:
                            if (not towers[tower] or towers[tower][-1] > selected_disk) and tower != selected_tower:
                                towers[tower].append(selected_disk)
                            else:
                                towers[selected_tower].append(selected_disk)
                            selected_tower = None
                            selected_disk = None

    pygame.display.update()

pygame.quit()
sys.exit()
