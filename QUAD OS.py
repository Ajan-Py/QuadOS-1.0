import pygame
import sys
import time

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 120, 215)
FONT = pygame.font.SysFont("Arial", 16)
BIG_FONT = pygame.font.SysFont("Arial", 32)
TITLE_FONT = pygame.font.SysFont("Arial", 48)

# Set up screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("QuadOS 1.0 by AJSoftwares")

# App states
booting = True
signed_in = False
current_app = None
text_content = ""
input_active = False
calc_input = ""
paint_lines = []

# Load icon placeholders
app_icons = {
    "Notepad": pygame.Rect(50, 100, 60, 60),
    "Calculator": pygame.Rect(150, 100, 60, 60),
    "Paint": pygame.Rect(250, 100, 60, 60),
    "Shutdown": pygame.Rect(350, 100, 60, 60)
}

def draw_button(rect, text):
    pygame.draw.rect(screen, GRAY, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)
    label = FONT.render(text, True, BLACK)
    screen.blit(label, (rect.x + (rect.width - label.get_width()) // 2, rect.y + (rect.height - label.get_height()) // 2))

def boot_screen():
    start = time.time()
    while time.time() - start < 7:
        screen.fill(BLACK)
        text = TITLE_FONT.render("QuadOS 1.0", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 80))
        sub = FONT.render("by AJSoftwares", True, WHITE)
        screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 2 - 40))

        # Apple-style loading bar
        bar_width = 300
        bar_height = 10
        elapsed = (time.time() - start) / 7
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - bar_width // 2, HEIGHT // 2 + 20, bar_width, bar_height), 2)
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - bar_width // 2 + 2, HEIGHT // 2 + 22, int((bar_width - 4) * elapsed), bar_height - 4))

        pygame.display.flip()
        pygame.time.delay(50)

def login_screen():
    username_input = ""
    input_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 20, 200, 40)
    sign_in_button = pygame.Rect(WIDTH//2 - 50, HEIGHT//2 + 40, 100, 40)
    global signed_in
    while not signed_in:
        screen.fill(BLACK)
        label = BIG_FONT.render("USER", True, WHITE)
        screen.blit(label, (WIDTH // 2 - label.get_width() // 2, HEIGHT // 2 - 80))
        pygame.draw.rect(screen, WHITE, input_rect, 2)
        user_text = FONT.render(username_input, True, WHITE)
        screen.blit(user_text, (input_rect.x + 5, input_rect.y + 10))
        draw_button(sign_in_button, "Sign In")
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if sign_in_button.collidepoint(event.pos):
                    signed_in = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    username_input = username_input[:-1]
                else:
                    username_input += event.unicode

def desktop():
    global current_app, text_content, calc_input, paint_lines
    clock = pygame.time.Clock()
    drawing = False

    while True:
        screen.fill((0, 128, 128))
        for name, rect in app_icons.items():
            draw_button(rect, name)

        # App windows
        if current_app == "Notepad":
            pygame.draw.rect(screen, WHITE, (100, 200, 600, 300))
            pygame.draw.rect(screen, BLACK, (100, 200, 600, 300), 2)
            close = pygame.Rect(680, 200, 20, 20)
            draw_button(close, "🗙")
            text_surface = FONT.render(text_content, True, BLACK)
            screen.blit(text_surface, (110, 230))
        elif current_app == "Calculator":
            pygame.draw.rect(screen, WHITE, (200, 200, 400, 200))
            pygame.draw.rect(screen, BLACK, (200, 200, 400, 200), 2)
            close = pygame.Rect(580, 200, 20, 20)
            draw_button(close, "🗙")
            result = ""
            try:
                result = str(eval(calc_input))
            except:
                result = "Error"
            calc_surface = FONT.render(calc_input + " = " + result, True, BLACK)
            screen.blit(calc_surface, (210, 230))
        elif current_app == "Paint":
            pygame.draw.rect(screen, WHITE, (100, 200, 600, 300))
            pygame.draw.rect(screen, BLACK, (100, 200, 600, 300), 2)
            close = pygame.Rect(680, 200, 20, 20)
            draw_button(close, "🗙")
            for line in paint_lines:
                pygame.draw.line(screen, BLACK, line[0], line[1], 2)
        elif current_app == "Shutdown":
            screen.fill(BLACK)
            shutting_down = BIG_FONT.render("Shutting Down...", True, WHITE)
            screen.blit(shutting_down, (WIDTH // 2 - shutting_down.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.delay(2000)
            pygame.quit()
            sys.exit()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if current_app == "Notepad":
                    if close.collidepoint(event.pos):
                        current_app = None
                elif current_app == "Calculator":
                    if close.collidepoint(event.pos):
                        current_app = None
                elif current_app == "Paint":
                    if close.collidepoint(event.pos):
                        current_app = None
                    elif pygame.Rect(100, 200, 600, 300).collidepoint(event.pos):
                        drawing = True
                        last_pos = event.pos
                else:
                    for name, rect in app_icons.items():
                        if rect.collidepoint(event.pos):
                            current_app = name
            if event.type == pygame.MOUSEBUTTONUP:
                drawing = False
            if event.type == pygame.MOUSEMOTION and drawing:
                new_pos = event.pos
                paint_lines.append((last_pos, new_pos))
                last_pos = new_pos
            if event.type == pygame.KEYDOWN:
                if current_app == "Notepad":
                    if event.key == pygame.K_BACKSPACE:
                        text_content = text_content[:-1]
                    else:
                        text_content += event.unicode
                elif current_app == "Calculator":
                    if event.key == pygame.K_RETURN:
                        pass
                    elif event.key == pygame.K_BACKSPACE:
                        calc_input = calc_input[:-1]
                    else:
                        calc_input += event.unicode

        clock.tick(30)

# Run OS
boot_screen()
login_screen()
desktop()
