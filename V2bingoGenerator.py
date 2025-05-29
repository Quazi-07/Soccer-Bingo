'''
Project: Soccer Bingo Spinning Wheel (Enhanced Version)
Developed by: Md. Saifur Rahman
Contact: iamsaif07@gmail.com
'''

import pygame
import random
import math

# Initialize pygame and mixer
pygame.init()
pygame.mixer.init()

# Screen settings
screen_info = pygame.display.Info()
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
#screen = pygame.display.set_mode((700, 1000))
pygame.display.set_caption("Soccer Bingo Spinning Wheel")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
COLOR_LIST = [RED, GREEN, BLUE, YELLOW]

# Fonts
font = pygame.font.Font(None, 28)
large_font = pygame.font.Font(None, 48)
title_font = pygame.font.Font(None, 60)
designer_font = pygame.font.Font(None, 30)

# Load sounds
try:
    spin_sound = pygame.mixer.Sound("spin_loop.mp3")
    select_sound = pygame.mixer.Sound("select.mp3")
except Exception as e:
    print(f"Sound loading failed: {e}")
    spin_sound = None
    select_sound = None

spin_channel = None

# Soccer bingo words
soccer_bingo_words = [
    "Goal", "Offside", "Corner Kick", "Free Kick", "Penalty Kick",
    "Yellow Card", "Red Card", "Throw-in", "Handball", "Header",
    "Dribble", "Tackle", "Save", "Assist", "Shot on Target",
    "Kickoff", "Half-Time", "Full-Time", "Substitution", "Injury Time",
    "Hat Trick", "Clean Sheet", "Equalizer", "Own Goal", "Referee Whistle"
]
random.shuffle(soccer_bingo_words)

# Wheel settings
wheel_radius = 250
center_x, center_y = WIDTH // 2, HEIGHT // 2
angle = 0
angular_velocity = 0
is_spinning = False
selected_word = None
selected_words = []
clock = pygame.time.Clock()

# Draw spinning wheel
def draw_wheel(angle):
    num_words = len(soccer_bingo_words) + len(selected_words)
    angle_step = 360 / num_words

    for i in range(num_words):
        word = selected_words[i] if i < len(selected_words) else soccer_bingo_words[i - len(selected_words)]
        start_angle = math.radians(i * angle_step + angle)
        end_angle = math.radians((i + 1) * angle_step + angle)

        x1 = center_x + wheel_radius * math.cos(start_angle)
        y1 = center_y + wheel_radius * math.sin(start_angle)
        x2 = center_x + wheel_radius * math.cos(end_angle)
        y2 = center_y + wheel_radius * math.sin(end_angle)

        color = COLOR_LIST[i % len(COLOR_LIST)]
        pygame.draw.polygon(screen, color, [(center_x, center_y), (x1, y1), (x2, y2)])
        pygame.draw.polygon(screen, BLACK, [(center_x, center_y), (x1, y1), (x2, y2)], 2)

        mid_angle = (start_angle + end_angle) / 2
        text_x = center_x + (wheel_radius * 0.7) * math.cos(mid_angle)
        text_y = center_y + (wheel_radius * 0.7) * math.sin(mid_angle)
        text = font.render(word, True, BLACK)
        screen.blit(text, text.get_rect(center=(text_x, text_y)))

# Draw the pointer
    
def draw_pointer():
    pygame.draw.polygon(screen, BLACK, [
        (center_x, center_y - wheel_radius - 5),         # Tip pointing down
        (center_x - 10, center_y - wheel_radius - 30),    # Top-left
        (center_x + 10, center_y - wheel_radius - 30)     # Top-right
    ])



# Display selected word
def display_selected_word():
    if selected_word:
        text = large_font.render(f"Selected Word: {selected_word}", True, RED)
        screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT - 80)))

# Main loop
running = True
while running:
    screen.fill(WHITE)
    title = title_font.render("Pearland Soccer Craze Bingo!", True, BLACK)
    screen.blit(title, title.get_rect(center=(WIDTH // 2, 50)))
    
    instruction = font.render("Press SPACEBAR to Spin the Wheel", True, BLACK)
    screen.blit(instruction, instruction.get_rect(center=(WIDTH // 2, 80)))
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE and len(soccer_bingo_words) > 0:
                if not is_spinning:
                    is_spinning = True
                    angular_velocity = random.uniform(10, 15)
                    if spin_sound:
                        spin_channel = spin_sound.play(-1)

    # Physics-based spin
    if is_spinning:
        angle = (angle + angular_velocity) % 360
        angular_velocity *= 0.98  # Friction

        if angular_velocity < 0.2:
            is_spinning = False
            if spin_channel:
                spin_channel.stop()
            index = int(((-angle % 360) / 360) * (len(soccer_bingo_words) + len(selected_words))) % len(soccer_bingo_words)
            selected_word = soccer_bingo_words.pop(index)
            selected_words.insert(0, selected_word)
            if select_sound:
                select_sound.play()

    draw_wheel(angle)
    draw_pointer()
    display_selected_word()

    # Footer
    footer = designer_font.render("© 2025 Pearland Soccer Craze | Saif", True, GRAY)
    screen.blit(footer, (10, HEIGHT - 30))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
