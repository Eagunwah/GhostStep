import pygame
import sys

pygame.init()

# --- SCREEN SETUP ---
WIDTH, HEIGHT = 1087, 625
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GhostStep")

# --- LOAD IMAGES --- 
background_img = pygame.image.load("UI/background.png").convert_alpha()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# second background for settings/level select screens
background2_img = pygame.image.load("UI/background2.png").convert_alpha()
background2_img = pygame.transform.scale(background2_img, (WIDTH, HEIGHT))

# normal button images
play_button_img = pygame.image.load("UI/play_button.png").convert_alpha()
level_button_img = pygame.image.load("UI/level_select_button.png").convert_alpha()
settings_button_img = pygame.image.load("UI/settings_button.png").convert_alpha()
back_button_img = pygame.image.load("UI/back_button.png").convert_alpha()
credit_button_img = pygame.image.load("UI/credit_button.png").convert_alpha()
home_button_img = pygame.image.load("UI/home_button.png").convert_alpha()

# pressed button images
play_button_pressed_img = pygame.image.load("UI/play_button_pressed.png").convert_alpha()
level_button_pressed_img = pygame.image.load("UI/level_select_button_pressed.png").convert_alpha()
settings_button_pressed_img = pygame.image.load("UI/settings_button_pressed.png").convert_alpha()
back_button_pressed_img = pygame.image.load("UI/back_button_pressed.png").convert_alpha()

credit_button_pressed_img = pygame.image.load("UI/credit_button_pressed.png").convert_alpha()
credit_img = pygame.image.load("UI/credit.png").convert_alpha()

home_button_pressed_img = pygame.image.load("UI/home_button_pressed.png").convert_alpha()

# Title images
title_img = pygame.image.load("UI/Title.png").convert_alpha()
settings_text_img = pygame.image.load("UI/settings_text.png").convert_alpha()
level_select_text_img = pygame.image.load("UI/Level_select_text.png").convert_alpha()
congrats_img = pygame.image.load("UI/congrats.png").convert_alpha()


# level images
spike_img = pygame.image.load("sprites/spike.png").convert_alpha()
level2_img = pygame.image.load("levels/level2.png").convert_alpha()
flag_img = pygame.image.load("sprites/flag.png").convert_alpha()

# restart button setup
restart_icon_img = pygame.image.load("UI/restart_icon.png").convert_alpha()
restart_scale = 0.04
restart_icon_img = pygame.transform.rotozoom(restart_icon_img, 0, restart_scale)
restart_icon_rect = restart_icon_img.get_rect(topleft=(5, 5))  
restart_pressed = False

# --- MUSIC SETUP ---
current_music = None
difficulty_level = "full"

game_music = {
    "menu": "music/menu.ogg",
    "level1": "music/Level_1.ogg",
    "level2": "music/Level_2.ogg",
    "level3": "music/Level_3.ogg",
    "full": "music/full_loop.ogg",
}

pygame.mixer.music.set_volume(0.17)

# allow multiple songs to be played based on song name
def play_music(song_name):
    global current_music
    if song_name not in game_music:
        print("No music")
        return
    if current_music == song_name and pygame.mixer.music.get_busy():
        return
    pygame.mixer.music.load(game_music[song_name])
    pygame.mixer.music.play(-1)
    current_music = song_name

def stop_music():
    global current_music
    pygame.mixer.music.stop()
    current_music = None

# --- BUTTON SETUP ---
PLAY_TARGET_WIDTH = WIDTH * 0.23  
play_scale = PLAY_TARGET_WIDTH / play_button_img.get_width()
SIDE_RELATIVE_SCALE = 0.22 / 0.3
side_scale = play_scale * SIDE_RELATIVE_SCALE
HOME_SCALE = play_scale * 0.75

play_button_img = pygame.transform.rotozoom(play_button_img, 0, play_scale)
play_button_pressed_img = pygame.transform.rotozoom(play_button_pressed_img, 0, play_scale)

level_button_img = pygame.transform.rotozoom(level_button_img, 0, side_scale)
level_button_pressed_img = pygame.transform.rotozoom(level_button_pressed_img, 0, side_scale)

settings_button_img = pygame.transform.rotozoom(settings_button_img, 0, side_scale)
settings_button_pressed_img = pygame.transform.rotozoom(settings_button_pressed_img, 0, side_scale)

back_button_img = pygame.transform.scale(back_button_img, (120, 100))
back_button_pressed_img = pygame.transform.scale(back_button_pressed_img, (120, 100))

credit_button_img = pygame.transform.rotozoom(credit_button_img, 0, 0.12)
credit_button_pressed_img = pygame.transform.rotozoom(credit_button_pressed_img, 0, 0.12)

credit_img = pygame.transform.rotozoom(credit_img, 0, 0.6) 
credit_rect = credit_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))

home_button_img = pygame.transform.rotozoom(home_button_img, 0, HOME_SCALE)
home_button_pressed_img = pygame.transform.rotozoom(home_button_pressed_img, 0, HOME_SCALE)


# --- START MENU BUTTON POSITION SETUP ---
button_spacing = -50 
centre_x = WIDTH // 2
centre_y = HEIGHT // 2 + 60

play_button_rect = play_button_img.get_rect(center=(centre_x, centre_y))

level_button_rect = level_button_img.get_rect(
    center=(centre_x - play_button_rect.width - button_spacing, centre_y)
)
settings_button_rect = settings_button_img.get_rect(
    center=(centre_x + play_button_rect.width + button_spacing, centre_y)
)

