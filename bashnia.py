import pygame
import sys

class Disk:
    def __init__(self, size, color):
        self.size = size
        self.color = color
        self.rect = None
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0
        self.original_tower = None
        self.original_position = None
        self.original_tower_index = None

class SettingsWindow:
    def __init__(self):
        self.num_disks = 5
        self.is_start_phase = True
        self.button_rect = pygame.Rect(50, 50, 300, 50)
        self.start_button_rect = pygame.Rect(50, 120, 250, 50)
        self.right_animation_counter = 0
        self.restart_question_shown = False
        
    
    def draw_restart_question(self, screen):
        if self.restart_question_shown:
            font = pygame.font.Font(None, 36)
            text = font.render("Хотите начать заново?", True, (0, 0, 0))
            yes_text = font.render("Да", True, (0, 255, 0))
            no_text = font.render("Нет", True, (255, 0, 0))

            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
            screen.blit(text, text_rect)

            yes_rect = yes_text.get_rect(center=(WIDTH // 2 - 50, HEIGHT // 2 + 20))
            screen.blit(yes_text, yes_rect)

            no_rect = no_text.get_rect(center=(WIDTH // 2 + 50, HEIGHT // 2 + 20))
            screen.blit(no_text, no_rect)

            self.restart_yes_rect = pygame.Rect(yes_rect.x - 10, yes_rect.y - 10, yes_rect.width + 20, yes_rect.height + 20)
            self.restart_no_rect = pygame.Rect(no_rect.x - 10, no_rect.y - 10, no_rect.width + 20, no_rect.height + 20)

    def handle_restart_question(self, event):
        if self.restart_question_shown:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.restart_yes_rect.collidepoint(event.pos):
                    self.is_start_phase = True
                    self.restart_question_shown = False
                    self.num_disks = 5
                    self.show_icon = False
                    self.restart_question_counter -= 1
                elif self.restart_no_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                    
    
    def draw_right_animation(self, screen):
        if self.right_animation_counter > 0:
            font = pygame.font.Font(None, 36)
            text = font.render("Правильно!", True, (0, 255, 0))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)
            self.right_animation_counter -= 1
            if self.right_animation_counter == 0:
                self.restart_question_shown = True
                self.restart_question_counter += 1
    
    def check_restart_button_click(self, pos):
        if not self.is_start_phase and self.restart_button_rect.collidepoint(pos):
            return True
        return False

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
        self.steps = []
        self.dragging = False
        self.selected_disk = None
        self.offset_x = 0
        self.offset_y = 0
        self.restart_game = False
        self.win_animation_counter = 0

    def draw_selected_disk(self, screen, mouse_pos):
        if self.selected_disk is not None:
            disk_width = self.selected_disk.size * 30
            disk_height = 20
            x = mouse_pos[0] - self.offset_x
            y = mouse_pos[1] - self.offset_y
            pygame.draw.rect(
                screen,
                self.selected_disk.color,
                (x - disk_width // 2 + 10 // 2, y, disk_width, disk_height),
            )

    def draw_win_animation(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (0, 0, WIDTH, HEIGHT), 10)
        font = pygame.font.Font(None, 36)
        text = font.render("Победа! Нажмите 'Заново'", True, (0, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

    def draw(self, screen, settings_window):
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

        if self.check_win(settings_window):
            self.draw_win_animation(screen)
        else:
            self.draw_selected_disk(screen, pygame.mouse.get_pos())

    def add_step(self, move_from, move_to):
        self.steps.append((move_from, move_to))

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for tower_index, tower in enumerate(self.towers):
                    top_disk = self.get_top_disk(tower_index)
                    if top_disk is not None:  # Проверяем, что башня не пуста
                        x = tower_index * 200 + (800 - 3 * 200) // 2
                        disk_rect = pygame.Rect(
                            x - top_disk.size * 15 + 10 // 2,
                            400 - len(tower) * 20,
                            top_disk.size * 30,
                            20,
                        )
                        if disk_rect.collidepoint(event.pos):
                            self.selected_disk = self.towers[tower_index].pop()
                            self.selected_disk.original_tower = tower_index
                            self.selected_disk.original_position = len(self.towers[self.selected_disk.original_tower])
                            self.dragging = True
                            self.offset_x = event.pos[0] - disk_rect.x
                            self.offset_y = event.pos[1] - disk_rect.y

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.dragging:
                target_tower_index = int((event.pos[0] - 50) / 200)

                if 0 <= target_tower_index < len(self.towers):
                    target_tower = self.towers[target_tower_index]
                    original_tower_index = self.selected_disk.original_tower
                    if not target_tower or (self.get_top_disk(target_tower_index) is not None and self.selected_disk.size < self.get_top_disk(target_tower_index).size):
                        self.towers[target_tower_index].append(self.selected_disk)
                        if hasattr(self.selected_disk, 'size'):
                            self.add_step(self.selected_disk.size, target_tower_index)
                            original_tower_index = None
                    else:
                        # Если диск размером больше пытаются поставить на диск размером меньше,
                        # вернем его на исходную башню и позицию
                        self.towers[original_tower_index].insert(self.selected_disk.original_position, self.selected_disk)

                    self.selected_disk = None
                    self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging and self.selected_disk is not None and self.selected_disk.rect is not None:
                self.selected_disk.rect.x = event.pos[0] - self.offset_x
                self.selected_disk.rect.y = event.pos[1] - self.offset_y

        if not self.dragging:
            self.update()

    def get_top_disk(self, tower_index):
        tower = self.towers[tower_index]
        return tower[-1] if tower else None

    def check_win(self, settings_window):
        if len(self.towers[2]) == settings_window.num_disks:
            settings_window.restart_question_counter = 100
            return True
        return False

    def update(self):
        if self.selected_disk is not None:
            original_tower_index = self.selected_disk.original_tower
            if original_tower_index is not None:
                self.towers[original_tower_index].insert(self.selected_disk.original_position, self.selected_disk)
                self.selected_disk = None

def create_towers(num_disks):
    return [
        [Disk(num_disks - i, (255, 255 - (25 * i), 20 * i)) for i in range(num_disks)],
        [],
        []
    ]

def main():
    pygame.init()
    global WIDTH, HEIGHT
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
                if game_window.check_win(settings_window):
                    settings_window.right_animation_counter = 100
                    settings_window.restart_question_shown = True
                    game_window = None

            settings_window.handle_restart_question(event)

        screen.fill((255, 255, 255))

        if settings_window.is_start_phase:
            settings_window.draw(screen)
        else:
            if game_window is None:
                game_window = GameWindow(settings_window.num_disks)
            game_window.draw(screen, settings_window)

        settings_window.draw_right_animation(screen)
        settings_window.draw_restart_question(screen)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

if __name__ == "__main__":
    main()
