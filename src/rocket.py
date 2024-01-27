import pygame

class Rocket(pygame.sprite.Sprite):


    def __init__(self, x, y):

        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('../assets/quetes/quete 5 - final/plane.png').convert_alpha(), (140,140))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
    def draw(self,window):
        window.blit(self.image,(self.rect.x-self.rect.width/2,self.rect.y-self.rect.height/2))
