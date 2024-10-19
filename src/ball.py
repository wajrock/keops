import pygame
import random as rd

class Ball(pygame.sprite.Sprite):


    def __init__(self):
        super().__init__()
        self.anim = 0
        self.movement = 0
        self.ralenti = 0
        self.remise = 0
        self.ralenti_remise = 0
        self.ral = 0
        self.but_anim = 0
        self.hors_terrain = False
        self.rond_central = (1880, 998)
        self.pos = [1880, 998]
        self.taille = [20, 20]
        self.images = [pygame.transform.scale(pygame.image.load('./assets/football/ball.png').convert_alpha(), (self.taille[0], self.taille[1])),
                        pygame.transform.scale(pygame.image.load('./assets/football/ball2.png').convert_alpha(), (self.taille[0], self.taille[1])),
                        pygame.transform.scale(pygame.image.load('./assets/football/ball3.png').convert_alpha(), (self.taille[0], self.taille[1]))]
        self.image = self.images[self.anim%2]
        self.rect = self.image.get_rect()
        self.rect.center = (self.pos[0], self.pos[1])
        self.msg_rect = pygame.Rect(0,0,0,0)

        # MESSAGE
        self.FONT150 = pygame.font.Font('./assets/fonts/font_goal.ttf', 150)
        self.FONT55 = pygame.font.Font('./assets/fonts/Minecraft.ttf', 55)
        self.FONT40 = pygame.font.Font('./assets/fonts/Minecraft.ttf', 40)
        self.fond = pygame.transform.scale(pygame.image.load('./assets/football/fond_goal.png').convert_alpha(), (860*1.2, 241*1.1))
        self.fond_rect = self.fond.get_rect()
        self.fond_rect.center = (350, 350)
        self.fond.set_alpha(150)

        # SCORE
        self.score_bleu = 0
        self.score_rouge = 0
        self.score_rect = pygame.Rect(270, 4 ,160, 50)
        self.surf = pygame.Surface(self.score_rect.size, pygame.SRCALPHA)
        self.surf.set_alpha(160)

    def draw(self,window):
        window.blit(self.image,(self.rect.center))

    def update(self):
        self.rect.center = (self.pos[0], self.pos[1])

    def move(self, rect, hor, ver, bleu, rouge, terrain, screen):
        '''
        Gère le déplacement du ballon
        I: rect : pygame.Rect : player.rect
           hor : pygame.Rect : ligne hor du terrain
           ver : idem ver
           bleu : pygame.Rect : but bleu
           rouge : idem rouge
        O : None
        '''

        # SCORE
        self.draw_score(screen)

        self.old_position = self.pos
        # COLLISION JOUEUR
        if self.ralenti_remise > 0:
            self.pos[0] += self.direction[0]/4
            self.pos[1] += self.direction[1]/4
            self.ralenti_remise-= 1
            if self.ralenti_remise == 0:
                self.hors_terrain = False
        elif self.remise > 0:
            self.pos[0] += self.direction[0]
            self.pos[1] += self.direction[1]
            self.remise -= 1
            if self.remise == 0:
                self.ralenti_remise = 12
            
        elif self.rect.colliderect(rect): 
            # self.movement = rd.choice([i for i in range(25, 75)]+[40])
            self.movement = 40
            self.direction = [(self.rect.centerx - rect.centerx)/10, (self.rect.centery - rect.centery)/10]
        
        # MOUVEMENT 
        # si la balle bouge
        if self.movement > 0:
            self.anim += 0.15
            self.image = self.images[int(self.anim)%3]
            self.pos[0] += self.direction[0]
            self.pos[1] += self.direction[1]
            self.movement -= 1
            if self.movement == 0:
                self.ralenti = 30
                      
        # RALENTI / ELAN
        if self.ralenti > 0:
            self.anim += 0.08
            self.image = self.images[int(self.anim)%3]
            self.pos[0] += self.direction[0]/3
            self.pos[1] += self.direction[1]/3
            self.ralenti -= 1 

        # COLLISION LIGNES
        # maj pos
        self.rect.center = (self.pos[0], self.pos[1])
        if self.rect.collidelist(hor) > -1 and not self.hors_terrain:
            if rect.centery < self.rond_central[1] and rect.centery > self.rect.centery: # joueur en haut du terrain et en dessous de la balle
                self.direction[1] = -self.direction[1]
                self.pos = self.old_position
            elif rect.centery > self.rond_central[1] and rect.centery < self.rect.centery: # joueur en bas du terrain et au dessus de la balle
                self.direction[1] = -self.direction[1]
                self.pos = self.old_position
        if self.rect.collidelist(ver) > -1 and not self.hors_terrain:
            if rect.centerx < self.rond_central[0] and rect.centerx > self.rect.centerx: # joueur a gauche du terrain et a droite de la balle
                self.direction[0] = -self.direction[0]
                self.pos = self.old_position
            elif rect.centerx > self.rond_central[0] and rect.centerx < self.rect.centerx: # joueur a droite du terrain et a gauche de la balle
                self.direction[0] = -self.direction[0]
                self.pos = self.old_position

        
        # HORS TERRAIN
        if not self.rect.colliderect(terrain):
            self.movement, self.ralenti = 0, 0
            # BUT ?
            if self.rect.colliderect(rouge): 
                if not self.but_anim:
                    self.display_message('blue')
                    self.score_bleu+=1
                    self.but_anim=1
            elif self.rect.colliderect(bleu):
                if not self.but_anim:
                    self.display_message('red')
                    self.score_rouge+=1
                    self.but_anim=1
            else:
                # remise en jeu
                self.remise = 22
                self.direction = [(self.rond_central[0] - self.rect.centerx)/25, (self.rond_central[1] - self.rect.centery)/25]
                self.hors_terrain = True
                
        # ANIM BUT        
        if self.msg_rect.right > 0 and self.but_anim:
            self.draw_message(screen)
        elif self.but_anim: self.kickoff()

        
        # maj pos
        self.rect.center = (self.pos[0], self.pos[1])

    def kickoff(self):
        self.pos = [1880, 998]
        self.but_anim = 0
        self.movement, self.ralenti = 0, 0

    def display_message(self, msg):
        # pygame.draw.rect(self.surf, 'black', self.surf.get_rect())
        self.msg = self.FONT150.render('Goallllllllll ! ! ! !', True, msg)
        self.msg_rect = self.msg.get_rect()
        self.msg_rect.midleft = (700, 350)
    
    def draw_message(self, screen):
        # screen.blit(self.surf, self.fond)
        screen.blit(self.fond, self.fond_rect)
        screen.blit(self.msg, self.msg_rect)
        self.msg_rect.x -= 10

    def draw_score(self, screen):
        score= pygame.image.load("./assets/buttons/score.png").convert_alpha()
        score = pygame.transform.scale(score, (score.get_size()[0]/1.8, score.get_size()[1]/1.8))
        score_rect = score.get_rect()
        score_rect.center = (350, 95)
        score_n = self.FONT40.render(str(self.score_bleu)+'-'+str(self.score_rouge),True,'white')
        score_n_rect = score_n.get_rect()
        score_n_rect.center = (350, 100)
        screen.blit(score, score_rect)
        screen.blit(score_n, score_n_rect)


