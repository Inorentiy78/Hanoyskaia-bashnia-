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
def draw_disk_button(num_disks, is_start_button):
    font = pygame.font.Font(None, 35)
    text = font.render("Количество дисков", True, BLACK)
    text_num = font.render(str(num_disks), True, BLACK)

    text_width = text.get_width() + text_num.get_width() + 20  # Calculate total width for the text and spacing
    button_rect = pygame.Rect(50, 50, text_width, 50)  # Use calculated text width

    pygame.draw.rect(screen, (200, 200, 200), button_rect)
    screen.blit(text, (button_rect.x + 10, 60))  # Adjust text position based on the button rectangle
    screen.blit(text_num, (button_rect.right - text_num.get_width() - 10, 60))  # Adjust the 'num_disks' position

    if is_start_button:
        start_text = font.render("Пуск", True, BLACK)
        start_button_rect = pygame.Rect(50, 120, 250, 50)
        pygame.draw.rect(screen, (0, 255, 0), start_button_rect)  # Green color for the start button
        screen.blit(start_text, (start_button_rect.x + 10, 130))

        return button_rect, start_button_rect  # Return both button rectangles for click check
    else:
        return button_rect 
is_start_phase = True  # Initial state
num_disks = 5


# Функция для проверки нажатия на кнопку числа дисков
def check_disk_button(pos):
    if 50 <= pos[0] <= 200 and 50 <= pos[1] <= 100:
        return True
    return False

is_start_phase = True  # Initial state
num_disks = 5
towers = create_towers(num_disks)

def main():
    clock = pygame.time.Clock()
    global is_start_phase
    global num_disks
    global towers

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if not is_start_phase and 50 <= mouse_pos[0] <= 200 and 50 <= mouse_pos[1] <= 100:
                    # Check if the mouse is in the disk selection button area only when it's not the start phase
                    num_disks += 1  # Increment the number of disks
                    if num_disks > 10:  # Limit the number of disks to 10
                        num_disks = 1

                    # Update towers with the new number of disks
                    towers = create_towers(num_disks)
                elif is_start_phase:
                    button_rect, start_button_rect = draw_disk_button(num_disks, is_start_button=True)
                    if start_button_rect.collidepoint(mouse_pos):
                        is_start_phase = False

        screen.fill(WHITE)
        draw_towers()
        if is_start_phase:
            draw_disk_button(num_disks, is_start_button=True)  # Draw the start button
        else:
            draw_disk_button(num_disks, is_start_button=False)  # Draw the disk selection button
            # Perform other actions based on user input (e.g., move disk)

        pygame.display.flip()
        clock.tick(30)
                    


if __name__ == "__main__":
    main()



"""if event.type == pygame.KEYDOWN:
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
                        move_disk(2, 1)"""
