import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Stopwatch Baseball")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (200, 200, 200)

# Fonts
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Load images for different base-running scenarios
base_images = {
    'empty': pygame.image.load('C:\\Users\\alexj\\Desktop\\  \\BISMO SPORTS\\STOPWATCH BASEBALL\\IMAGES\\base_0_0_0.png'),
    '1': pygame.image.load('C:\\Users\\alexj\\Desktop\\  \\BISMO SPORTS\\STOPWATCH BASEBALL\\IMAGES\\base_1_0_0.png'),
    '2': pygame.image.load('C:\\Users\\alexj\\Desktop\\  \\BISMO SPORTS\\STOPWATCH BASEBALL\\IMAGES\\base_0_1_0.png'),
    '3': pygame.image.load('C:\\Users\\alexj\\Desktop\\  \\BISMO SPORTS\\STOPWATCH BASEBALL\\IMAGES\\base_0_0_1.png'),
    '12': pygame.image.load('C:\\Users\\alexj\\Desktop\\  \\BISMO SPORTS\\STOPWATCH BASEBALL\\IMAGES\\base_1_1_0.png'),
    '13': pygame.image.load('C:\\Users\\alexj\\Desktop\\  \\BISMO SPORTS\\STOPWATCH BASEBALL\\IMAGES\\base_1_0_1.png'),
    '23': pygame.image.load('C:\\Users\\alexj\\Desktop\\  \\BISMO SPORTS\\STOPWATCH BASEBALL\\IMAGES\\base_0_1_1.png'),
    '123': pygame.image.load('C:\\Users\\alexj\\Desktop\\  \\BISMO SPORTS\\STOPWATCH BASEBALL\\IMAGES\\base_1_1_1.png')
}

# Scale images to appropriate size
for key in base_images:
    base_images[key] = pygame.transform.scale(base_images[key], (600, 400))

# Game variables
clock = pygame.time.Clock()
running = True
paused = False
start_time = None
stop_time = None
message = ""
home_score = [0] * 9
away_score = [0] * 9
current_inning = 1
half_inning = 'top'
outs = 0
batter_on_base = [False, False, False, False]  # 1B, 2B, 3B, Home
game_over = False

# Buttons
start_button = pygame.Rect(290, 220, 100, 50)
stop_button = pygame.Rect(410, 220, 100, 50)

# Game functions
def display_message(text, color, size, y_offset=0):
    font = pygame.font.Font(None, size)
    message = font.render(text, True, color)
    message_rect = message.get_rect(center=(400, 300 + y_offset))
    screen.blit(message, message_rect)

def display_outcome():
    if game_over:
        display_message(message, RED if "wins" in message else GREEN, 74, 100)
    else:
        display_message(message, RED if "OUT" in message else GREEN, 74, 100)

    display_message("Press P to pause, R to reset", BLACK, 36, 0)

def reset_game():
    global start_time, stop_time, message, home_score, away_score, current_inning, half_inning, outs, batter_on_base, game_over
    start_time = None
    stop_time = None
    message = ""
    home_score = [0] * 9
    away_score = [0] * 9
    current_inning = 1
    half_inning = 'top'
    outs = 0
    batter_on_base = [False, False, False, False]
    game_over = False

def draw_runners():
    base_state = ''.join([str(i + 1) for i, on_base in enumerate(batter_on_base[:3]) if on_base])
    base_state = base_state if base_state else 'empty'
    screen.blit(base_images[base_state], (100, 300))

def draw_scoreboard():
    scoreboard_x = 0
    scoreboard_y = 0
    scoreboard_width = SCREEN_WIDTH
    scoreboard_height = 150
    padding = 24
    column_width = (scoreboard_width - 2 * padding) // 11  # 9 innings + 2 for total columns

    # Draw scoreboard box
    pygame.draw.rect(screen, GREY, (scoreboard_x, scoreboard_y, scoreboard_width, scoreboard_height))
    pygame.draw.rect(screen, BLACK, (scoreboard_x, scoreboard_y, scoreboard_width, scoreboard_height), 2)

    # Display innings
    screen.blit(small_font.render("INN", True, BLACK), (scoreboard_x + padding, scoreboard_y + 20))
    for i in range(9):
        screen.blit(small_font.render(str(i + 1), True, BLACK), (scoreboard_x + padding + column_width * (i + 1), scoreboard_y + 20))
    screen.blit(small_font.render("R", True, BLACK), (scoreboard_x + padding + column_width * 10, scoreboard_y + 20))

    # Display away scores
    screen.blit(small_font.render("A", True, BLACK), (scoreboard_x + padding, scoreboard_y + 50))
    for i in range(9):
        screen.blit(small_font.render(str(away_score[i]), True, BLACK), (scoreboard_x + padding + column_width * (i + 1), scoreboard_y + 50))
    screen.blit(small_font.render(str(sum(away_score)), True, BLACK), (scoreboard_x + padding + column_width * 10, scoreboard_y + 50))

    # Display home scores
    screen.blit(small_font.render("H", True, BLACK), (scoreboard_x + padding, scoreboard_y + 80))
    for i in range(9):
        screen.blit(small_font.render(str(home_score[i]), True, BLACK), (scoreboard_x + padding + column_width * (i + 1), scoreboard_y + 80))
    screen.blit(small_font.render(str(sum(home_score)), True, BLACK), (scoreboard_x + padding + column_width * 10, scoreboard_y + 80))

    # Display current inning and outs
    if not game_over:
        inning_text = f"INN: {'TOP' if half_inning == 'top' else 'BOT'} {current_inning}"
        outs_text = f"OUTS: {outs}"
        inning_surface = small_font.render(inning_text, True, BLACK)
        outs_surface = small_font.render(outs_text, True, RED)
        screen.blit(inning_surface, (scoreboard_x + padding, scoreboard_y + 110))
        screen.blit(outs_surface, (scoreboard_x + padding + 200, scoreboard_y + 110))

