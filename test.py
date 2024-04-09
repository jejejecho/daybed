import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 500
GREY = (192, 192, 192)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
LIGHT_GREEN = (0, 255, 0)
RED = (255, 0, 0)
FONT_SIZE = 40
FPS = 60
WORD_DURATION = 30

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Typing Game")
clock = pygame.time.Clock()

font = pygame.font.Font(None, FONT_SIZE)

COMMON_WORDS = ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'I', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me', 'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know', 'take', 'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other', 'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also', 'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way', 'even', 'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most', 'us']

def get_random_word():
    return random.choice(COMMON_WORDS)

def draw_text(surface, text, color, font, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

def start_screen():
    start_text = font.render("Press Enter to Start", True, BLACK)
    start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    screen.fill(GREY)
    screen.blit(start_text, start_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

def main():
    start_screen()

    start_time = pygame.time.get_ticks()
    word_count = 0
    total_word_count = 0
    correct_chars_count = 0
    total_chars_count = 0
    incorrect_words_count = 0
    timer_started = False
    game_started = True
    current_word = get_random_word()
    typed_word = ''

    restart_button = pygame.Rect(WIDTH - 140, 20, 120, 40)

    running = True
    while running:
        screen.fill(GREY)

        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN:
                    if timer_started:
                        if typed_word == current_word:
                            word_count += 1
                            total_word_count += 1
                            correct_chars_count += len(current_word)
                            total_chars_count += len(current_word)
                            current_word = get_random_word()
                        else:
                            total_chars_count += len(typed_word)
                            total_word_count += 1
                            incorrect_words_count += 1
                    else:
                        timer_started = True
                    typed_word = ''
                elif event.key == pygame.K_BACKSPACE:
                    typed_word = typed_word[:-1]
                    if typed_word and typed_word != current_word[:len(typed_word)]:
                        incorrect_words_count += 1
                elif event.key != pygame.K_CAPSLOCK:
                    typed_word += event.unicode
                    if event.key != pygame.K_RETURN:
                        total_chars_count += 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    start_time = pygame.time.get_ticks()
                    word_count = 0
                    total_word_count = 0
                    correct_chars_count = 0
                    total_chars_count = 0
                    incorrect_words_count = 0
                    timer_started = False
                    current_word = get_random_word()
                    typed_word = ''

        draw_text(screen, f"Time Left: {max(0, WORD_DURATION - elapsed_time)} seconds", BLACK, font, WIDTH // 2, HEIGHT // 5)
        correct_color = GREEN if typed_word == current_word[:len(typed_word)] else RED
        draw_text(screen, f"{current_word}", correct_color, font, WIDTH // 2, HEIGHT // 2 - 2 * FONT_SIZE)
        draw_text(screen, f"{typed_word}", BLACK, font, WIDTH // 2, HEIGHT // 2)
        draw_text(screen, f"Words Typed: {word_count}", BLACK, font, WIDTH // 2, 3 * HEIGHT // 4)

        if len(typed_word) > 0:
            accuracy = max(((word_count - incorrect_words_count) / max(1, total_word_count)) * 100, 0)
            accuracy = round(accuracy, 2)
            draw_text(screen, f"Accuracy: {accuracy}%", BLACK, font, WIDTH // 2, HEIGHT // 2 + 2 * FONT_SIZE)

        if elapsed_time >= WORD_DURATION:
            wpm = round((word_count / WORD_DURATION) * 60, 2)
            pygame.draw.rect(screen, LIGHT_GREEN, restart_button)
            draw_text(screen, "Restart", BLACK, font, restart_button.centerx, restart_button.centery)
            draw_text(screen, f"WPM: {wpm}", BLACK, font, WIDTH // 2, HEIGHT // 2 + 4 * FONT_SIZE)

            if restart_button.collidepoint(pygame.mouse.get_pos()):
                start_time = pygame.time.get_ticks()
                word_count = 0
                total_word_count = 0
                correct_chars_count = 0
                total_chars_count = 0
                incorrect_words_count = 0
                timer_started = False
                current_word = get_random_word()
                typed_word = ''

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
