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

def load_map(map):
    blocks = []
    x = 0 
    y = 0
    for bl in map :
        for l in bl:
            if l == "1":
                wall = GameObject(x,y,40,40,wall_pict)
                blocks.append(wall)
            x += 40
        y += 40
        x = 0       
    return blocks
map = load_map(map1)
clock = pygame.time.Clock()
while game :
    for obj in map: 
        obj.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
    pygame.display.update()
    clock.tick(FPS)