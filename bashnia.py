import pygame
import sys

class Disk:
    def __init__(self, size, color):
        self.size = size
        self.color = color

class SettingsWindow:
    def __init__(self):
        self.num_disks = 5
        self.is_start_phase = True
        self.button_rect = pygame.Rect(50, 50, 200, 50)
        self.start_button_rect = pygame.Rect(50, 120, 250, 50)

    def draw(self, screen):
        font = pygame.font.Font(None, 35)
        text = font.render("Количество дисков:", True, (0, 0, 0))
        text_num = font.render(str(self.num_disks), True, (0, 0, 0))

        text_width = text.get_width() + text_num.get_width() + 20
        pygame.draw.rect(screen, (200, 200, 200), self.button_rect)
        screen.blit(text, (self.button_rect.x + 10, self.button_rect.centery - text.get_height() // 2))
        screen.blit(text_num, (self.button_rect.right - text_num.get_width() - 10, self.button_rect.centery - text_num.get_height() // 2))

        if self.is_start_phase:
            start_text = font.render("Пуск", True, (0, 255, 0))
            pygame.draw.rect(screen, (0, 255, 0), self.start_button_rect)
            screen.blit(start_text, (self.start_button_rect.x + 10, self.start_button_rect.centery - start_text.get_height() // 2))

    def check_button_click(self, pos):
        if self.is_start_phase and self.start_button_rect.collidepoint(pos):
            self.is_start_phase = False
        elif self.button_rect.collidepoint(pos):
            self.num_disks += 1
            if self.num_disks > 10:
                self.num_disks = 1

class GameWindow:
    def __init__(self, num_disks):
        self.towers = create_towers(num_disks)

    def draw(self, screen):
        for i, tower in enumerate(self.towers):
            x = i * 200 + (800 - 3 * 200) // 2
            pygame.draw.rect(screen, (0, 0, 0), (x, 400 - 200, 10, 200))
            for j, disk in enumerate(tower):
                disk_width = disk.size * 30
                disk_height = 20
                pygame.draw.rect(
                    screen,
                    disk.color,
                    (x - disk_width // 2 + 10 // 2, 400 - (j + 1) * disk_height, disk_width, disk_height),
                )

def create_towers(num_disks):
    return [
        [Disk(num_disks - i, (255, 255 - (25 * i), 20 * i)) for i in range(num_disks)],
        [],
        []
    ]

def main():
    pygame.init()
    WIDTH, HEIGHT = 800, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Ханойская башня")

    settings_window = SettingsWindow()
    game_window = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                settings_window.check_button_click(mouse_pos)

        screen.fill((255, 255, 255))

        if settings_window.is_start_phase:
            settings_window.draw(screen)
        else:
            if game_window is None:
                game_window = GameWindow(settings_window.num_disks)
            game_window.draw(screen)

        pygame.display.flip()

if __name__ == "__main__":
    main()
