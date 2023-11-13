import pygame
import sys

# Инициализация Pygame
pygame.init()

# Определение цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Определение параметров дисков
DISK_WIDTH = 30
DISK_HEIGHT = 20

# Определение параметров башен
TOWER_WIDTH = 10
TOWER_HEIGHT = 200
TOWER_SPACING = 200  # Изменено на более широкий интервал

# Определение параметров окна
WIDTH = 800  # Увеличено для увеличения ширины столбцов
HEIGHT = 400

# Инициализация экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ханойская башня")

class Disk:
    def __init__(self, size, color):
        self.size = size
        self.color = color

# Определение дисков и башен
towers = [[Disk(5, (255, 0, 0)), Disk(4, (255, 255, 0)), Disk(3, (0, 255, 0)), Disk(2, (0, 255, 255)), Disk(1, (0, 0, 255))], [], []]

# Определение функции отрисовки башен и дисков
def draw_towers():
    for i, tower in enumerate(towers):
        x = i * TOWER_SPACING + (WIDTH - 3 * TOWER_SPACING) // 2  # Разместить столбцы в центре
        pygame.draw.rect(screen, BLACK, (x, HEIGHT - TOWER_HEIGHT, TOWER_WIDTH, TOWER_HEIGHT))
        for j, disk in enumerate(tower):
            disk_width = disk.size * DISK_WIDTH
            disk_height = DISK_HEIGHT
            pygame.draw.rect(screen, disk.color, (x - disk_width // 2 + TOWER_WIDTH // 2, HEIGHT - (j + 1) * disk_height, disk_width, disk_height))

# Определение функции перемещения диска
def move_disk(source, target):
    if towers[source] and (not towers[target] or towers[source][-1].size < towers[target][-1].size):
        disk = towers[source].pop()
        towers[target].append(disk)

# Определение главного цикла игры
def main():
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Обработка событий клавиш
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    move_disk(0, 1)
                elif event.key == pygame.K_2:
                    move_disk(0, 2)
                elif event.key == pygame.K_3:
                    move_disk(1, 0)
                elif event.key == pygame.K_4:
                    move_disk(1, 2)
                elif event.key == pygame.K_5:
                    move_disk(2, 0)
                elif event.key == pygame.K_6:
                    move_disk(2, 1)

        # Отрисовка
        screen.fill(WHITE)
        draw_towers()
        pygame.display.flip()

        # Ограничение частоты кадров
        clock.tick(30)

if __name__ == "__main__":
    main()
