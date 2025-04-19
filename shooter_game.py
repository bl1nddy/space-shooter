import pygame
import random

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("space.ogg")
pygame.mixer.music.play()

fire = pygame.mixer.Sound("fire.ogg")

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(player_image), (55, 55))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def __init__(self, player_x, player_y, player_speed):
        super().__init__('bullet.png', player_x, player_y, player_speed)

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:  
            self.kill()

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, 15)
        self.bullets_fired = 0
        self.reloading = False
        self.reload_time = 500
        self.last_shot_time = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

        if self.reloading:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time >= self.reload_time:
                self.reloading = False
                self.bullets_fired = 0 
    def fire(self):
        if not self.reloading:
            bullet = Bullet(self.rect.centerx, self.rect.top, 20)
            bullets.add(bullet)
            self.bullets_fired += 1
            fire.play()
            if self.bullets_fired >= 3:
                self.reloading = True
                self.last_shot_time = pygame.time.get_ticks()

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = random.randint(80, win_width - 80)
            self.rect.y = 0
            global lost
            lost += 1

class Asteroid(GameSprite):
    def __init__(self, player_x, player_y, player_speed):
        super().__init__('asteroid.png', player_x, player_y, player_speed)
    def update(self):
        self.rect.y += 2 * self.speed
        if self.rect.y > win_height:
            self.kill()

lost = 0
score = 0
goal = 10
max_lost = 10

win_height = 500
win_width = 700
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Shooter")
background = pygame.transform.scale(pygame.image.load("galaxy.jpg"), (win_width, win_height))

player = Player('rocket.png', 250, 445, 10)
sprites = pygame.sprite.Group()
players = pygame.sprite.Group()
players.add(player)

bullets = pygame.sprite.Group()


for i in range(1, 6):
    enemy = Enemy('ufo.png', random.randint(80, win_width - 80), -40, random.randint(3, 5))
    sprites.add(enemy)


for i in range(1, 3):
    asteroid = Asteroid(random.randint(0, win_width - 55), -40, random.randint(3, 5))
    sprites.add(asteroid)

pygame.font.init()
font = pygame.font.Font("PressStart2P-Regular.ttf", 14)

running = True
finish = False
clock = pygame.time.Clock()
FPS = 60

while running:  
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                player.fire()

    if not finish:
        window.blit(background, (0, 0))
        sprites.update()
        players.update()
        bullets.update() 
        
       
        collides = pygame.sprite.groupcollide(sprites, bullets, False, True)
        for enemy in collides:
            score += 1
            enemy.kill()  
            new_enemy = Enemy('ufo.png', random.randint(80, win_width - 80), -40, random.randint(3, 5))
            sprites.add(new_enemy)
            asteroid = Asteroid(random.randint(0, win_width - 55), -40, random.randint(3, 5))
            sprites.add(asteroid)

      
        if pygame.sprite.spritecollide(player, sprites, False):
            finish = True
            text_losecrash = font.render("Ты проиграл! Корабль столкнулся с врагом.", 1, (255, 0, 0))
            window.blit(text_losecrash, (50, 220))

        if lost >= max_lost:
            finish = True
            text_losesleep = font.render("Ты проиграл!", 1, (255, 0, 0))
            window.blit(text_losesleep, (50, 200))
            text_losesleep1 = font.render("Корабль пропустил слишком много врагов.", 1, (255, 0, 0))
            window.blit(text_losesleep1, (50, 225))
            text_losesleep2 = font.render("Ты не защитил космос.", 1, (255, 0, 0))
            window.blit(text_losesleep2, (120, 250))

        if score >= goal:
            finish = True
            text_win = font.render("ТЫ ВЫИГРАЛ! Ты сбил достаточно врагов.", 1, (76, 153, 0))
            window.blit(text_win, (50, 220))
            text_win2 = font.render("Космос гордится тобой!", 1, (76, 153, 0))
            window.blit(text_win2, (50, 250))

        text1 = font.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text1, (10, 40))
        text = font.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text, (10, 10))

        sprites.draw(window)  
        bullets.draw(window)
        players.draw(window)

        pygame.display.update() 
        clock.tick(FPS)  

pygame.quit()