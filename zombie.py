import pygame

class Zombie(pygame.sprite.Sprite):
    def __init__(self):
        super(Zombie, self).__init__()
        self.image = pygame.image.load('material/images/Zombie_0.png').convert_alpha()
        self.images = [pygame.image.load('material/images/Zombie_{}.png'.format(i)).convert_alpha()for i in range(0, 22)]
        
        self.rect = self.image.get_rect()
        self.rect.top = 50
        self.rect.left = 1000
        self.speed = 5

    def update(self,*args):
        self.image = self.images[(args[0])%len(self.images)]
        if self.rect.left > 250:
         self.rect.left -= self.speed