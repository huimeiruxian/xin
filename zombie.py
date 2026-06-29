import pygame
import random  # 记得导入 random

class Zombie(pygame.sprite.Sprite):
    def __init__(self):
        super(Zombie, self).__init__()
        self.image = pygame.image.load('material/images/Zombie_0.png').convert_alpha()
        self.images = [pygame.image.load('material/images/Zombie_{}.png'.format(i)).convert_alpha()for i in range(0, 22)]
        self.dieimages = [pygame.image.load('material/images/ZombieDie_{}.png'.format(i)).convert_alpha()for i in range(0, 10)]
        self.attack_images = [pygame.image.load('material/images/ZombieAttack_{}.png'.format(i)).convert_alpha()for i in range(0, 21)]
        self.rect = self.images[0].get_rect()
        # 优化：植物基准Y设为100，僵尸稍高一点设为60，这样它们的脚能完美对齐
        self.rect.top = 30 + random.randrange(0, 5) * 100
        self.energy=6
        self.rect.left = 1000
        self.speed = 5
        self.dietimes=0
        self.isMeetWallNut=False
        self.isAlive=True

    def update(self,*args):
        if self.energy>0:
            if self.isMeetWallNut:
                self.image=self.attack_images[args[0]%len(self.attack_images)]
            else:
                self.image = self.images[(args[0])%len(self.images)]
            if self.rect.left > -50 and not self.isMeetWallNut:
                self.rect.left -= self.speed
        else:
            if self.dietimes<20:
                self.image=self.dieimages[self.dietimes//2]
                self.dietimes+=1
            else:
                if self.dietimes>30:
                    self.isAlive=False
                    self.kill()
                else:
                    self.dietimes+=1