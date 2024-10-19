import pygame

class PNJ(pygame.sprite.Sprite):


    def __init__(self, image, taille, pos):

        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('./assets/pnj/'+image+'.png').convert_alpha(), taille)
        self.rect = self.image.get_rect()
        self.rect.x = pos.x-self.rect.width/2
        self.rect.y = pos.y

    def draw(self,window):
        window.blit(self.image,(self.rect.topleft))