import pygame
from config import *

def draw_scores(screen, font, player1, player2, colors, time_attack_active, time_attack_time_left):
    p1_score_text = font.render(f"Score: {player1.score}", True, player1.color)
    screen.blit(p1_score_text, (10, 10))
    if player2:
        p2_score_text = font.render(f"Score: {player2.score}", True, player2.color)
        screen.blit(p2_score_text, (SCREEN_WIDTH - p2_score_text.get_width() - 10, 10))
    if time_attack_active:
        mins = time_attack_time_left // 60000
        secs = (time_attack_time_left // 1000) % 60
        timer_text = font.render(f"Time: {mins}:{secs:02d}", True, colors["text"])
        screen.blit(timer_text, (SCREEN_WIDTH // 2 - timer_text.get_width() // 2, 10))

def draw_game_over_text(screen, font, player1, player2, colors, time_attack_active):
    screen.fill(colors["bg"])
    large_font = pygame.font.Font(None, GAME_OVER_FONT_SIZE)
    if not player2:
        score_text = large_font.render(f" Final Score: {player1.score}", True, player1.color)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(score_text, score_rect)
        small_font = pygame.font.Font(None, GAME_OVER_SMALL_FONT_SIZE)
        instruction_text = small_font.render("Press ENTER/SPACE to return to title", True, colors["text"])
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 40))
        screen.blit(instruction_text, instruction_rect)
        return
    winner_color = colors["text"]
    if time_attack_active:
        if player1.score > player2.score:
            winner_color = player1.color
            text = large_font.render("Blue Wins!" if player1.color == BLUE else "Yellow Wins!", True, winner_color)
        elif player2.score > player1.score:
            winner_color = player2.color
            text = large_font.render("Yellow Wins!" if player2.color == YELLOW else "Blue Wins!", True, winner_color)
        else:
            text = large_font.render("It's a Tie!", True, colors["text"])
    else:
        if player1.score > player2.score:
            winner_color = player1.color
            text = large_font.render("Blue Wins!" if player1.color == BLUE else "Yellow Wins!", True, winner_color)
        elif player2.score > player1.score:
            winner_color = player2.color
            text = large_font.render("Yellow Wins!" if player2.color == YELLOW else "Blue Wins!", True, winner_color)
        else:
            text = large_font.render("It's a Tie!", True, colors["text"])
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 60))
    screen.blit(text, text_rect)
    score_font = pygame.font.Font(None, FONT_SIZE)
    score_text = score_font.render(f"Final Score - Blue: {player1.score}  Yellow: {player2.score}", True, colors["text"])
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(score_text, score_rect)
    small_font = pygame.font.Font(None, GAME_OVER_SMALL_FONT_SIZE)
    instruction_text = small_font.render("Press ENTER/SPACE to return to title", True, colors["text"])
    instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 40))
    screen.blit(instruction_text, instruction_rect)
