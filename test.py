import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (255, 255, 255)
TEXT_COLOR = (0, 0, 0)
CORRECT_COLOR = (0, 128, 0)
INCORRECT_COLOR = (255, 0, 0)
FONT_SIZE = 30
FPS = 60
WORD_DURATION = 30
PARAGRAPH_LENGTH = 5

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Typing Game")
clock = pygame.time.Clock()

font = pygame.font.Font(None, FONT_SIZE)
input_font = pygame.font.Font(None, FONT_SIZE + 5)

COMMON_WORDS = ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'I', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me', 'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know', 'take', 'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other', 'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also', 'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way', 'even', 'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most', 'us']

def generate_paragraph():
    return ' '.join(random.choices(COMMON_WORDS, k=PARAGRAPH_LENGTH))

def draw_text(surface, text, color, font, x, y, centered=False):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if centered:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

def start_screen():
    screen.fill(BACKGROUND_COLOR)
    title_font = pygame.font.Font(None, 50)
    draw_text(screen, "Typing Game", TEXT_COLOR, title_font, WIDTH // 2, HEIGHT // 4, centered=True)
    instructions_font = pygame.font.Font(None, 30)
    draw_text(screen, "Type as many words as you can in 30 seconds!", TEXT_COLOR, instructions_font, WIDTH // 2, HEIGHT // 2 - 30, centered=True)
    draw_text(screen, "Press Enter to Start", TEXT_COLOR, instructions_font, WIDTH // 2, HEIGHT // 2 + 30, centered=True)

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

def restart_prompt():
    screen.fill(BACKGROUND_COLOR)
    restart_font = pygame.font.Font(None, 40)
    draw_text(screen, "Do you want to restart? (y/n)", TEXT_COLOR, restart_font, WIDTH // 2, HEIGHT // 2, centered=True)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True
                elif event.key == pygame.K_n:
                    return False

def main():
    start_screen()

    while True:
        word_count = 0
        correct_chars_count = 0
        total_chars_count = 0
        start_time = pygame.time.get_ticks()
        current_paragraph = generate_paragraph()
        words_typed = ''
        current_word_index = 0

        running = True
        while running:
            screen.fill(BACKGROUND_COLOR)

            elapsed_time = (pygame.time.get_ticks() - start_time) / 1000

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
                    elif event.key == pygame.K_BACKSPACE:
                        if len(words_typed) > 0:
                            words_typed = words_typed[:-1]
                    elif event.key == pygame.K_SPACE:
                        if words_typed == current_paragraph.split()[current_word_index]:
                            word_count += 1
                            correct_chars_count += len(words_typed)
                            total_chars_count += len(words_typed)
                            words_typed = ''
                            current_word_index += 1
                            if current_word_index >= PARAGRAPH_LENGTH:
                                current_word_index = 0
                                current_paragraph = generate_paragraph()
                        else:
                            total_chars_count += len(words_typed)
                            words_typed = ''
                    elif event.key != pygame.K_CAPSLOCK:
                        words_typed += event.unicode

            draw_text(screen, f"Time Left: {max(0, WORD_DURATION - elapsed_time):.2f} seconds", TEXT_COLOR, font, 100, 50)
            words = current_paragraph.split()
            for i, word in enumerate(words):
                if i == current_word_index:
                    correct_part = word[:len(words_typed)]
                    incorrect_part = word[len(words_typed):]
                    correct_width = font.size(correct_part)[0]
                    incorrect_width = font.size(incorrect_part)[0]
                    draw_text(screen, correct_part, CORRECT_COLOR, font, WIDTH // 2 - incorrect_width // 2 - correct_width // 2, HEIGHT // 2 + i * 30, centered=False)
                    draw_text(screen, incorrect_part, INCORRECT_COLOR, font, WIDTH // 2 - incorrect_width // 2 + correct_width // 2, HEIGHT // 2 + i * 30, centered=False)
                else:
                    draw_text(screen, word, TEXT_COLOR, font, WIDTH // 2, HEIGHT // 2 + i * 30, centered=True)

            draw_text(screen, words_typed, CORRECT_COLOR, input_font, WIDTH // 2, HEIGHT // 2 + 30 * PARAGRAPH_LENGTH, centered=True)

            if elapsed_time >= WORD_DURATION:
                restart = restart_prompt()
                if not restart:
                    running = False
                break

            wpm = round(word_count / (elapsed_time / 60), 2) if elapsed_time > 0 else 0
            accuracy = round((correct_chars_count / total_chars_count) * 100, 2) if total_chars_count > 0 else 0

            draw_text(screen, f"WPM: {wpm}", TEXT_COLOR, font, WIDTH // 2, HEIGHT - 100, centered=True)
            draw_text(screen, f"Accuracy: {accuracy}%", TEXT_COLOR, font, WIDTH // 2, HEIGHT - 50, centered=True)

            pygame.display.flip()
            clock.tick(FPS)

if __name__ == '__main__':
    main()
