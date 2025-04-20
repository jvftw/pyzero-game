import random
from pgzero.builtins import Actor, Rect, keyboard, sounds, clock

WIDTH = 1000
HEIGHT = 600
TITLE = "HERO JUMP"

MENU = 0
PLAYING = 1
game_state = MENU

music_on = True
sound_on = True

groundcolour = (0, 0, 139)
floor = Rect((0, 580), (1000, 20))

heroi = Actor("jumper-1", (500, 250))
heroi_x_velocity = 0
heroi_y_velocity = 0
gravity = 1
jumping = False
jumped = False
allowx = True

platforms = [
    Rect((450, 500), (100, 10)),
    Rect((300, 400), (100, 10)),
    Rect((600, 400), (100, 10)),
    Rect((200, 300), (100, 10)),
    Rect((700, 300), (100, 10)),
    Rect((100, 200), (100, 10)),
    Rect((800, 200), (100, 10)),
    Rect((0, 100), (100, 10)),
    Rect((900, 100), (100, 10)),
    floor
]

plat61_x, plat62_x = 200, 700
platform61 = Rect((plat61_x, 200), (100, 10))
platform62 = Rect((plat62_x, 200), (100, 10))
platforms.append(platform61)
platforms.append(platform62)
plat61left = plat62left = True

class Inimigo:
    def __init__(self):
        plataforma = random.choice(platforms[:-3])
        x = random.randint(int(plataforma.left) + 20, int(plataforma.right) - 20)
        y = plataforma.top - 20
        self.actor = Actor("redjumper-1", (x, y))
        self.x_velocity = random.choice([-2, 2])
        self.y_velocity = 0
        self.jump_timer = random.randint(0, 60)
        self.move_timer = 0
        self.jumping = False

inimigo1 = Inimigo()
inimigo2 = Inimigo()

diamond_positions = [(950, 70), (50, 70), (850, 170), (150, 170),
                    (750, 270), (250, 270), (650, 370), (350, 370), (500, 470)]
gem = Actor("diamond_s", random.choice(diamond_positions))
points = 0
vidas = 3

start_button = Rect((WIDTH/2 - 100, HEIGHT/2 - 80), (200, 50))
sound_button = Rect((WIDTH/2 - 100, HEIGHT/2), (200, 50))
exit_button = Rect((WIDTH/2 - 100, HEIGHT/2 + 80), (200, 50))

def draw():
    if game_state == MENU:
        draw_menu()
    elif game_state == PLAYING:
        draw_game()

def draw_menu():
    screen.fill((173, 216, 230))
    screen.blit("skyline_large", (0, 0))
    screen.draw.text("HERO JUMP", center=(WIDTH/2, HEIGHT/4), fontsize=70, shadow=(2, 2), color=(255, 255, 255), scolor="#202020")
    screen.draw.filled_rect(start_button, (0, 100, 0))
    screen.draw.text("START", center=start_button.center, fontsize=30, color=(255, 255, 255))
    sound_text = "MUSIC: ON" if sound_on else "MUSIC: OFF"
    screen.draw.filled_rect(sound_button, (100, 0, 0))
    screen.draw.text(sound_text, center=sound_button.center, fontsize=30, color=(255, 255, 255))
    screen.draw.filled_rect(exit_button, (100, 100, 0))
    screen.draw.text("EXIT", center=exit_button.center, fontsize=30, color=(255, 255, 255))

def draw_game():
    screen.fill((173, 216, 230))
    screen.blit("skyline_large", (0, 0))
    platform61.x = plat61_x
    platform62.x = plat62_x
    for platform in platforms:
        screen.draw.filled_rect(platform, groundcolour)
    heroi.draw()
    inimigo1.actor.draw()
    inimigo2.actor.draw()
    gem.draw()
    screen.draw.text("LOOT:", center=(50, 540), fontsize=40, shadow=(1,1), color=(255,255,255), scolor="#202020")
    screen.draw.text(str(points), center=(45, 570), fontsize=40, shadow=(1,1), color=(255,255,255), scolor="#202020")
    screen.draw.text("LIVES:", center=(950, 540), fontsize=40, shadow=(1,1), color=(255,255,255), scolor="#202020")
    screen.draw.text(str(vidas), center=(945, 570), fontsize=40, shadow=(1,1), color=(255,255,255), scolor="#202020")

def update(dt):
    if game_state == PLAYING:
        mover_plataformas()
        heroi_move(dt)
        mover_inimigo(inimigo1)
        mover_inimigo(inimigo2)
        if heroi.colliderect(inimigo1.actor) or heroi.colliderect(inimigo2.actor):
            perder_vida()

def mover_plataformas():
    global plat61_x, plat62_x, plat61left, plat62left
    if plat61left:
        plat61_x += 2
        if plat61_x >= 400: plat61left = False
    else:
        plat61_x -= 2
        if plat61_x <= 200: plat61left = True
    if plat62left:
        plat62_x += 2
        if plat62_x >= 700: plat62left = False
    else:
        plat62_x -= 2
        if plat62_x <= 500: plat62left = True
    platform61.x = plat61_x
    platform62.x = plat62_x

