import pygame
import sys

class Disk:
    def __init__(self, size, color):
        self.size = size
        self.color = color
        self.rect = None  # Добавляем атрибут rect для представления прямоугольника
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0

class SettingsWindow:
    def __init__(self):
        self.num_disks = 5
        self.is_start_phase = True
        self.button_rect = pygame.Rect(50, 50, 300, 50)
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
            start_text = font.render("Пуск", True, (0, 0, 0))
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
        self.steps = []  # Добавляем список для хранения шагов
        self.dragging = False
        self.selected_disk = None
        self.offset_x = 0
        self.offset_y = 0

    def draw(self, screen):
        for i, tower in enumerate(self.towers):
            x = i * 200 + (800 - 3 * 200) // 2
            pygame.draw.rect(screen, (0, 0, 0), (x, 400 - 200, 10, 200))
            for j, disk in enumerate(tower):
                disk_width = disk.size * 30
                disk_height = 20
                if disk == self.selected_disk and self.dragging:
                    pygame.draw.rect(
                        screen,
                        disk.color,
                        (disk.rect.x + (x - disk.size * 15 + 10 // 2 - disk.rect.x) * 0.2,
                         disk.rect.y - (disk.rect.y - (400 - (j + 1) * 20)) * 0.2,
                         disk_width, disk_height),
                    )
                else:
                    pygame.draw.rect(
                        screen,
                        disk.color,
                        (x - disk_width // 2 + 10 // 2, 400 - (j + 1) * disk_height, disk_width, disk_height),
                    )

    def add_step(self, move_from, move_to):
        self.steps.append((move_from, move_to))

    def handle_events(self, event):
        target_tower_index = None  # Установите начальное значение переменной перед использованием

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for tower_index, tower in enumerate(self.towers):
                    if tower:  # Проверяем, что стопка не пуста
                        top_disk = tower[-1]
                        x = tower_index * 200 + (800 - 3 * 200) // 2
                        disk_rect = pygame.Rect(
                            x - top_disk.size * 15 + 10 // 2,
                            400 - len(tower) * 20,
                            top_disk.size * 30,
                            20,
                        )
                        if disk_rect.collidepoint(event.pos):
                            self.selected_disk = self.towers[tower_index].pop()
                            self.dragging = True
                            self.offset_x = event.pos[0] - disk_rect.x
                            self.offset_y = event.pos[1] - disk_rect.y

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.dragging and self.selected_disk is not None:
                    target_tower_index = int((event.pos[0] - 50) / 200)

                    if 0 <= target_tower_index < len(self.towers):
                        target_tower = self.towers[target_tower_index]
                        if not target_tower or (target_tower[-1] is not None and hasattr(target_tower[-1], 'size') and (not hasattr(self.selected_disk, 'size') or (self.selected_disk.size < target_tower[-1].size))):
                            self.towers[target_tower_index].append(self.selected_disk)
                            if hasattr(self.selected_disk, 'size'):
                                self.add_step(self.selected_disk.size, target_tower_index)
                        else:
                            # Если нельзя положить диск, вернем его на исходную башню
                            self.towers[int((self.selected_disk.x + 100) / 200)].append(self.selected_disk)

                        self.selected_disk = None
                        self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging and self.selected_disk is not None:
                # Обновляем позицию выбранного диска в соответствии с текущими координатами мыши
                self.selected_disk.x = event.pos[0] - self.offset_x
                self.selected_disk.y = event.pos[1] - self.offset_y

        # Используйте target_tower_index после блока обработки событий
        if target_tower_index is not None:
            print(f"Selected Tower: {target_tower_index}")

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

            if settings_window.is_start_phase:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    settings_window.check_button_click(mouse_pos)
            elif game_window is not None:
                game_window.handle_events(event)

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