def pause_menu():
    screen.fill(WHITE)
    display_message("Paused", BLACK, 74, -100)
    display_message("Press R to Restart or P to Resume", BLACK, 36, 100)
    pygame.display.flip()

def draw_buttons():
    pygame.draw.rect(screen, GREY, start_button)
    pygame.draw.rect(screen, GREY, stop_button)
    start_text = small_font.render("START", True, BLACK)
    stop_text = small_font.render("STOP", True, BLACK)
    screen.blit(start_text, (start_button.x + 10, start_button.y + 10))
    screen.blit(stop_text, (stop_button.x + 10, stop_button.y + 10))

def draw_timer_box():
    pygame.draw.rect(screen, BLACK, (300, 150, 200, 60), 3)
    if start_time and not stop_time:
        elapsed_time = time.time() - start_time
        timer_text = f"{elapsed_time:.2f}"
    else:
        timer_text = "0.00" if start_time is None else f"{stop_time - start_time:.2f}"
    timer_display = font.render(timer_text, True, BLACK)
    screen.blit(timer_display, (350, 160))

def move_runners(hit_type):
    global batter_on_base
    new_bases = [False, False, False, False]
    runs_scored = 0
    
    if hit_type == "SINGLE":
        for i in reversed(range(3)):
            if batter_on_base[i]:
                if i == 2:
                    runs_scored += 1  # Runner on 3rd scores
                else:
                    new_bases[i + 1] = True  # Move runners up one base
        new_bases[0] = True  # Batter goes to 1st
    elif hit_type == "DOUBLE":
        for i in reversed(range(3)):
            if batter_on_base[i]:
                if i >= 1:
                    runs_scored += 1  # Runners on 2nd and 3rd score
                else:
                    new_bases[i + 2] = True  # Move runners up two bases
        new_bases[1] = True  # Batter goes to 2nd
    elif hit_type == "TRIPLE":
        for i in reversed(range(3)):
            if batter_on_base[i]:
                runs_scored += 1  # All runners score
        new_bases[2] = True  # Batter goes to 3rd
    elif hit_type == "HOME RUN":
        runs_scored += 1  # Batter scores
        for i in range(3):
            if batter_on_base[i]:
                runs_scored += 1  # All runners score
    
    batter_on_base = new_bases
    return runs_scored

def handle_batting(elapsed_time):
    global outs, half_inning, current_inning, batter_on_base, game_over, message
    hit_type = None
    runs_scored = 0

    if elapsed_time == 0.97:
        hit_type = "SINGLE"
    elif elapsed_time == 0.98:
        hit_type = "DOUBLE"
    elif elapsed_time == 0.99:
        hit_type = "TRIPLE"
    elif elapsed_time == 1.00:
        hit_type = "HOME RUN"
    else:
        hit_type = "OUT"
        outs += 1

    if hit_type == "OUT":
        if outs >= 3:
            outs = 0
            batter_on_base = [False, False, False, False]  # Clear the bases
            if half_inning == 'top':
                half_inning = 'bottom'
            else:
                half_inning = 'top'
                current_inning += 1
                if current_inning > 9:
                    game_over = True
                    if sum(home_score) > sum(away_score):
                        message = "Home team wins!"
                    elif sum(away_score) > sum(home_score):
                        message = "Away team wins!"
                    else:
                        message = "It's a tie!"
                elif current_inning == 9 and half_inning == 'bottom' and sum(home_score) > sum(away_score):
                    game_over = True
                    message = "Home team wins!"
    else:
        runs_scored = move_runners(hit_type)
        if half_inning == 'top':
            away_score[current_inning - 1] += runs_scored
        else:
            home_score[current_inning - 1] += runs_scored

    message = f"{hit_type}!"

    return hit_type

# Game loop
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos) and not game_over:
                if not start_time:
                    start_time = time.time()
                elif stop_time:
                    start_time = time.time()
                    stop_time = None
            elif stop_button.collidepoint(event.pos) and not game_over:
                if start_time and not stop_time:
                    stop_time = time.time()
                    elapsed_time = round(stop_time - start_time, 2)
                    handle_batting(elapsed_time)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()
            elif event.key == pygame.K_p:
                paused = not paused
                if not paused:
                    start_time = None
                    stop_time = None

    if paused:
        pause_menu()
        continue

    draw_scoreboard()
    draw_runners()
    draw_buttons()
    draw_timer_box()

    display_outcome()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()