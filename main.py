import pygame
from maps import map1
FPS = 60
game = True
pygame.init()

win_size = (800, 800)
window = pygame.display.set_mode(win_size)

class GameObject():
    def __init__(self, x, y, w, h, image):
        self.rect = pygame.Rect(x, y, w, h)
        image = pygame.transform.scale(image, (w, h))
        self.image = image

    def update(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

wall_pict = pygame.image.load("wall.jpg")
tank_player_pict = pygame.image.load("tank.png")
fon1 = pygame.image.load("fon1.png")
bullet_pict = pygame.image.load("bullet.png")
expl_pict1 = pygame.image.load("explosion_picts/explosion1.png")
expl_pict2 = pygame.image.load("explosion_picts/explosion2.png")
expl_pict3 = pygame.image.load("explosion_picts/explosion3.png")
expl_pict4 = pygame.image.load("explosion_picts/explosion4.png")
expl_pict5 = pygame.image.load("explosion_picts/explosion5.png")
expl_pict6 = pygame.image.load("explosion_picts/explosion6.png")
expl_pict7 = pygame.image.load("explosion_picts/explosion7.png")
expl_list = [expl_pict1 , expl_pict2 , expl_pict3 , expl_pict4,expl_pict5,expl_pict6,expl_pict7]
class Bullet(GameObject):
    def __init__(self, x, y, w, h, image, speed, direction=0):
        super().__init__(x, y, w, h, image)
        self.speed = speed
        self.direction = direction

    def move(self):
        if self.direction == 0:
            self.rect.y -= self.speed
        if self.direction == 1:
            self.rect.x += self.speed
        if self.direction == 2:
            self.rect.y += self.speed
        if self.direction == 3:
            self.rect.x -= self.speed

bullets = []

class Explosion(GameObject):
    def __init__(self,x,y,w,h,image):
        super().__init__(x,y,w,h,image)
        self.timer = 0
        self.queue = 1
    def anim_explosion(self):
        if self.timer >= 5:
            self.image = expl_list[self.queue]
            self.queue += 1
            self.timer = 0
        self.timer +=1
explosions = []

class Player(GameObject):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image)
        self.direction = 0
        self.speed = speed
        self.cooldown = 0
        self.img_up = self.image
        self.img_down = pygame.transform.rotate(self.image, 180)
        self.img_right = pygame.transform.rotate(self.image, -90)
        self.img_left = pygame.transform.rotate(self.image, 90)

    def move(self, K_up, K_down, K_left, K_right, walls):
        k = pygame.key.get_pressed()
        if k[K_up]:
            self.direction = 0
            self.image = self.img_up
            new_rect = self.rect.move(0, -self.speed)
            if new_rect.y >= 0 and not any(new_rect.colliderect(w.rect) for w in walls):
                self.rect = new_rect

        if k[K_down]:
            self.direction = 2
            self.image = self.img_down
            new_rect = self.rect.move(0, self.speed)
            if new_rect.y < win_size[1] and not any(new_rect.colliderect(w.rect) for w in walls):
                self.rect = new_rect

        if k[K_left]:
            self.direction = 3
            self.image = self.img_left
            new_rect = self.rect.move(-self.speed, 0)
            if new_rect.x >= 0 and not any(new_rect.colliderect(w.rect) for w in walls):
                self.rect = new_rect

        if k[K_right]:
            self.direction = 1
            self.image = self.img_right
            new_rect = self.rect.move(self.speed, 0)
            if new_rect.x < win_size[0] and not any(new_rect.colliderect(w.rect) for w in walls):
                self.rect = new_rect

    def shoot(self):
        self.cooldown -= 1
        if pygame.mouse.get_pressed()[0] and self.cooldown <= 0:
            self.cooldown = 50
            bullet = Bullet(self.rect.x + self.rect.w / 3, self.rect.y + self.rect.h / 3, 10, 10, bullet_pict, 5, self.direction)
            bullets.append(bullet)

def load_map(map_data):
    blocks = []
    walls = []
    fon = GameObject(0, 0, 800, 800, fon1)
    blocks.append(fon)
    x = 0
    y = 0
    for bl in map_data:
        global player1
        for l in bl:
            if l == "1":
                wall = GameObject(x, y, 40, 40, wall_pict)
                blocks.append(wall)
                walls.append(wall)
            if l == "5":
                player1 = Player(x, y, 40, 40,tank_player_pict, 2)
                blocks.append(player1)
            x += 40
        y += 40
        x = 0
    return blocks, walls

map_data = load_map(map1)
map_blocks, walls = map_data
clock = pygame.time.Clock()

while game:
    player1.move(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, walls)
    player1.shoot()

    for obj in map_blocks:
        obj.update()

    for bullet in bullets[:]:
        bullet.move()
        bullet.update()
        if any(bullet.rect.colliderect(wall.rect) for wall in walls):
            explosion = Explosion(bullet.rect.x , bullet.rect.y , 35 , 35 , expl_pict1)
            explosions.append(explosion)
            bullets.remove(bullet)
    for explosion in explosions:
        if explosion.queue < 7 :
            explosion.update()
            explosion.anim_explosion()
        # else:
        #     explosions.remove(explosion)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
            
    pygame.display.update()
    clock.tick(FPS)
