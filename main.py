import pygame
from maps import map1
FPS = 60
game = True
pygame.init()

win_size = (800 , 800) #40 пикселей клетка
window = pygame.display.set_mode(win_size)

class GameObject():
    def __init__(self , x ,y ,w ,h, image ) :
        self.rect = pygame.Rect(x,y,w,h)
        image = pygame.transform.scale(image ,(w,h))
        self.image = image

    def update(self):
        window.blit(self.image, (self.rect.x,self.rect.y))

wall_pict = pygame.image.load("wall.jpg")
tank_player_pict = pygame.image.load("tank.png")
fon1 = pygame.image.load("fon1.png")

class Player(GameObject):
    def __init__(self, x, y, w, h, image,speed):
        super().__init__(x, y, w, h, image)
        self.speed = speed
    def move(self, K_up,K_down,K_left,K_right):
        k = pygame.key.get_pressed()
        if k[K_up]:
            if self.rect.y >= 0:
                self.rect.y -= self.speed
            else:
                self.rect.y += self.speed
        if k[K_down]:
            if self.rect.y < 700:
                self.rect.y += self.speed
            else:
                self.rect.y -= self.speed
        if k[K_left]:
            self.rect.x -= self.speed
            
        if k[K_right]:
            self.rect.x += self.speed

def load_map(map):
    blocks = []
    fon = GameObject(0,0,800,800,fon1)
    blocks.append(fon)
    x = 0 
    y = 0
    for bl in map :
        global player1
        for l in bl:
            if l == "1":
                wall = GameObject(x,y,40,40,wall_pict)
                blocks.append(wall)
            if l == "5":
                player1 = Player(x,y,40,40,tank_player_pict,2)
                blocks.append(player1)
            x += 40
        y += 40
        x = 0       
    return blocks
map = load_map(map1)
clock = pygame.time.Clock()
while game :
    player1.move(pygame.K_w,pygame.K_s,pygame.K_a,pygame.K_d)
    for obj in map: 
        obj.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
    pygame.display.update()
    clock.tick(FPS)