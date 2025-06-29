import pygame
from config import *
from python import Python
from apple import Apple

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
        self.menu_options = ["Classic", "Time Attack", "Settings"]
        self.selected_option = 0

        self.speed = DEFAULT_SPEED
        self.initial_snake_size = DEFAULT_INITIAL_SNAKE_SIZE
        self.theme = "Dark"
        self.settings_selected = 0

        self.time_attack_minutes = DEFAULT_TIME_ATTACK_MINUTES
        self.time_attack_time_left = 0
        self.time_attack_active = False

        self.player1 = Python(5, 5, BLUE, PLAYER_1_KEYS)
        self.player2 = Python(GRID_WIDTH - 6, GRID_HEIGHT - 6, YELLOW, PLAYER_2_KEYS)
        self.pythons = [self.player1, self.player2]
        self.apple = Apple()
        self.apple.randomize(self.pythons)

    def get_colors(self):
        if self.theme == "Dark":
            return {
                "bg": BLACK,
                "text": WHITE,
                "highlight": YELLOW,
                "title": BLUE
            }
        else:
            return {
                "bg": WHITE,
                "text": BLACK,
                "highlight": BLUE,
                "title": YELLOW,
            }

    def reset_game(self, mode="Classic"):
        self.player1 = Python(5, 5, BLUE, PLAYER_1_KEYS)
        self.player2 = Python(GRID_WIDTH - 6, GRID_HEIGHT - 6, YELLOW, PLAYER_2_KEYS)
        self.pythons = [self.player1, self.player2]
        for _ in range(self.initial_snake_size - 1):
            self.player1.grow()
            self.player2.grow()
        self.player1.score = 0
        self.player2.score = 0
        self.apple = Apple()
        self.apple.randomize(self.pythons)
        self.game_over = False
        if mode == "Time Attack":
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

            if self.state == "title":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        if self.selected_option == 0:
                            self.reset_game("Classic")
                            self.state = "playing"
                        elif self.selected_option == 1:
                            self.reset_game("Time Attack")
                            self.state = "playing"
                        elif self.selected_option == 2:
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
                    elif event.key == pygame.K_RIGHT:
                        if self.settings_selected == 0:
                            self.initial_snake_size = min(10, self.initial_snake_size + 1)
                        elif self.settings_selected == 1:
                            self.speed = min(5, self.speed + 1)
                        elif self.settings_selected == 2:
                            self.theme = "Light" if self.theme == "Dark" else "Dark"
                        elif self.settings_selected == 3:
                            self.time_attack_minutes = min(10, self.time_attack_minutes + 1)
                    elif event.key == pygame.K_UP:
                        self.settings_selected = (self.settings_selected - 1) % 4
                    elif event.key == pygame.K_DOWN:
                        self.settings_selected = (self.settings_selected + 1) % 4
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

        if not self.player1.alive and not self.player2.alive:
            self.game_over = True
            self.state = "game_over"

    def draw_scores(self):
        colors = self.get_colors()
        p1_score_text = self.font.render(f"Blue: {self.player1.score}", True, colors["text"])
        p2_score_text = self.font.render(f"Yellow: {self.player2.score}", True, colors["text"])
        self.screen.blit(p1_score_text, (10, 10))
        self.screen.blit(p2_score_text, (SCREEN_WIDTH - p2_score_text.get_width() - 10, 10))
        if self.time_attack_active:
            mins = self.time_attack_time_left // 60000
            secs = (self.time_attack_time_left // 1000) % 60
            timer_text = self.font.render(f"Time: {mins}:{secs:02d}", True, colors["text"])
            self.screen.blit(timer_text, (SCREEN_WIDTH // 2 - timer_text.get_width() // 2, 10))

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
            self.draw_scores()
            if self.game_over:
                self.draw_game_over_text()
            pygame.display.flip()
        elif self.state == "game_over":
            self.draw_game_over_text()
            pygame.display.flip()

    def draw_title_screen(self):
        colors = self.get_colors()
        self.screen.fill(colors["bg"])
        title_font = pygame.font.Font(None, TITLE_FONT_SIZE)
        title_text = title_font.render("PYTHONS", True, colors["title"])
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100))
        self.screen.blit(title_text, title_rect)

        menu_font = pygame.font.Font(None, MENU_FONT_SIZE)
        for i, option in enumerate(self.menu_options):
            color = colors["highlight"] if i == self.selected_option else colors["text"]
            option_text = menu_font.render(option, True, color)
            option_rect = option_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + i * 60))
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
            ("Time Attack Duration", self.time_attack_minutes, 1, MAX_DURATION)
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

    def draw_game_over_text(self):
        colors = self.get_colors()
        self.screen.fill(colors["bg"])
        large_font = pygame.font.Font(None, GAME_OVER_FONT_SIZE)
        if self.time_attack_active:
            if self.player1.score > self.player2.score:
                text = large_font.render("Blue Wins!", True, BLUE)
            elif self.player2.score > self.player1.score:
                text = large_font.render("Yellow Wins!", True, YELLOW)
            else:
                text = large_font.render("It's a Tie!", True, colors["text"])
        else:
            if self.player1.score > self.player2.score:
                text = large_font.render("Blue Wins!", True, BLUE)
            elif self.player2.score > self.player1.score:
                text = large_font.render("Yellow Wins!", True, YELLOW)
            else:
                text = large_font.render("It's a Tie!", True, colors["text"])
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 60))
        self.screen.blit(text, text_rect)

        score_font = pygame.font.Font(None, FONT_SIZE)
        score_text = score_font.render(
            f"Final Score - Blue: {self.player1.score}  Yellow: {self.player2.score}",
            True, colors["text"]
        )
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.screen.blit(score_text, score_rect)

        small_font = pygame.font.Font(None, GAME_OVER_SMALL_FONT_SIZE)
        instruction_text = small_font.render("Press ENTER/SPACE to return to title", True, colors["text"])
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 40))
        self.screen.blit(instruction_text, instruction_rect)

    settings_selected = 0

