"""registration page"""
from time import time
import pickle
import pygame

pygame.display.init()
window_size = pygame.display.get_desktop_sizes()[0]
screen = pygame.display.set_mode(window_size)
width = window_size[0]
height = window_size[1]

LOGGING = True
NEWPLAYER = True
NAMEID = ""
FONTPATH = "font/BACKTO1982.TTF"
pygame.font.init()
font = pygame.font.Font(FONTPATH, width // 30)
big_font = pygame.font.Font(FONTPATH, 80)
name_surface = big_font.render(f"{NAMEID}", True, (0,0,0))
name_rect = name_surface.get_rect(midtop=(width / 2, height / 2))
text_surface = font.render("Press RETURN to continue", True, (0,0,0))
text_rect = text_surface.get_rect(midtop = (width/2, 50))
cursor_surface = font.render("-", True, (50,50,50))
cursor_rect = cursor_surface.get_rect(topleft=(name_rect.topright))
cursor_time = time()

# Button class
class Button:
    def __init__(self, text, x, y, width, height, font, bg_color, text_color):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color
        self.rect = pygame.Rect(x, y, width, height)
        self.text_surf = font.render(text, True, text_color)

    def draw(self, win):
        pygame.draw.rect(win, self.bg_color, self.rect)
        win.blit(self.text_surf, (self.x + 20, self.y + 10))

    def is_over(self, pos):
        return self.rect.collidepoint(pos)

# Difficulty buttons
button_width = 150
button_height = 50
button_y = height / 2 + 100
font_size = 30
button_font = pygame.font.Font(None, font_size)
easy_button = Button('Easy', width / 4 - button_width / 2, button_y, button_width, button_height, button_font, (0, 255, 0), (255, 255, 255))
medium_button = Button('Medium', width / 2 - button_width / 2, button_y, button_width, button_height, button_font, (255, 255, 0), (0, 0, 0))
hard_button = Button('Hard', 3 * width / 4 - button_width / 2, button_y, button_width, button_height, button_font, (255, 0, 0), (255, 255, 255))

while LOGGING:
    cursor_rect = cursor_surface.get_rect(topleft=(name_rect.topright))
    screen.fill((150,150,150))
    name_surface = font.render(f"{NAMEID}", True, (0,0,0))
    name_rect = name_surface.get_rect(midtop=(width / 2, height / 2))
    screen.blit(name_surface, name_rect)
    easy_button.draw(screen)
    medium_button.draw(screen)
    hard_button.draw(screen)

    if int(((time()))*2.2)%2 == 0 and len(NAMEID) < 20:
        screen.blit(cursor_surface, cursor_rect)
        cursor_time = time()
    if len(NAMEID) == 0:
        NAMEID = "Type your name"
    if NAMEID != "Type your name":
        screen.blit(text_surface, text_rect)

    # Event handling for difficulty buttons
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if easy_button.is_over(mouse_pos):
                selected_difficulty = 'Easy'  # Set difficulty to easy
            elif medium_button.is_over(mouse_pos):
                selected_difficulty = 'Medium'  # Set difficulty to medium
            elif hard_button.is_over(mouse_pos):
                selected_difficulty = 'Hard'  # Set difficulty to hard

            

            if event.type == pygame.QUIT:
                LOGGING = False
            elif event.type == pygame.KEYDOWN:
                if event.type == 256:
                    PLAYING = False
                    LOGGING = False
            elif event.type == 768:
                if (event.unicode.isalpha() or event.unicode.isnumeric()) and len(NAMEID) < 20:
                    if NAMEID == "Type your name":
                        NAMEID = ""
                    NAMEID += event.unicode
            elif event.key == 8:
                if NAMEID != "Type your name":
                    NAMEID = NAMEID[0:len(NAMEID)-1]
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER) and len(NAMEID) > 0 and NAMEID != "Type your name" and selected_difficulty is not None:
                PLAYING = True
                LOGGING = False
    pygame.display.flip()

REGISTERED = False
# Initialize best score
SCORE = 0
try:
    with open("best_score.pickle", "rb") as f:
        scores = pickle.load(f)
except (EOFError, FileNotFoundError):
    scores = {}
    with open("best_score.pickle", "wb") as f:
        pickle.dump(scores, f)

for key, value in scores.items():
    if key == NAMEID:
        NEWPLAYER = False
        BESTSCORE = value
if NEWPLAYER:
    BESTSCORE = 0
    
