import pygame
from config import *
from apple import Apple
from player import create_player1, create_player2
from modes import GameMode, get_mode_settings
from ui import draw_scores, draw_game_over_text

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pythons")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.running = True
        self.game_over = False
        self.state = "title"
        self.menu_options = [
            "Classic 1P", "Classic 2P", "Time Attack 1P", "Time Attack 2P", "Settings"
        ]
        self.selected_option = 0
        self.speed = DEFAULT_SPEED
        self.initial_snake_size = DEFAULT_INITIAL_SNAKE_SIZE
        self.theme = "Dark"
        self.settings_selected = 0
        self.time_attack_minutes = DEFAULT_TIME_ATTACK_MINUTES
        self.time_attack_time_left = 0
        self.time_attack_active = False
        self.mode = GameMode.CLASSIC_2P
        self.player1 = create_player1()
        self.player2 = create_player2()
        self.pythons = [self.player1, self.player2]
        self.apple = Apple()
        self.apple.randomize(self.pythons)
        self.color_swap = False

    def get_colors(self):
        if self.theme == "Dark":
            return {"bg": BLACK, "text": WHITE, "highlight": YELLOW, "title": BLUE}
        else:
            return {"bg": WHITE, "text": BLACK, "highlight": BLUE, "title": YELLOW}

    def reset_game(self, mode):
        settings = get_mode_settings(mode)
        self.mode = mode
        if self.color_swap:
            p1_color, p2_color = YELLOW, BLUE
        else:
            p1_color, p2_color = BLUE, YELLOW
        from python import Python
        self.player1 = Python(5, 5, p1_color, PLAYER_1_KEYS)
        self.player2 = Python(GRID_WIDTH - 6, GRID_HEIGHT - 6, p2_color, PLAYER_2_KEYS) if settings["players"] == 2 else None
        self.pythons = [self.player1] if not self.player2 else [self.player1, self.player2]
        for _ in range(self.initial_snake_size - 1):
            self.player1.grow()
            if self.player2:
                self.player2.grow()
        self.player1.score = 0
        if self.player2:
            self.player2.score = 0
        self.apple = Apple()
        self.apple.randomize(self.pythons)
        self.game_over = False
        if settings["time_attack"]:
            self.time_attack_time_left = self.time_attack_minutes * 60 * 1000
            self.time_attack_active = True
            self.time_attack_start_ticks = pygame.time.get_ticks()
        else:
            self.time_attack_active = False

    def run(self):
        while self.running:
            self.handle_events()
            if self.state == "playing" and not self.game_over:
                self.update()
            self.draw()
            self.clock.tick(FPS * self.speed / DEFAULT_SPEED)
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            if self.state == "title":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        if self.selected_option == 0:
                            self.reset_game(GameMode.CLASSIC_1P)
                            self.state = "playing"
                        elif self.selected_option == 1:
                            self.reset_game(GameMode.CLASSIC_2P)
                            self.state = "playing"
                        elif self.selected_option == 2:
                            self.reset_game(GameMode.TIME_ATTACK_1P)
                            self.state = "playing"
                        elif self.selected_option == 3:
                            self.reset_game(GameMode.TIME_ATTACK_2P)
                            self.state = "playing"
                        elif self.selected_option == 4:
                            self.state = "settings"
            elif self.state == "settings":
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self.state = "title"
                    elif event.key == pygame.K_LEFT:
                        if self.settings_selected == 0:
                            self.initial_snake_size = max(1, self.initial_snake_size - 1)
                        elif self.settings_selected == 1:
                            self.speed = max(1, self.speed - 1)
                        elif self.settings_selected == 2:
                            self.theme = "Light" if self.theme == "Dark" else "Dark"
                        elif self.settings_selected == 3:
                            self.time_attack_minutes = max(1, self.time_attack_minutes - 1)
                        elif self.settings_selected == 4:
                            self.color_swap = not self.color_swap
                    elif event.key == pygame.K_RIGHT:
                        if self.settings_selected == 0:
                            self.initial_snake_size = min(10, self.initial_snake_size + 1)
                        elif self.settings_selected == 1:
                            self.speed = min(5, self.speed + 1)
                        elif self.settings_selected == 2:
                            self.theme = "Light" if self.theme == "Dark" else "Dark"
                        elif self.settings_selected == 3:
                            self.time_attack_minutes = min(10, self.time_attack_minutes + 1)
                        elif self.settings_selected == 4:
                            self.color_swap = not self.color_swap
                    elif event.key == pygame.K_UP:
                        self.settings_selected = (self.settings_selected - 1) % 5
                    elif event.key == pygame.K_DOWN:
                        self.settings_selected = (self.settings_selected + 1) % 5
            elif self.state == "playing":
                for python in self.pythons:
                    python.handle_input(event)
                if self.game_over and event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self.state = "title"
            elif self.state == "game_over":
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self.state = "title"

    def update(self):
        for python in self.pythons:
            python.move()
            python.check_collision()
            if python.alive and python.body[0].colliderect(self.apple.rect):
                python.grow()
                self.apple.randomize(self.pythons)
        if self.time_attack_active:
            elapsed = pygame.time.get_ticks() - self.time_attack_start_ticks
            self.time_attack_time_left = self.time_attack_minutes * 60 * 1000 - elapsed
            if self.time_attack_time_left <= 0:
                self.time_attack_time_left = 0
                self.game_over = True
                self.state = "game_over"
        if not self.player1.alive and (not self.player2 or not self.player2.alive):
            self.game_over = True
            self.state = "game_over"

    def draw(self):
        colors = self.get_colors()
        if self.state == "title":
            self.draw_title_screen()
        elif self.state == "settings":
            self.draw_settings_screen()
        elif self.state == "playing":
            self.screen.fill(colors["bg"])
            for python in self.pythons:
                python.draw(self.screen)
            self.apple.draw(self.screen)
            draw_scores(self.screen, self.font, self.player1, self.player2, colors, self.time_attack_active, self.time_attack_time_left)
            if self.game_over:
                draw_game_over_text(self.screen, self.font, self.player1, self.player2, colors, self.time_attack_active)
            pygame.display.flip()
        elif self.state == "game_over":
            draw_game_over_text(self.screen, self.font, self.player1, self.player2, colors, self.time_attack_active)
            pygame.display.flip()

    def draw_title_screen(self):
        colors = self.get_colors()
        self.screen.fill(colors["bg"])
        title_font = pygame.font.Font(None, TITLE_FONT_SIZE)
        title_text = title_font.render("PYTHONS", True, colors["title"])
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100))
        self.screen.blit(title_text, title_rect)
        menu_font = pygame.font.Font(None, MENU_FONT_SIZE)
        menu_spacing = 38
        for i, option in enumerate(self.menu_options):
            color = colors["highlight"] if i == self.selected_option else colors["text"]
            option_text = menu_font.render(option, True, color)
            option_rect = option_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + i * menu_spacing))
            self.screen.blit(option_text, option_rect)
        instruction_font = pygame.font.Font(None, INSTRUCTION_FONT_SIZE)
        instruction_text = instruction_font.render("Use UP/DOWN to navigate and ENTER/SPACE to select", True, colors["text"])
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 60))
        self.screen.blit(instruction_text, instruction_rect)
        pygame.display.flip()

    def draw_settings_screen(self):
        colors = self.get_colors()
        self.screen.fill(colors["bg"])
        settings_font = pygame.font.Font(None, SETTINGS_FONT_SIZE)
        y = SCREEN_HEIGHT // 2 - 120
        settings_list = [
            ("Initial Snake Size", self.initial_snake_size, 1, MAX_INITIAL_SNAKE_SIZE),
            ("Speed", self.speed, 1, MAX_SPEED),
            ("Theme", self.theme, None, None),
            ("Time Attack Duration", self.time_attack_minutes, 1, MAX_DURATION),
            ("Python Colors", "Yellow/Blue" if self.color_swap else "Blue/Yellow", None, None)
        ]
        for i, (label, value, minval, maxval) in enumerate(settings_list):
            color = colors["highlight"] if self.settings_selected == i else colors["text"]
            text = f"{label}: {value}"
            txt = settings_font.render(text, True, color)
            rect = txt.get_rect(center=(SCREEN_WIDTH // 2, y + i * 70))
            self.screen.blit(txt, rect)
        instruction_font = pygame.font.Font(None, INSTRUCTION_FONT_SIZE)
        instruction_text = instruction_font.render(
            "Use UP/DOWN to select, LEFT/RIGHT to change, ENTER/SPACE to return", True, colors["text"]
        )
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 60))
        self.screen.blit(instruction_text, instruction_rect)
        pygame.display.flip()