def mover_inimigo(inimigo):
    inimigo.move_timer += 1
    if inimigo.move_timer > 60:
        inimigo.move_timer = 0
        inimigo.x_velocity = random.choice([-2, -1, 1, 2])
    inimigo.jump_timer += 1
    if inimigo.jump_timer > 90 and not inimigo.jumping and esta_sobre_plataforma(inimigo.actor, inimigo.y_velocity):
        inimigo.jump_timer = 0
        inimigo.y_velocity = -12
        inimigo.jumping = True
        inimigo.actor.image = "redjumper-up"
    if not esta_sobre_plataforma(inimigo.actor, inimigo.y_velocity):
        inimigo.y_velocity += 0.5
        if inimigo.y_velocity > 0:
            inimigo.actor.image = "redjumper-fall"
    else:
        if inimigo.jumping:
            inimigo.jumping = False
        inimigo.y_velocity = 0
    inimigo.actor.x += inimigo.x_velocity
    inimigo.actor.y += inimigo.y_velocity
    if inimigo.actor.x < 30:
        inimigo.actor.x = 30
        inimigo.x_velocity = random.randint(0, 2)
    elif inimigo.actor.x > WIDTH - 30:
        inimigo.actor.x = WIDTH - 30
        inimigo.x_velocity = random.randint(-2, 0)
    if inimigo.x_velocity > 0:
        inimigo.actor.image = "redjumper-right"
    elif inimigo.x_velocity < 0:
        inimigo.actor.image = "redjumper-left"
    elif not inimigo.jumping:
        inimigo.actor.image = "redjumper-1"

def esta_sobre_plataforma(ator, y_velocity):
    for platform in platforms:
        if (ator.colliderect(platform) and
            ator.bottom <= platform.top + 15 and
            y_velocity >= 0):
            ator.bottom = platform.top + 1
            return True
    return False

def heroi_move(dt):
    global heroi_x_velocity, heroi_y_velocity, jumping, gravity, jumped, allowx, points
    if heroi_x_velocity == 0 and not jumped:
        heroi.image = "jumper-1"
    if esta_sobre_plataforma(heroi, heroi_y_velocity):
        gravity = 1
        allowx = True
        if jumping:
            jumping = False
    else:
        heroi.y += gravity
        if gravity <= 20:
            gravity += 0.5
    if (keyboard.left) and allowx:
        if (heroi.x > 40) and (heroi_x_velocity > -8):
            heroi_x_velocity -= 2
            heroi.image = "jumper-left"
            if (keyboard.left) and jumped:
                heroi.image = "jumper-jleft"
    if (keyboard.right) and allowx:
        if (heroi.x < 960) and (heroi_x_velocity < 8):
            heroi_x_velocity += 2
            heroi.image = "jumper-right"
            if (keyboard.right) and jumped:
                heroi.image = "jumper-jright"
    heroi.x += heroi_x_velocity
    if heroi_x_velocity > 0:
        heroi_x_velocity -= 1
    elif heroi_x_velocity < 0:
        heroi_x_velocity += 1
    if heroi.x < 50 or heroi.x > 950:
        heroi_x_velocity = 0
    if (keyboard.up) and not jumping and esta_sobre_plataforma(heroi, heroi_y_velocity) and not jumped:
        if sound_on:
            sounds.jump.play()
        jumping = True
        jumped = True
        clock.schedule_unique(jumpedrecently, 0.4)
        heroi.image = "jumper-up"
        heroi_y_velocity = 95
    if jumping:
        if heroi_y_velocity > 25:
            heroi_y_velocity = heroi_y_velocity - ((100 - heroi_y_velocity) / 2)
            heroi.y -= heroi_y_velocity / 3
        else:
            heroi_y_velocity = 0
            jumping = False
    if heroi.colliderect(gem):
        points += 1
        if sound_on:
            sounds.gem.play()
        gem.pos = random.choice([pos for pos in diamond_positions if pos != gem.pos])

def perder_vida():
    global vidas, game_state, points
    if sound_on:
        sounds.hit.play()
    vidas -= 1
    heroi.pos = (500, 250)
    heroi_y_velocity = 0
    jumping = False
    if vidas <= 0:
        game_state = MENU
        vidas = 3
        points = 0
        sounds.hero_music.stop()

def on_mouse_down(pos):
    global game_state, music_on, sound_on, points, vidas
    if game_state == MENU:
        if start_button.collidepoint(pos):
            game_state = PLAYING
            points = 0
            vidas = 3
            reset_inimigos()
            if music_on:
                sounds.hero_music.play(-1)
        elif sound_button.collidepoint(pos):
            sound_on = not sound_on
            music_on = not music_on
            if music_on:
                sounds.hero_music.play(-1)
            else:
                sounds.hero_music.stop()
        elif exit_button.collidepoint(pos):
            exit()

def reset_inimigos():
    global inimigo1, inimigo2
    inimigo1 = Inimigo()
    inimigo2 = Inimigo()

def jumpedrecently():
    global jumped
    jumped = False
