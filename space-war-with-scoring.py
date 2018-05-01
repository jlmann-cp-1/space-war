# Imports
import pygame
import random

# Initialize game engine
pygame.init()


# Window
WIDTH = 800
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)
TITLE = "Space War"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)


# Timer
clock = pygame.time.Clock()
refresh_rate = 60

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (100, 255, 100)

# Fonts
FONT_SM = pygame.font.Font(None, 24)
FONT_MD = pygame.font.Font(None, 32)
FONT_LG = pygame.font.Font(None, 64)
FONT_XL = pygame.font.Font("assets/fonts/spacerangerboldital.ttf", 96)

# Images
ship_img = pygame.image.load('assets/images/player.png')
laser_img = pygame.image.load('assets/images/laserRed.png')
mob_img = pygame.image.load('assets/images/enemyShip.png')
bomb_img = pygame.image.load('assets/images/laserGreen.png')

# Sounds
EXPLOSION = pygame.mixer.Sound('assets/sounds/explosion.ogg')

# Stages
START = 0
PLAYING = 1
CLEAR = 2
END = 3

# Game classes
class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.speed = 3
        self.shield = 5

    def move_left(self):
        self.rect.x -= self.speed
        
    def move_right(self):
        self.rect.x += self.speed

    def shoot(self):
        laser = Laser(laser_img)
        laser.rect.centerx = self.rect.centerx
        laser.rect.centery = self.rect.top
        lasers.add(laser)

    def update(self, bombs):
        hit_list = pygame.sprite.spritecollide(self, bombs, True)

        for hit in hit_list:
            # play hit sound
            self.shield -= 1

        hit_list = pygame.sprite.spritecollide(self, mobs, False)
        if len(hit_list) > 0:
            self.shield = 0

        if self.shield == 0:
            EXPLOSION.play()
            self.kill()
            
class Laser(pygame.sprite.Sprite):
    
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        
        self.speed = 5

    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 0:
            self.kill()
    
class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.value = 10

    def drop_bomb(self):
        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)
    
    def update(self, lasers, player):
        hit_list = pygame.sprite.spritecollide(self, lasers, True, pygame.sprite.collide_mask)

        if len(hit_list) > 0:
            EXPLOSION.play()
            player.score += self.value
            self.kill()


class Bomb(pygame.sprite.Sprite):
    
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
    
    
class Fleet:

    def __init__(self, mobs, level):
        self.mobs = mobs
        self.moving_right = True
        self.speed = 5
        self.bomb_rate = 60 - 2 * level

    def move(self):
        reverse = False
        
        for m in mobs:
            if self.moving_right:
                m.rect.x += self.speed
                if m.rect.right >= WIDTH:
                    reverse = True
            else:
                m.rect.x -= self.speed
                if m.rect.left <=0:
                    reverse = True

        if reverse == True:
            self.moving_right = not self.moving_right
            for m in mobs:
                m.rect.y += 32
            
    def choose_bomber(self):
        rand = random.randrange(0, self.bomb_rate)
        all_mobs = mobs.sprites()
        
        if len(all_mobs) > 0 and rand == 0:
            return random.choice(all_mobs)
        else:
            return None
    
    def update(self):
        self.move()

        bomber = self.choose_bomber()
        if bomber != None:
            bomber.drop_bomb()

# Game helper functions
def show_start_screen():
    title_text = FONT_XL.render("Space War!", 1, WHITE)
    start_text = FONT_SM.render("Press SPACE to start", 1, WHITE)
    
    title_text_rect = title_text.get_rect()
    title_text_rect.centerx = WIDTH / 2
    title_text_rect.bottom = HEIGHT / 2 - 16

    start_text_rect = start_text.get_rect()
    start_text_rect.centerx = WIDTH / 2
    start_text_rect.top = HEIGHT / 2
    
    screen.blit(title_text, title_text_rect)
    screen.blit(start_text, start_text_rect)

def show_stats(player, level):
    score_text = FONT_SM.render("Score: " + str(player.score), 1, WHITE)
    screen.blit(score_text, (32, 32))

    ship = player.sprite
    if ship != None:
        shield = ship.shield
    else:
        shield =0
        
    shield_text = FONT_SM.render("Shield: " + str(shield), 1, WHITE)
    screen.blit(shield_text, (32, 64))

    shield_text = FONT_SM.render("Level: " + str(level), 1, WHITE)
    screen.blit(shield_text, (32, 96))

def show_end_screen():
    title_text = FONT_LG.render("Game Over", 1, WHITE)
    start_text = FONT_SM.render("Press 'r' to play again", 1, WHITE)
    
    title_text_rect = title_text.get_rect()
    title_text_rect.centerx = WIDTH / 2
    title_text_rect.bottom = HEIGHT / 2 - 16

    start_text_rect = start_text.get_rect()
    start_text_rect.centerx = WIDTH / 2
    start_text_rect.top = HEIGHT / 2
    
    screen.blit(title_text, title_text_rect)
    screen.blit(start_text, start_text_rect)

def show_clear_screen(level):
    title_text = FONT_MD.render("Level " + str(level) + " complete!", 1, WHITE)
    start_text = FONT_SM.render("Press 'SPACE' to continue", 1, WHITE)
    
    title_text_rect = title_text.get_rect()
    title_text_rect.centerx = WIDTH / 2
    title_text_rect.bottom = HEIGHT / 2 - 16

    start_text_rect = start_text.get_rect()
    start_text_rect.centerx = WIDTH / 2
    start_text_rect.top = HEIGHT / 2
    
    screen.blit(title_text, title_text_rect)
    screen.blit(start_text, start_text_rect)
    d
def setup():
    global ship, player, stage, level
    
    ship = Ship(384, 536, ship_img)

    player = pygame.sprite.GroupSingle()
    player.add(ship)
    player.score = 0    
    
    stage = START
    level = 1

def start(level):
    global ship, mobs, fleet, lasers, bombs
    
    mob1 = Mob(128, 64, mob_img)
    mob2 = Mob(256, 64, mob_img)
    mob3 = Mob(384, 64, mob_img)

    mobs = pygame.sprite.Group()
    mobs.add(mob1, mob2, mob3)
    fleet = Fleet(mobs, level)
    
    lasers = pygame.sprite.Group()
    bombs = pygame.sprite.Group()

# Game loop
setup()
start(level)
    
done = False

while not done:
    # Event processing (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if stage == START:
                if event.key == pygame.K_SPACE:
                    stage = PLAYING
            elif stage == PLAYING:
                if event.key == pygame.K_SPACE:
                    ship.shoot()
            elif stage == END:
                if event.key == pygame.K_r:
                    setup()
                    start(level)

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_LEFT]:
        ship.move_left()
    elif pressed[pygame.K_RIGHT]:
        ship.move_right()
        
    
    # Game logic (Check for collisions, update points, etc.)
    if stage == PLAYING:
        player.update(bombs)
        lasers.update()   
        mobs.update(lasers, player)
        bombs.update()
        fleet.update()

        if len(player) == 0:
            stage = END
        elif len(mobs) == 0:
            level += 1
            start(level)
     
    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    screen.fill(BLACK)
        
    lasers.draw(screen)
    player.draw(screen)
    bombs.draw(screen)
    mobs.draw(screen)

    show_stats(player, level)
    
    if stage == START:
        show_start_screen()
    elif stage == END:
        show_end_screen()
    
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
