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
GREEN = (0, 255, 0)

# Images
ship_img = pygame.image.load('assets/images/player.png')
bullet_img = pygame.image.load('assets/images/laserRed.png')
enemy_img = pygame.image.load('assets/images/enemyShip.png')
bomb_img = pygame.image.load('assets/images/laserGreen.png')
bg_img = pygame.image.load('assets/images/Background/starBackground.png')

# Sounds
LASER = pygame.mixer.Sound('assets/sounds/shoot.wav')
HIT = pygame.mixer.Sound('assets/sounds/hit.wav')
EXPLOSION = pygame.mixer.Sound('assets/sounds/explosion.ogg')
pygame.mixer.music.load('assets/sounds/drums_of_mordon.ogg')

# Fonts
font_sm = pygame.font.Font('assets/fonts/joystix_monospace.ttf', 16)
font_md = pygame.font.Font('assets/fonts/joystix_monospace.ttf', 32)
font_lg = pygame.font.Font('assets/fonts/joystix_monospace.ttf', 64)

# Stages
START = 0
PLAYING = 1
OVER = 2

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
        x = self.rect.centerx - bullet_img.get_rect().width / 2
        y = self.rect.top
        b = Bullet(x, y, bullet_img)
        bullets.add(b)
        LASER.play()

    def die(self):
        self.kill()
        EXPLOSION.play()

    def update(self, bombs, mobs):
        '''
        A ship dies when it's shield reaches zero. Getting hit by a mob will
        instantly kill a player. Getting hit by a bomb will reduce the shield
        by one.
        '''
        
        hit_list = pygame.sprite.spritecollide(self, mobs, False)
        
        if len(hit_list) > 0:
            self.shield = 0

        hit_list = pygame.sprite.spritecollide(self, bombs, True)
        
        for h in hit_list:
            HIT.play()
            self.shield -= 1

        if self.shield <= 0:
            self.die()
            
class Bullet(pygame.sprite.Sprite):
    
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        
        self.speed = 8

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

    def drop_bomb(self):
        x = self.rect.centerx - bullet_img.get_rect().width / 2
        y = self.rect.bottom
        b = Bomb(x, y, bomb_img)
        bombs.add(b)
    
    def update(self, bullets):
        hit_list = pygame.sprite.spritecollide(self, bullets, True, pygame.sprite.collide_mask)
        
        if len(hit_list) > 0:
            EXPLOSION.play()
            self.kill()

class Bomb(pygame.sprite.Sprite):
    
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.speed = 4

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()

class Fleet:

    def __init__(self, mobs):
        self.mobs = mobs
        self.moving_right = True
        self.speed = 5
        self.bomb_rate = 60

    def choose_bomber(self):
        rand = random.randrange(0, self.bomb_rate)
        all_mobs = mobs.sprites()

        if len(all_mobs) > 0 and rand == 0:
            return random.choice(all_mobs)
        else:
            return None

        reverse = False

    def move(self):
        reverse = False
        
        for m in mobs:
            if self.moving_right:
                m.rect.x += self.speed
                if m.rect.right > WIDTH:
                    reverse = True
            else:
                m.rect.x -= self.speed
                if m.rect.left < 0:
                    reverse = True

        if reverse:
            self.moving_right = not self.moving_right

            for m in mobs:
                m.rect.y += 32
                
    def update(self):
        #self.move()

        bomber = self.choose_bomber()
        if bomber != None:
            bomber.drop_bomb()

class Background(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
                
        self.w = image.get_rect().width
        self.h = image.get_rect().height

        self.image = pygame.Surface([WIDTH, HEIGHT + self.h])
        self.rect = self.image.get_rect()

        for x in range(0, self.rect.width, self.w):
            for y in range(-1 * self.h, self.rect.height, self.h):
                self.image.blit(bg_img, [x, y])
                
        self.rect.x = 0
        self.rect.y = -1 * self.h
        
    def update(self):
        self.rect.y += 1
        if self.rect.y == 0:
            self.rect.y = -1 * self.h
        
# Make game objects
x = WIDTH / 2 - ship_img.get_rect().width / 2
y = HEIGHT - 1.5 * ship_img.get_rect().height
ship = Ship(x, y, ship_img)

mob1 = Mob(128, 64, enemy_img)
mob2 = Mob(256, 64, enemy_img)
mob3 = Mob(384, 64, enemy_img)

# Add objects to sprite groups
player = pygame.sprite.GroupSingle()
player.add(ship)

mobs = pygame.sprite.Group()
mobs.add(mob1, mob2, mob3)

bullets = pygame.sprite.Group()
bombs = pygame.sprite.Group()

fleet = Fleet(mobs)

stars = Background(bg_img)
background = pygame.sprite.GroupSingle()
background.add(stars)

# Setup
stage = START
pygame.mixer.music.play(-1)

# Game loop
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

    if stage == PLAYING:
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_LEFT]:
            ship.move_left()
        elif pressed[pygame.K_RIGHT]:
            ship.move_right()
        
    # Game logic (Check for collisions, update points, etc.)
    background.update()
    
    if stage == PLAYING:
        bullets.update()
        bombs.update()
        fleet.update()
        mobs.update(bullets)
        player.update(bombs, mobs)
    
    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    background.draw(screen)
    bullets.draw(screen)
    bombs.draw(screen)
    player.draw(screen)
    mobs.draw(screen)

    if stage == START:
        title_text = font_lg.render("Space War!", True, WHITE)
        start_text = font_sm.render("Press SPACE to start", True, WHITE)
        screen.blit(title_text, [145, 200])
        screen.blit(start_text, [250, 310])
        
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()

    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
