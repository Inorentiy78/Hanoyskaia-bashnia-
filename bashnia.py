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
towers = [[Disk(10, (255, 0, 0)), Disk(9, (255, 255, 0)), Disk(8, (0, 255, 0)), Disk(7, (0, 255, 255)), Disk(6, (0, 0, 255)), Disk(5, (255, 0, 255)), Disk(4, (255, 128, 0)), Disk(3, (128, 255, 0)), Disk(2, (0, 128, 255)), Disk(1, (128, 0, 255))],
     [], []]



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

def create_towers(num_disks):
    return [
        [Disk(num_disks - i, (255, 255 - (25 * i), 20 * i)) for i in range(num_disks)],
        [],
        []
    ]

# Функция для отрисовки кнопок с числом дисков
def draw_disk_button(num_disks):
    font = pygame.font.Font(None, 35)
    text = font.render("Количество дисков", True, BLACK)
    pygame.draw.rect(screen, (200, 200, 200), (50, 50, 250, 50))  # Button-like appearance
    screen.blit(text, (60, 60))
    text_num = font.render(str(num_disks), True, BLACK)
    screen.blit(text_num, ( 320, 60)) 

# Функция для проверки нажатия на кнопку числа дисков
def check_disk_button(pos):
    if 50 <= pos[0] <= 150 and 50 <= pos[1] <= 100:
        return True
    return False

# Определение главного цикла игры
def main():
    clock = pygame.time.Clock()
    num_disks = 5  # Default number of disks
    global towers
    towers = create_towers(num_disks) 
   

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if check_disk_button(mouse_pos):
                    num_disks = (num_disks % 10) + 1  # Изменение числа дисков при клике на кнопку
                    towers = create_towers(num_disks)  # Обновить башни при изменении числа дисков

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

        screen.fill(WHITE)
        draw_towers()
        draw_disk_button(num_disks)  # Отрисовка кнопки
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