home_button_rect = home_button_img.get_rect(
    center=(WIDTH // 2, HEIGHT // 2 + 170)
)

credit_button_rect = credit_button_img.get_rect(topleft=(785, 295))

# --- TITLES SETUP ---
title_img = pygame.transform.rotozoom(title_img, 0, 0.6)
title_rect = title_img.get_rect(center=(WIDTH // 2, 130))

settings_text_img = pygame.transform.rotozoom(settings_text_img, 0, 0.23)
settings_text_rect = settings_text_img.get_rect(center=(WIDTH // 2, 85))

level_select_text_img = pygame.transform.rotozoom(level_select_text_img, 0, 0.23)
level_select_text_rect = level_select_text_img.get_rect(center=(WIDTH // 2, 90))

congrats_img = pygame.transform.rotozoom(congrats_img, 0, 0.5)


# --- GAME VARIABLES ---
GROUND_HEIGHT = 80
ground_y = HEIGHT - GROUND_HEIGHT

enemy = pygame.Rect(600, ground_y - 50, 50, 50)
ENEMY_COLLISION_MARGIN = 12
SPIKE_HEIGHT_REDUCTION = 12        
COLLISION_HEIGHT_REDUCTION = 6   
spawn_point = (140, ground_y - 50)
player = pygame.Rect(spawn_point[0], spawn_point[1], 30, 30)
FLAG_SIZE = 50

GROUND_COLOUR = (70, 25, 92)
LEVEL2_PLATFORM_COLOUR = (70, 25, 92)  

WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GAME_BACKGROUND_COLOUR = (38, 11, 58)
GHOST_COLOUR = (200, 200, 255)
GHOST_SOLID_COLOUR = (160, 200, 255)  

# --- BOUNCE PAD INFO ---
BOUNCE_PAD_SIZE = (30, 7)
BOUNCE_MULTIPLIER = 1.5

# --- INSTRUCTION TEXT  ---
INSTRUCTION_TEXT = "WAD or ARROW KEYS to move, R key to restart"
INSTRUCTION_COLOUR = (189, 99, 195)  
INSTRUCTION_FONT = pygame.font.Font(None, 28)  

# --- TEXT SET UP ---
END_TEXT = "Well done, you've completed my game. Press the home button to go back to the start screen."
END_FONT = pygame.font.Font(None, 32)


player_dead = False
show_credit_image = False

# --- LEVELS SET UP  ---
level2_img = pygame.transform.scale(level2_img, (WIDTH, HEIGHT))
flag_img = pygame.transform.scale(flag_img, (FLAG_SIZE, FLAG_SIZE))
flag_rect = pygame.Rect(WIDTH - FLAG_SIZE - 40, ground_y - FLAG_SIZE, FLAG_SIZE, FLAG_SIZE)


# Physics
gravity = 0.6
jump_force = -9
player_velocity_y = 0
enemy_velocity_y = 0
on_ground_player = True
on_ground_enemy = True

# Timing
FPS = 60
clock = pygame.time.Clock()

# --- GHOST SYSTEM (multiple ghosts system) ---
DELAY_SEC = 0.0
FRAMES_DELAY = int(DELAY_SEC * FPS)

recordings_history = []  
ghosts = []              
recording_active = False
current_recording = []

MAX_GHOSTS = 3
current_screen = "start"

# button pressed states
play_pressed = False
level_pressed = False
settings_pressed = False
back_pressed = False  
credit_pressed = False
home_pressed = False

# delayed screen change
screen_change_delay = 0       
pending_screen = None         

# level/game reset
def reset_full_game():
    global current_screen, player, ghosts, recordings_history
    global recording_active, current_recording, on_ground_player
    ghosts.clear()
    recordings_history.clear()
    current_recording.clear()
    recording_active = False
    player.x, player.y = spawn_point
    on_ground_player = True
    restart()

# allow bounce pads for level 4 and level 5
def get_active_bounce_pads():
    if current_screen == "level4":
        return LEVEL4_BOUNCE_PADS
    elif current_screen == "level5":
        return LEVEL5_BOUNCE_PADS
    return []


# --- TEXT ON SCREEN ---
def draw_level1_instructions():
    text_surface = INSTRUCTION_FONT.render(
        INSTRUCTION_TEXT,
        True,
        INSTRUCTION_COLOUR
    )
    text_rect = text_surface.get_rect(
        midtop=(WIDTH // 2, 20)  
    )
    screen.blit(text_surface, text_rect)

# --- SPAWNPOINT/STAR DRAW ---
# coordinant points for the star and fill it in
def draw_star(surface, colour, centre, size):
    x, y = centre
    points = [
        (x, y - size),
        (x + size * 0.3, y - size * 0.3),
        (x + size, y - size * 0.3),
        (x + size * 0.4, y + size * 0.1),
        (x + size * 0.6, y + size),
        (x, y + size * 0.5),
        (x - size * 0.6, y + size),
        (x - size * 0.4, y + size * 0.1),
        (x - size, y - size * 0.3),
        (x - size * 0.3, y - size * 0.3)
    ]
    pygame.draw.polygon(surface, colour, points)
    

# ----------------------------------Spike Initialisation Code (includes point in triangle)-----------------------------------------

# --- LOAD SPIKE IMAGE AND SCALE THEM ---
SPIKE_WIDTH = enemy.width
SPIKE_HEIGHT = max(4, enemy.height - SPIKE_HEIGHT_REDUCTION)  

spike_img = pygame.transform.smoothscale(spike_img, (SPIKE_WIDTH, SPIKE_HEIGHT))

# collisions for spikes and enemies (can be toggled on or off)
Enemy_collision = False
Spike_collisions = False

# ---  4 SPIKES FOR GAME SCREEN (The first level) ---
NUM_SPIKES = 4
SPACING = 4  
spikes = []
for _ in range(NUM_SPIKES):
    r = pygame.Rect(0, 0, SPIKE_WIDTH, SPIKE_HEIGHT)
    r.bottom = enemy.bottom  
    spikes.append(r)
group_width = NUM_SPIKES * SPIKE_WIDTH + (NUM_SPIKES - 1) * SPACING
start_x = (WIDTH // 2) - group_width // 2

for i, level_spikes in enumerate(spikes):
    level_spikes.x = start_x + i * (SPIKE_WIDTH + SPACING)

# --- TRIANGLE COLLISION (POINT-IN-TRIANGLE) ---
def point_in_triangle(point, tip, bottom_left, bottom_right):
# The coordinants of the triange points and the last middle point
    (x, y) = point
    (x1, y1) = tip
    (x2, y2) = bottom_left
    (x3, y3) = bottom_right
    denominator = (y2 - y3)*(x1 - x3) + (x3 - x2)*(y1 - y3)
    if abs(denominator) < 1e-9:
        return False
    a = ((y2 - y3)*(x - x3) + (x3 - x2)*(y - y3)) / denominator
    b = ((y3 - y1)*(x - x3) + (x1 - x3)*(y - y3)) / denominator
    c = 1 - a - b
    return (0 <= a <= 1) and (0 <= b <= 1) and (0 <= c <= 1)

def rect_corners(rect):
# collision rectangle positions - to make a triangle
    return [
        (rect.left, rect.top),
        (rect.right, rect.top),
        (rect.right, rect.bottom),
        (rect.left, rect.bottom),
    ]

def point_in_rect(point, rect):
    x, y = point
    return rect.left <= x <= rect.right and rect.top <= y <= rect.bottom

def orientation(a, b, c):
    (x1, y1), (x2, y2), (x3, y3) = a, b, c
    values = (y2 - y1)*(x3 - x2) - (x2 - x1)*(y3 - y2)
    if abs(values) < 1e-9:
        return 0
    return 1 if values > 0 else 2

def on_segment(a, b, c):
    (x1, y1), (x2, y2), (x3, y3) = a, b, c
    return (min(x1, x3) <= x2 <= max(x1, x3)) and (min(y1, y3) <= y2 <= max(y1, y3))

def segments_intersect(p1, q1, p2, q2):
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if o1 != o2 and o3 != o4:
        return True
    if o1 == 0 and on_segment(p1, p2, q1):
        return True
    if o2 == 0 and on_segment(p1, q2, q1):
        return True
    if o3 == 0 and on_segment(p2, p1, q2):
        return True
    if o4 == 0 and on_segment(p2, q1, q2):
        return True
    return False

def spike_triangle_points(s_rect):
    top_point = (s_rect.centerx, s_rect.top)
    bottom_left_point = (s_rect.left, s_rect.bottom)
    bottom_right_point = (s_rect.right, s_rect.bottom)
    return top_point, bottom_left_point, bottom_right_point

def spike_triangle_collides_rect(player_rect, s_rect):
    tip, bottom_left, bottom_right = spike_triangle_points(s_rect)
    for corner in rect_corners(player_rect):
        if point_in_triangle(corner, tip, bottom_left, bottom_right):
            return True
    for vertex in (tip, bottom_left, bottom_right):
        if point_in_rect(vertex, player_rect):
            return True
    triangle_edges = [(tip, bottom_left), (bottom_left, bottom_right), (bottom_right , tip)]
    rc = rect_corners(player_rect)
    rect_edges = [(rc[0], rc[1]), (rc[1], rc[2]), (rc[2], rc[3]), (rc[3], rc[0])]
    for te in triangle_edges:
        for re in rect_edges:
            if segments_intersect(te[0], te[1], re[0], re[1]):
                return True
    return False
# ----------------------------------------------------------------------------------------------------------


# --- SCREEN DRAW (Screen elemeents: buttons and buttons position, backgrounds)---
def draw_start_screen():
    screen.blit(background_img, (0, 0))
    screen.blit(title_img, title_rect)
    
    # Shows the corresponding button pressed image if the button has been pressed
    play_img_to_draw = play_button_pressed_img if play_pressed else play_button_img
    level_img_to_draw = level_button_pressed_img if level_pressed else level_button_img
    settings_img_to_draw = settings_button_pressed_img if settings_pressed else settings_button_img
    credit_img_to_draw = credit_button_pressed_img if credit_pressed else credit_button_img
    
    # Draws the button image and button rectangle on the screen
    screen.blit(credit_img_to_draw, credit_button_rect)
    screen.blit(level_img_to_draw, level_button_rect)
    screen.blit(play_img_to_draw, play_button_rect)
    screen.blit(settings_img_to_draw, settings_button_rect)
 
    if show_credit_image:
        screen.blit(credit_img, credit_rect)
        
arrow_rect = pygame.Rect(20, 20, 120, 120)


def draw_arrow_back():
    screen.blit(back_button_pressed_img if back_pressed else back_button_img, arrow_rect)

def draw_level_select_screen():
    screen.blit(background2_img, (0, 0))
    screen.blit(level_select_text_img, level_select_text_rect)
    draw_arrow_back()

def draw_settings_screen():
    screen.blit(background2_img, (0, 0))
    screen.blit(settings_text_img, settings_text_rect)
    draw_arrow_back()

# --- GAME DRAW ---
def draw_game():
    # Clear the screen
    screen.fill(GAME_BACKGROUND_COLOUR)

    # Draw ground
    pygame.draw.rect(screen, GROUND_COLOUR, (0, ground_y, WIDTH, GROUND_HEIGHT))
    # Draw ghosts and the ghost's required opacity based on how recent the ghost has been created
    total = len(ghosts)
    for i, ghost_configuration in enumerate(ghosts):
        if not ghost_configuration["visible"]:
            continue
        scale = (i + 1) / total if total > 0 else 1.0
        ghost_opacity = int(255 * 0.6 * scale) if ghost_configuration["playing"] else 255
        ghost_colour = (*GHOST_COLOUR, ghost_opacity) if ghost_configuration["playing"] else (*GHOST_SOLID_COLOUR, 255)
        GHOST_SURFACE = pygame.Surface((ghost_configuration["rect"].width, ghost_configuration["rect"].height), pygame.SRCALPHA)
        GHOST_SURFACE.fill(ghost_colour)
        screen.blit(GHOST_SURFACE, ghost_configuration["rect"].topleft)

    # Draw spikes and draw the spike rectangle (will be invisible)
    for level_spikes in spikes:
        screen.blit(spike_img, level_spikes.topleft)
        if Spike_collisions:
            tip, bottom_left_point, bottom_right_point = spike_triangle_points(level_spikes)
            pygame.draw.polygon(screen, (255, 0, 255), [tip, bottom_left_point, bottom_right_point], 2)

    # Draw spawn point star
    draw_star(screen, YELLOW, (spawn_point[0] + 15, spawn_point[1] + 30), 15)

    # Draw the flag using image
    screen.blit(flag_img, flag_rect.topleft)

    # Draw the player 
    pygame.draw.rect(screen, WHITE, player)

    # Draw restart button in top-left
    screen.blit(restart_icon_img, restart_icon_rect)
    draw_level1_instructions()


# Player controls and interactions (with the bounce pad)
def update_player(keys):
    global player_velocity_y, on_ground_player, recording_active, current_recording

    prev_rect = player.copy()
    speed = 6
    moved_or_jumped = False

    # --- Horizontal movement ---
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.x -= speed
        moved_or_jumped = True
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.x += speed
        moved_or_jumped = True

    # --- Jump ---
    if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and on_ground_player:
        player_velocity_y = jump_force
        on_ground_player = False
        moved_or_jumped = True
    
    # --- Bounce pad (collision and function) ---
    for pad in get_active_bounce_pads():
        if player.colliderect(pad) and player_velocity_y >= 0:
            player.bottom = pad.top
            player_velocity_y = jump_force * BOUNCE_MULTIPLIER
            on_ground_player = False
            break


    # --- Gravity ---
    player_velocity_y += gravity
    player.y += player_velocity_y

    # --- Ghost platform collision (player collision on the ghost platform) ---
    for ghost in ghosts:
        if ghost["visible"] and not ghost["playing"]:
            ghost_rect = ghost["rect"]
            if player.colliderect(ghost_rect):
                if prev_rect.bottom <= ghost_rect.top:
                    player.bottom = ghost_rect.top
                    player_velocity_y = 0
                    on_ground_player = True
                elif prev_rect.top >= ghost_rect.bottom:
                    player.top = ghost_rect.bottom
                    player_velocity_y = 0
                elif prev_rect.right <= ghost_rect.left:
                    player.right = ghost_rect.left
                elif prev_rect.left >= ghost_rect.right:
                    player.left = ghost_rect.right

    # ================= LEVEL 2 PLATFORM COLLISION =================
    if current_screen == "level2":
        for platform in LEVEL2_PLATFORMS:
            if player.colliderect(platform):
    
                # Landing on top
                if prev_rect.bottom <= platform.top:
                    player.bottom = platform.top
                    player_velocity_y = 0
                    on_ground_player = True
    
                # Hitting from below
                elif prev_rect.top >= platform.bottom:
                    player.top = platform.bottom
                    player_velocity_y = 0
    
                # Hitting from left
                elif prev_rect.right <= platform.left:
                    player.right = platform.left
    
                # Hitting from right
                elif prev_rect.left >= platform.right:
                    player.left = platform.right

    # ================= LEVEL 3 PLATFORM COLLISION =================
    elif current_screen == "level3":
        for platform in LEVEL3_PLATFORMS:
            if player.colliderect(platform):
                    
                # Landing on top
                if prev_rect.bottom <= platform.top:
                    player.bottom = platform.top
                    player_velocity_y = 0
                    on_ground_player = True
                    
                # Hitting from below
                elif prev_rect.top >= platform.bottom:
                    player.top = platform.bottom
                    player_velocity_y = 0
                    
                # Hitting from left
                elif prev_rect.right <= platform.left:
                    player.right = platform.left
                    
                # Hitting from right
                elif prev_rect.left >= platform.right:
                    player.left = platform.right

    # ================= LEVEL 4 PLATFORM COLLISION =================
    elif current_screen == "level4":
        for platform in LEVEL4_PLATFORMS:
            if player.colliderect(platform):
                    
                # Landing on top
                if prev_rect.bottom <= platform.top:
                    player.bottom = platform.top
                    player_velocity_y = 0
                    on_ground_player = True
                    
                # Hitting from below
                elif prev_rect.top >= platform.bottom:
                    player.top = platform.bottom
                    player_velocity_y = 0
                    
                # Hitting from left
                elif prev_rect.right <= platform.left:
                    player.right = platform.left
                    
                # Hitting from right
                elif prev_rect.left >= platform.right:
                    player.left = platform.right

    # ================= LEVEL 5 PLATFORM COLLISION =================
    elif current_screen == "level5":
        for platform in LEVEL5_PLATFORMS:
            if player.colliderect(platform):

                # landing on top 
                if prev_rect.bottom <= platform.top:
                    player.bottom = platform.top
                    player_velocity_y = 0
                    on_ground_player = True

                # hitting from below
                elif prev_rect.top >= platform.bottom:
                    player.top = platform.bottom
                    player_velocity_y = 0

                # hitting from left
                elif prev_rect.right <= platform.left:
                    player.right = platform.left

                # hitting from right
                elif prev_rect.left >= platform.right:
                    player.left = platform.right

    # --- Ground collision ---
    if player.bottom >= ground_y:
        player.bottom = ground_y
        player_velocity_y = 0
        on_ground_player = True

    # --- Screen bounds ---
    player.left = max(player.left, 0)
    player.right = min(player.right, WIDTH)
    player.top = max(player.top, 0)

    # --- Ghost recording ---
    if moved_or_jumped and not recording_active:
        recording_active = True
        current_recording.clear()
        current_recording.append((player.x, player.y))
    elif recording_active:
        current_recording.append((player.x, player.y))


# Applied gravity to spikes to ensure always on ground
def update_spikes():
    global enemy_velocity_y, on_ground_enemy
    for level_spikes in spikes:
        enemy_velocity_y += gravity
        level_spikes.y += enemy_velocity_y

        if level_spikes.bottom >= ground_y:
            level_spikes.bottom = ground_y
            enemy_velocity_y = 0
            on_ground_enemy = True

# The replay system for the ghosts, playing back frame by frame the recorded positions
def update_ghosts():
    for ghost in ghosts:
        if not ghost["playing"]:
            continue
        if ghost["delay_frames"] > 0:
            ghost["delay_frames"] -= 1
            continue
        if ghost["play_index"] < len(ghost["playback"]):
            gx, gy = ghost["playback"][ghost["play_index"]]
            ghost["rect"].x = gx
            ghost["rect"].y = gy
            ghost["play_index"] += 1
        else:
            ghost["playing"] = False

# Takes the player's previous runs and converts them into ghosts that replay it
def respawn_ghosts_from_history():
    global ghosts
    ghosts = []
    recent_runs = recordings_history[-MAX_GHOSTS:]
    for run in recent_runs:
        if not run:
            continue  
        start_x, start_y = run[0]
        ghost_rect = pygame.Rect(start_x, start_y, player.width, player.height)

        ghost = {
            "rect": ghost_rect,
            "playback": list(run),  
            "visible": True,
            "playing": True,
            "delay_frames": FRAMES_DELAY,
            "play_index": 0
        }

        ghosts.append(ghost)


# restart level and elements code
def restart():
    global player_velocity_y, recording_active, current_recording, recordings_history, ghosts, on_ground_player
    player.x, player.y = spawn_point
    
    player_velocity_y = 0
    current_recording.clear()
    recordings_history.clear()
    ghosts.clear()
    recording_active = False
    
    if player.bottom >= ground_y:
        player.bottom = ground_y      
    else:
        on_ground_player = False




#---------------------------------------------- LEVEL DESIGN (spieks and platform positions) -----------------------------------------------   
# ========== LEVEL 2 DESIGN ===========
LEVEL2_SPAWN_POINT = (120, ground_y - 50)
LEVEL2_SPIKES = []
LEVEL2_PLATFORMS = []
LEVEL2_FLAG_RECT = pygame.Rect(
    WIDTH - 120,
    ground_y - FLAG_SIZE,
    FLAG_SIZE,
    FLAG_SIZE
)


LEVEL2_SPAWN_POINT = (120, ground_y - 50)

# ----- PLATFORMS -----
# The positions of the platforms on the level screen
LEVEL2_PLATFORMS.clear()
LEVEL2_PLATFORMS.extend([   
    pygame.Rect(250, ground_y - 50, 185, 50),
    pygame.Rect(430, ground_y - 150, 50, 200),
    pygame.Rect(630, ground_y - 150, 50, 200),
    pygame.Rect(750, ground_y - 180, 100, 50),
])

# Spike Info
LEVEL2_SPIKES.clear()
LEVEL2_SPIKE_WIDTH = 50
LEVEL2_SPIKE_HEIGHT = SPIKE_HEIGHT

# ----- SPIKES -----
# The positions of the spikes on the level screen
LEVEL2_SPIKES.append(
    pygame.Rect(
        380,
        ground_y - LEVEL2_SPIKE_HEIGHT - 50,
        LEVEL2_SPIKE_WIDTH,
        LEVEL2_SPIKE_HEIGHT
    )
)


LEVEL2_SPIKES.append(
    pygame.Rect(
        480,
        ground_y - LEVEL2_SPIKE_HEIGHT,
        LEVEL2_SPIKE_WIDTH,
        LEVEL2_SPIKE_HEIGHT
    )
)


LEVEL2_SPIKES.append(
    pygame.Rect(
        530,
        ground_y - LEVEL2_SPIKE_HEIGHT,
        LEVEL2_SPIKE_WIDTH,
        LEVEL2_SPIKE_HEIGHT
    )
)


LEVEL2_SPIKES.append(
    pygame.Rect(
        580,
        ground_y - LEVEL2_SPIKE_HEIGHT,
        LEVEL2_SPIKE_WIDTH,
        LEVEL2_SPIKE_HEIGHT
    )
)


LEVEL2_SPIKES.append(
    pygame.Rect(
        750,
        ground_y - LEVEL2_SPIKE_HEIGHT - 180,
        LEVEL2_SPIKE_WIDTH,
        LEVEL2_SPIKE_HEIGHT
    )
)


LEVEL2_SPIKES.append(
    pygame.Rect(
        800,
        ground_y - LEVEL2_SPIKE_HEIGHT - 180,
        LEVEL2_SPIKE_WIDTH,
        LEVEL2_SPIKE_HEIGHT
    )
)


LEVEL2_SPIKES.append(
    pygame.Rect(
        750,
        ground_y - LEVEL2_SPIKE_HEIGHT,
        LEVEL2_SPIKE_WIDTH,
        LEVEL2_SPIKE_HEIGHT
    )
)


LEVEL2_SPIKES.append(
    pygame.Rect(
        800,
        ground_y - LEVEL2_SPIKE_HEIGHT,
        LEVEL2_SPIKE_WIDTH,
        LEVEL2_SPIKE_HEIGHT
    )
)


# ----- FLAG -----
LEVEL2_FLAG_RECT = pygame.Rect(
    WIDTH - 120,
    ground_y - FLAG_SIZE,
    FLAG_SIZE,
    FLAG_SIZE
)

# ================= LEVEL 3 DESIGN =================
LEVEL3_SPAWN_POINT = LEVEL2_SPAWN_POINT  
LEVEL3_PLATFORMS = [] 
LEVEL3_SPIKES = []

# ----- PLATFORMS -----
# The positions of the platforms on the level screen
LEVEL3_PLATFORMS.clear()
LEVEL3_PLATFORMS.extend([   
    pygame.Rect(280, ground_y - 50, 170, 50),
    pygame.Rect(400, ground_y - 100, 50, 50),
    pygame.Rect(580, ground_y - 80, 50, 50),
    pygame.Rect(860, ground_y - 390, 110, 390),
    pygame.Rect(810, ground_y - 240, 80, 240),
    pygame.Rect(760, ground_y - 180, 50, 180),
    pygame.Rect(700, ground_y - 300, 50, 50),
    pygame.Rect(480, ground_y - 300, 50, 50),
    pygame.Rect(180, ground_y - 300, 150, 50),
    pygame.Rect(180, ground_y - 390, 50, 50),
    pygame.Rect(300, ground_y - 445, 450, 50),
    
])

# ----- SPIKES -----
# The positions of the spikes on the level screen
LEVEL3_SPIKE_WIDTH = 50
LEVEL3_SPIKE_HEIGHT = SPIKE_HEIGHT
LEVEL3_SPIKES.append(
    pygame.Rect(
        460,  
        ground_y - LEVEL3_SPIKE_HEIGHT,
        LEVEL3_SPIKE_WIDTH,
        LEVEL3_SPIKE_HEIGHT
    )
)


LEVEL3_SPIKES.append(
    pygame.Rect(
        510,  
        ground_y - LEVEL3_SPIKE_HEIGHT,
        LEVEL3_SPIKE_WIDTH,
        LEVEL3_SPIKE_HEIGHT
    )
)


LEVEL3_SPIKES.append(
    pygame.Rect(
        650,  
        ground_y - LEVEL3_SPIKE_HEIGHT,
        LEVEL3_SPIKE_WIDTH,
        LEVEL3_SPIKE_HEIGHT
    )
)


LEVEL3_SPIKES.append(
    pygame.Rect(
        700,  
        ground_y - LEVEL3_SPIKE_HEIGHT,
        LEVEL3_SPIKE_WIDTH,
        LEVEL3_SPIKE_HEIGHT
    )
)


LEVEL3_SPIKES.append(
    pygame.Rect(
        580,  
        ground_y - LEVEL3_SPIKE_HEIGHT - 80,
        LEVEL3_SPIKE_WIDTH,
        LEVEL3_SPIKE_HEIGHT
    )
)


LEVEL3_SPIKES.append(
    pygame.Rect(
        180,  
        ground_y - LEVEL3_SPIKE_HEIGHT - 300,
        LEVEL3_SPIKE_WIDTH,
        LEVEL3_SPIKE_HEIGHT
    )
)

LEVEL3_FLAG_RECT = LEVEL2_FLAG_RECT.copy()  

# ====================== LEVEL 4 DESIGN =========================
LEVEL4_SPAWN_POINT = LEVEL2_SPAWN_POINT
LEVEL4_PLATFORMS = []
LEVEL4_SPIKES = []
LEVEL4_UPSIDE_SPIKES = []
LEVEL4_SAWS = []

# ---- PLATFORM ----
# The positions of the platforms on the level screen
LEVEL4_PLATFORMS.clear()
LEVEL4_PLATFORMS.extend([
    pygame.Rect(230, ground_y - 140, 100, 200),
    pygame.Rect(480, ground_y - 50, 150, 50),
    pygame.Rect(830, ground_y - 130, 50, 130),
])


# --- BOUNCE PADS ---
# The positions of bounce pads on the level screen
LEVEL4_BOUNCE_PADS = [
    pygame.Rect(200, ground_y - 5, *BOUNCE_PAD_SIZE),
    pygame.Rect(600, ground_y - 55, *BOUNCE_PAD_SIZE),
    
]


# ---- SPIKES ----
# The positions of the spikes on the level screen
LEVEL4_SPIKES.append(
    pygame.Rect(
        330,
        ground_y - SPIKE_HEIGHT,
        50,
        SPIKE_HEIGHT
    )
)


LEVEL4_SPIKES.append(
    pygame.Rect(
        380,
        ground_y - SPIKE_HEIGHT,
        50,
        SPIKE_HEIGHT
    )
)


LEVEL4_SPIKES.append(
    pygame.Rect(
        430,
        ground_y - SPIKE_HEIGHT,
        50,
        SPIKE_HEIGHT
    )
)


LEVEL4_SPIKES.append(
    pygame.Rect(
        780,
        ground_y - SPIKE_HEIGHT,
        50,
        SPIKE_HEIGHT
    )
)


LEVEL4_SPIKES.append(
    pygame.Rect(
        680,
        ground_y - SPIKE_HEIGHT,
        50,
        SPIKE_HEIGHT
    )
)


LEVEL4_SPIKES.append(
    pygame.Rect(
        630,
        ground_y - SPIKE_HEIGHT,
        50,
        SPIKE_HEIGHT
    )
)


LEVEL4_SPIKES.append(
    pygame.Rect(
        730,
        ground_y - SPIKE_HEIGHT,
        50,
        SPIKE_HEIGHT
    )
)


LEVEL4_SPIKES.append(
    pygame.Rect(
        830,
        ground_y - SPIKE_HEIGHT - 130,
        50,
        SPIKE_HEIGHT
    )
)

LEVEL4_FLAG_RECT = LEVEL2_FLAG_RECT.copy()


# ====================== LEVEL 5 DESIGN =========================
LEVEL5_SPAWN_POINT = LEVEL2_SPAWN_POINT
LEVEL5_PLATFORMS = []
LEVEL5_SPIKES = []

# ---- PLATFORM ----
# The positions of the platforms on the level screen
LEVEL5_PLATFORMS.clear()
LEVEL5_PLATFORMS.extend([
    pygame.Rect(375, ground_y - 130, 150, 20),
    pygame.Rect(475, ground_y - 205, 50, 20),
    pygame.Rect(250, ground_y - 190, 50, 20),
    pygame.Rect(375, ground_y - 280, 150, 20),
    pygame.Rect(600, ground_y - 130, 150, 20),
    pygame.Rect(600, ground_y - 280, 150, 20),
    pygame.Rect(600, ground_y - 355, 50, 20),
    pygame.Rect(600, ground_y - 430, 50, 20),
    pygame.Rect(800, ground_y - 100, 50, 20),
    pygame.Rect(900, ground_y - 75, 50, 20),
    pygame.Rect(900, ground_y - 150, 50, 20),
    pygame.Rect(900, ground_y - 225, 150, 20),
    pygame.Rect(900, ground_y - 300, 50, 20),
    pygame.Rect(1000, ground_y - 300, 50, 20),
    pygame.Rect(900, ground_y - 375, 150, 20),
])

# --- BOUNCE PADS ---
# The positions of bounce pads on the level screen
LEVEL5_BOUNCE_PADS = [
    pygame.Rect(305, ground_y - 5, *BOUNCE_PAD_SIZE),
    pygame.Rect(340, ground_y - 5, *BOUNCE_PAD_SIZE),
    pygame.Rect(260, ground_y - 195, *BOUNCE_PAD_SIZE),
    pygame.Rect(530, ground_y - 5, *BOUNCE_PAD_SIZE),
    pygame.Rect(565, ground_y - 5, *BOUNCE_PAD_SIZE),
    pygame.Rect(710, ground_y - 285, *BOUNCE_PAD_SIZE),
    pygame.Rect(810, ground_y - 105, *BOUNCE_PAD_SIZE),
]

# ---- SPIKE ----
# The positions of the spikes on the level screen
#ground spikes
LEVEL5_SPIKES.append(
    pygame.Rect(
        250,
        ground_y - SPIKE_HEIGHT,
        50,
        SPIKE_HEIGHT
    )
)


LEVEL5_SPIKES.append(
    pygame.Rect(
        375,
        ground_y - SPIKE_HEIGHT,
        50,
        SPIKE_HEIGHT
    )
)


LEVEL5_SPIKES.append(
    pygame.Rect(
        425,
        ground_y - SPIKE_HEIGHT,
        50,
        SPIKE_HEIGHT
    )
)


LEVEL5_SPIKES.append(
    pygame.Rect(
        475,
        ground_y - SPIKE_HEIGHT,
        50,
        SPIKE_HEIGHT
    )
)


LEVEL5_SPIKES.append(
    pygame.Rect(
        600,
        ground_y - SPIKE_HEIGHT,
        50,
        SPIKE_HEIGHT
    )
)


LEVEL5_SPIKES.append(
    pygame.Rect(
        650,
        ground_y - SPIKE_HEIGHT,
        50,
        SPIKE_HEIGHT
    )
)


LEVEL5_SPIKES.append(
    pygame.Rect(
        700,
        ground_y - SPIKE_HEIGHT,
        50,
        SPIKE_HEIGHT
    )
)


LEVEL5_SPIKES.append(
    pygame.Rect(
        750,
        ground_y - SPIKE_HEIGHT,
        50,
        SPIKE_HEIGHT
    )
)


LEVEL5_SPIKES.append(
    pygame.Rect(
        800,
        ground_y - SPIKE_HEIGHT,
        50,
        SPIKE_HEIGHT
    )
)


LEVEL5_SPIKES.append(
    pygame.Rect(
        850,
        ground_y - SPIKE_HEIGHT,
        50,
        SPIKE_HEIGHT
    )
)


LEVEL5_SPIKES.append(
    pygame.Rect(
        900,
        ground_y - SPIKE_HEIGHT,
        50,
        SPIKE_HEIGHT
    )
)

# platform spikes
LEVEL5_SPIKES.append(
    pygame.Rect(
        475,
        ground_y - SPIKE_HEIGHT - 130,
        50,
        SPIKE_HEIGHT
    )
)


LEVEL5_SPIKES.append(
    pygame.Rect(
        475,
        ground_y - SPIKE_HEIGHT - 205,
        50,
        SPIKE_HEIGHT
    )
)

LEVEL5_SPIKES.append(
    pygame.Rect(
        375,
        ground_y - SPIKE_HEIGHT - 280,
        50,
        SPIKE_HEIGHT
    )
)
LEVEL5_SPIKES.append(
    pygame.Rect(
        700,
        ground_y - SPIKE_HEIGHT - 130,
        50,
        SPIKE_HEIGHT
    )
)


LEVEL5_SPIKES.append(
    pygame.Rect(
        600,
        ground_y - SPIKE_HEIGHT - 280,
        50,
        SPIKE_HEIGHT
    )
)


LEVEL5_SPIKES.append(
    pygame.Rect(
        600,
        ground_y - SPIKE_HEIGHT - 355,
        50,
        SPIKE_HEIGHT
    )
)

LEVEL5_SPIKES.append(
    pygame.Rect(
        600,
        ground_y - SPIKE_HEIGHT - 430,
        50,
        SPIKE_HEIGHT
    )
)

LEVEL5_SPIKES.append(
    pygame.Rect(
        900,
        ground_y - SPIKE_HEIGHT - 75,
        50,
        SPIKE_HEIGHT
    )
)

LEVEL5_SPIKES.append(
    pygame.Rect(
        900,
        ground_y - SPIKE_HEIGHT - 150,
        50,
        SPIKE_HEIGHT
    )
)


LEVEL5_SPIKES.append(
    pygame.Rect(
        1000,
        ground_y - SPIKE_HEIGHT - 225,
        50,
        SPIKE_HEIGHT
    )
)


LEVEL5_SPIKES.append(
    pygame.Rect(
        1000,
        ground_y - SPIKE_HEIGHT - 300,
        50,
        SPIKE_HEIGHT
    )
)


LEVEL5_FLAG_RECT = LEVEL2_FLAG_RECT.copy()
#-----------------------------------------------------------------------------------------------------------






# --- HANDLE COLLISION (collision code that is initialised in each level)---
def handle_collision():
    global player_velocity_y, recording_active, current_recording
    global recordings_history, ghosts, current_screen, on_ground_player

    # ================= LEVEL 1 =================
    if current_screen == "game":
        # Initialise the result of spike collisions 
        for level_spikes in spikes:
            if spike_triangle_collides_rect(player, level_spikes):
                
                # Creates ghosts based on the run
                if current_recording:
                    recordings_history.append(list(current_recording))
                    recordings_history = recordings_history[-MAX_GHOSTS:]
                    respawn_ghosts_from_history()

                # sends the player to spawnpoint and resets the recording of the currently active ghost
                player.x, player.y = spawn_point
                player_velocity_y = 0
                recording_active = False
                current_recording.clear()
                on_ground_player = False

                if player.bottom >= ground_y:
                    player.bottom = ground_y
                    on_ground_player = True
                return
            
        # Initialise Flag collisions with the player (sends to next level)
        if player.colliderect(flag_rect):
            current_screen = "level2"
            restart()
            player.x, player.y = LEVEL2_SPAWN_POINT
            return

    # ================= LEVEL 2 =================
    elif current_screen == "level2":

        # --- Spike collision ---
        # Initialise the result of spike collisions 
        for level_spikes in LEVEL2_SPIKES:
            if spike_triangle_collides_rect(player, level_spikes):
                if current_recording:
                    recordings_history.append(list(current_recording))
                    recordings_history = recordings_history[-MAX_GHOSTS:]
                    respawn_ghosts_from_history()
                
                # sends the player to spawnpoint and resets the recording of the currently active ghost
                recording_active = False
                current_recording.clear()                  
                player.x, player.y = LEVEL2_SPAWN_POINT
                player_velocity_y = 0
                on_ground_player = False
                
                
                if player.bottom >= ground_y:
                    player.bottom = ground_y
                    on_ground_player = True
                return
        if player.colliderect(flag_rect):
            current_screen = "level3"
            restart()
            player.x, player.y = LEVEL2_SPAWN_POINT
            return 

        # --- Flag ---
        if player.colliderect(LEVEL2_FLAG_RECT):
            print("Level 2 complete")
            return
    
    # =================== LEVEL 3 ====================
    elif current_screen == "level3":
        # Spike collision
        for level_spikes in LEVEL3_SPIKES:
            if spike_triangle_collides_rect(player, level_spikes):
                if current_recording:
                    recordings_history.append(list(current_recording))
                    recordings_history = recordings_history[-MAX_GHOSTS:]
                    respawn_ghosts_from_history()
        
                recording_active = False
                current_recording.clear()
                player.x, player.y = LEVEL3_SPAWN_POINT
                player_velocity_y = 0
                
                on_ground_player = False
                if player.bottom >= ground_y:
                    player.bottom = ground_y
                    on_ground_player = True
                return
            
        if player.colliderect(flag_rect):
            current_screen = "level4"
            restart()
            player.x, player.y = LEVEL2_SPAWN_POINT
            return 
        
        # Flag collision
        if player.colliderect(LEVEL3_FLAG_RECT):
            print("Level 3 complete")
            return
        
    # =================== LEVEL 4 ====================
    elif current_screen == "level4":
        
        for level_spikes in LEVEL4_SPIKES:
            if spike_triangle_collides_rect(player, level_spikes):
        
                if current_recording:
                    recordings_history.append(list(current_recording))
                    recordings_history = recordings_history[-MAX_GHOSTS:]
                    respawn_ghosts_from_history()
        
                recording_active = False
                current_recording.clear()
                player.x, player.y = LEVEL4_SPAWN_POINT
                player_velocity_y = 0
                on_ground_player = False
        
                if player.bottom >= ground_y:
                    player.bottom = ground_y
                    on_ground_player = True
                return
        
        if player.colliderect(flag_rect):
            current_screen = "level5"
            restart()
            player.x, player.y = LEVEL2_SPAWN_POINT
            return
        
        if player.colliderect(LEVEL4_FLAG_RECT):
            print("Level 4 complete")
            return

    # =================== LEVEL 5 ====================
    elif current_screen == "level5":

        # --- Spike collision ---
        for level_spikes in LEVEL5_SPIKES:
            if spike_triangle_collides_rect(player, level_spikes):

                if current_recording:
                    recordings_history.append(list(current_recording))
                    recordings_history = recordings_history[-MAX_GHOSTS:]
                    respawn_ghosts_from_history()

                recording_active = False
                current_recording.clear()
                player.x, player.y = LEVEL5_SPAWN_POINT
                player_velocity_y = 0
                on_ground_player = False

                if player.bottom >= ground_y:
                    player.bottom = ground_y
                    on_ground_player = True
                return

        # --- Flag ---
        if player.colliderect(LEVEL5_FLAG_RECT):
            current_screen = "end"
            return






# ------------------------------- LEVELS FUNCTIONS (Level element initialisations when drawing a level) --------------------------------------------
# --- DRAW LEVEL 2 ---
def draw_level2():
    screen.fill(GAME_BACKGROUND_COLOUR)

    # --- ground ---
    # Drawing the ground onto the screen
    pygame.draw.rect(
        screen,
        LEVEL2_PLATFORM_COLOUR,
        (0, ground_y, WIDTH, GROUND_HEIGHT)
    )

    # --- platforms ---
    # Drawing the platforms  onto the screen
    for platform in LEVEL2_PLATFORMS:
        pygame.draw.rect(screen, LEVEL2_PLATFORM_COLOUR, platform)

    # --- spikes ---
    # Drawing the spikes onto the screen and initialising the spike collision
    for level_spikes in LEVEL2_SPIKES:
        screen.blit(spike_img, level_spikes.topleft)
        if Spike_collisions:
            tip, bottom_left_point, bottom_right_point = spike_triangle_points(level_spikes)
            pygame.draw.polygon(screen, (255, 0, 255), [tip, bottom_left_point, bottom_right_point], 2)

    # --- ghosts ---
    # draws the ghost on to the screen (including the opacity)
    total = len(ghosts)
    for i, ghost_configuration in enumerate(ghosts):
        if not ghost_configuration["visible"]:
            continue
        scale = (i + 1) / total if total > 0 else 1.0
        ghost_opacity = int(255 * 0.6 * scale) if ghost_configuration["playing"] else 255
        ghost_colour = (*GHOST_COLOUR, ghost_opacity) if ghost_configuration["playing"] else (*GHOST_SOLID_COLOUR, 255)
        GHOST_SURFACE = pygame.Surface(ghost_configuration["rect"].size, pygame.SRCALPHA)
        GHOST_SURFACE.fill(ghost_colour)
        screen.blit(GHOST_SURFACE, ghost_configuration["rect"].topleft)

    # Drawing the star, flag image, player and restart button image onto the screen
    draw_star(screen,YELLOW,(LEVEL2_SPAWN_POINT[0] + 15, LEVEL2_SPAWN_POINT[1] + 30),15)
    screen.blit(flag_img, LEVEL2_FLAG_RECT.topleft)
    pygame.draw.rect(screen, WHITE, player)
    screen.blit(restart_icon_img, restart_icon_rect)
    


def draw_level3():
    screen.fill(GAME_BACKGROUND_COLOUR)

    # --- Ground ---
    # Drawing the ground onto the screen
    pygame.draw.rect(screen, LEVEL2_PLATFORM_COLOUR, (0, ground_y, WIDTH, GROUND_HEIGHT))

    # --- Platforms ---
    # Drawing the platforms  onto the screen   
    for platform in LEVEL3_PLATFORMS:
        pygame.draw.rect(screen, LEVEL2_PLATFORM_COLOUR, platform)

    # --- Spikes ---
    # Drawing the spikes onto the screen and initialising the spike collision 
    for level_spikes in LEVEL3_SPIKES:
        screen.blit(spike_img, level_spikes.topleft)
        if Spike_collisions:
            tip, bottom_left_point, bottom_right_point = spike_triangle_points(level_spikes)
            pygame.draw.polygon(screen, (255, 0, 255), [tip, bottom_left_point, bottom_right_point], 2)

    # --- Ghosts ---
    # draws the ghost on to the screen (including the opacity)
    total = len(ghosts)
    for i, ghost_configuration in enumerate(ghosts):
        if not ghost_configuration["visible"]:
            continue
        scale = (i + 1) / total if total > 0 else 1.0
        ghost_opacity = int(255 * 0.6 * scale) if ghost_configuration["playing"] else 255
        ghost_colour = (*GHOST_COLOUR, ghost_opacity) if ghost_configuration["playing"] else (*GHOST_SOLID_COLOUR, 255)
        GHOST_SURFACE = pygame.Surface(ghost_configuration["rect"].size, pygame.SRCALPHA)
        GHOST_SURFACE.fill(ghost_colour)
        screen.blit(GHOST_SURFACE, ghost_configuration["rect"].topleft)

    # Drawing the star, flag image, player and restart button image onto the screen
    draw_star(screen, YELLOW, (LEVEL3_SPAWN_POINT[0] + 15, LEVEL3_SPAWN_POINT[1] + 30), 15)
    screen.blit(flag_img, LEVEL3_FLAG_RECT.topleft)
    pygame.draw.rect(screen, WHITE, player)
    screen.blit(restart_icon_img, restart_icon_rect)



def draw_level4():
    screen.fill(GAME_BACKGROUND_COLOUR)

    # Drawing the bounce pads onto the screen for the level
    pygame.draw.rect(screen, LEVEL2_PLATFORM_COLOUR, (0, ground_y, WIDTH, GROUND_HEIGHT))
    for pad in get_active_bounce_pads():
        pygame.draw.rect(screen, YELLOW, pad)
    for platform in LEVEL4_PLATFORMS:
        pygame.draw.rect(screen, LEVEL2_PLATFORM_COLOUR, platform)
    for level_spikes in LEVEL4_SPIKES:
        screen.blit(spike_img, level_spikes.topleft)
    for level_spikes in LEVEL4_UPSIDE_SPIKES:
        flipped_spike = pygame.transform.flip(spike_img, False, True)
        screen.blit(flipped_spike, level_spikes.topleft)

    # Ghosts
    # draws the ghost on to the screen (including the opacity)
    total = len(ghosts)
    for i, ghost_configuration in enumerate(ghosts):
        if not ghost_configuration["visible"]:
            continue
        scale = (i + 1) / total if total > 0 else 1
        ghost_opacity = int(255 * 0.6 * scale) if ghost_configuration["playing"] else 255
        ghost_colour = (*GHOST_COLOUR, ghost_opacity) if ghost_configuration["playing"] else (*GHOST_SOLID_COLOUR, 255)
        GHOST_SURFACE = pygame.Surface(ghost_configuration["rect"].size, pygame.SRCALPHA)
        GHOST_SURFACE.fill(ghost_colour)
        screen.blit(GHOST_SURFACE, ghost_configuration["rect"].topleft)

    # Drawing the star, flag image, player and restart button image onto the screen
    draw_star(screen, YELLOW, (LEVEL4_SPAWN_POINT[0] + 15, LEVEL4_SPAWN_POINT[1] + 30), 15)
    screen.blit(flag_img, LEVEL4_FLAG_RECT.topleft)
    pygame.draw.rect(screen, WHITE, player)
    screen.blit(restart_icon_img, restart_icon_rect)
  
    
    
def draw_level5():
    screen.fill(GAME_BACKGROUND_COLOUR)

    # --- Ground ---
    # Drawing the ground onto the screen
    pygame.draw.rect(screen, LEVEL2_PLATFORM_COLOUR, (0, ground_y, WIDTH, GROUND_HEIGHT))

    # --- bounce pads ---
    # Drawing the bounce pads onto the screen
    for pad in get_active_bounce_pads():
        pygame.draw.rect(screen, YELLOW, pad)    
    
    # --- Platforms ---
    # Drawing the platforms onto the screen
    for platform in LEVEL5_PLATFORMS:
        pygame.draw.rect(screen, LEVEL2_PLATFORM_COLOUR, platform)

    # --- Spikes ---
    # Drawing the spikes onto the screen
    for level_spikes in LEVEL5_SPIKES:
        screen.blit(spike_img, level_spikes.topleft)

    # --- Ghosts ---
    # draws the ghost on to the screen (including the opacity)
    total = len(ghosts)
    for i, ghost_configuration in enumerate(ghosts):
        if not ghost_configuration["visible"]:
            continue
        scale = (i + 1) / total if total > 0 else 1.0
        ghost_opacity = int(255 * 0.6 * scale) if ghost_configuration["playing"] else 255
        ghost_colour = (*GHOST_COLOUR, ghost_opacity) if ghost_configuration["playing"] else (*GHOST_SOLID_COLOUR, 255)
        GHOST_SURFACE = pygame.Surface(ghost_configuration["rect"].size, pygame.SRCALPHA)
        GHOST_SURFACE.fill(ghost_colour)
        screen.blit(GHOST_SURFACE, ghost_configuration["rect"].topleft)

    # Drawing the star, flag image, player and restart button image onto the screen
    draw_star(screen,YELLOW,(LEVEL5_SPAWN_POINT[0] + 15, LEVEL5_SPAWN_POINT[1] + 30),15)
    screen.blit(flag_img, LEVEL5_FLAG_RECT.topleft)
    pygame.draw.rect(screen, WHITE, player)
    screen.blit(restart_icon_img, restart_icon_rect)

def draw_end_screen():
    screen.blit(background2_img, (0, 0))

    # Congrats image
    congrats_rect = congrats_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))
    screen.blit(congrats_img, congrats_rect)

    # End text
    text_surface = END_FONT.render(END_TEXT, True, INSTRUCTION_COLOUR)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70))
    screen.blit(text_surface, text_rect)

    # Home button
    home_img_to_draw = home_button_pressed_img if home_pressed else home_button_img
    screen.blit(home_img_to_draw, home_button_rect)
#------------------------------------------------------------------------------------------------------------




# --- MAIN LOOP ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            # end screen home button
            if current_screen == "end":
                if home_button_rect.collidepoint(mouse_pos):
                    home_pressed = True

            # restart button click validation 
            if current_screen not in ("start", "level_select", "settings"):
                if restart_icon_rect.collidepoint(mouse_pos):
                    restart_pressed = True
    
            # --- menu buttons ---
            if current_screen == "start":
                if play_button_rect.collidepoint(mouse_pos):
                    play_pressed = True
                elif level_button_rect.collidepoint(mouse_pos):
                    level_pressed = True
                elif settings_button_rect.collidepoint(mouse_pos):
                    settings_pressed = True
                elif credit_button_rect.collidepoint(mouse_pos):
                    credit_pressed = True
            elif current_screen in ("level_select", "settings"):
                if arrow_rect.collidepoint(mouse_pos):
                    back_pressed = True
    
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = event.pos
            
            # end screen home button
            if current_screen == "end":
                if home_button_rect.collidepoint(mouse_pos) and home_pressed:
                    pending_screen = "start"
                    screen_change_delay = pygame.time.get_ticks() + 100
                home_pressed = False

            # restart button validation (if it actually has been pressed - restart_pressed = true - restarts the screen)
            if current_screen not in ("start", "level_select", "settings"):
                if restart_icon_rect.collidepoint(mouse_pos) and restart_pressed:
                    restart()
                restart_pressed = False
    
            # --- menu button pressed ---
            if current_screen == "start":
                if play_button_rect.collidepoint(mouse_pos) and play_pressed:
                    reset_full_game()
                    pending_screen = "game"
                    screen_change_delay = pygame.time.get_ticks() + 100
                elif level_button_rect.collidepoint(mouse_pos) and level_pressed:
                    pending_screen = "level_select"
                    screen_change_delay = pygame.time.get_ticks() + 100
                elif settings_button_rect.collidepoint(mouse_pos) and settings_pressed:
                    pending_screen = "settings"
                    screen_change_delay = pygame.time.get_ticks() + 100
                elif credit_button_rect.collidepoint(mouse_pos) and credit_pressed:
                    show_credit_image = True
                else:
                    show_credit_image = False
    
                play_pressed = level_pressed = settings_pressed = credit_pressed = False
    
            elif current_screen in ("level_select", "settings"):
                if arrow_rect.collidepoint(mouse_pos) and back_pressed:
                    pending_screen = "start"
                    screen_change_delay = pygame.time.get_ticks() + 100
                back_pressed = False 


        # Restart Key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                if current_screen not in ("start", "level_select", "settings"):
                    restart()

    # Handle delayed screen changes
    if pending_screen is not None and pygame.time.get_ticks() >= screen_change_delay:
        current_screen = pending_screen
        pending_screen = None

    # --- SCREENS ---
    # Screen music
    if current_screen == "start":
        draw_start_screen()
        play_music("menu")
    elif current_screen == "level_select":
        draw_level_select_screen()
        play_music("menu")
    elif current_screen == "settings":
        draw_settings_screen()
        play_music("menu")
        
    # Game screen (level 1) functions
    elif current_screen == "game":
        play_music(difficulty_level)
        keys = pygame.key.get_pressed()
        update_player(keys)
        update_spikes()
        handle_collision()
        update_ghosts()
        draw_game()
    
    # Level 2 functions
    elif current_screen == "level2":
        keys = pygame.key.get_pressed()
        update_player(keys)
        handle_collision()
        update_ghosts()
        draw_level2()

    # Level 3 functions
    elif current_screen == "level3":
        keys = pygame.key.get_pressed()
        update_player(keys)
        handle_collision()
        update_ghosts()
        draw_level3()
    
    # Level 4 functions
    elif current_screen == "level4":
        keys = pygame.key.get_pressed()
        update_player(keys)
        handle_collision()
        update_ghosts()
        draw_level4()
    
    # Level 5 functions    
    elif current_screen == "level5":
        keys = pygame.key.get_pressed()
        update_player(keys)
        handle_collision()
        update_ghosts()
        draw_level5()
    
    # Level end screen functions
    elif current_screen == "end":
        draw_end_screen()

    pygame.display.flip()
    clock.tick(FPS)





