import pygame

class Sunflower(pygame.sprite.Sprite):
    def __init__(self):
        super(Sunflower, self).__init__()
        self.image = pygame.image.load('material/images/sunflower_00.png').convert_alpha()
        self.images = [pygame.image.load('material/images/sunflower_{:02d}.png'.format(i)).convert_alpha()for i in range(0, 13)]
        
        self.rect = self.image.get_rect()
        self.rect.top = 150
        self.rect.left = 250

    def update(self,*args):
        self.image = self.images[(args[0])%len(self.images)]