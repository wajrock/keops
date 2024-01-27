import pygame

# FLOU
from PIL import Image, ImageFilter

import time
from pygame import mixer
import numpy

from player import Player
from map import Map
from ball import Ball
from pnj import PNJ

class Game:

    def __init__(self):

        # INITIALISATION FENETRE
        self.screen = pygame.display.set_mode((700,700))
        pygame.display.set_caption('KEOPS - Escape Game')
        self.icon = pygame.image.load('../assets/others/icone.png')
        pygame.display.set_icon(self.icon)

        # CHARGEMENT
        self.c = False
    
        # FONDS ECRAN
        self.background = pygame.image.load("../assets/backgrounds/background.png").convert()
        self.background_succes = pygame.image.load("../assets/backgrounds/success_background.png").convert()
        self.background_options = pygame.image.load("../assets/backgrounds/options.png").convert()
        self.carte = pygame.image.load("../assets/gps/map.png").convert()
        self.carte = pygame.transform.scale(self.carte, (self.carte.get_size()[0]/2, self.carte.get_size()[1]/2))
        self.carte_rect = self.carte.get_rect()
        self.carte_mid = (self.carte.get_size()[0]/2, self.carte.get_size()[1]/2)
        self.coord_player = [0,0]
        self.pin = pygame.image.load("../assets/gps/pin.png").convert_alpha()
        self.pin = pygame.transform.scale(self.pin, (self.pin.get_size()[0]/10, self.pin.get_size()[1]/10))
        self.pin_rect = self.pin.get_rect()
        self.pin_pos = [1600, 0]
        self.pin_rect.topleft = self.pin_pos 
        self.trajet = False

        # TRAJET
        self.montre = pygame.image.load("../assets/gps/phone.png").convert_alpha()
        self.montre = pygame.transform.scale(self.montre, (self.montre.get_size()[0]/3, self.montre.get_size()[1]/3))
        self.montre_rect = self.montre.get_rect()
        self.montre_rect.bottomleft = (10, 625)
        self.fleche = pygame.transform.scale(pygame.image.load('../assets/gps/green_arrow.png').convert_alpha(), (60,60))
        self.fleche_rect = self.fleche.get_rect()  
        self.angle = 90  
        self.anim_montre = False

        #AFFICHAGE BULLE TEXTE
        self.bubble = pygame.image.load("../assets/texts/dialog.png")
        self.indic = pygame.image.load("../assets/texts/dialog1.png")

        #INITIALISATION COULEURS BOUTTONS
        self.color_play_button,self.color_options_button,self.color_quit_button,self.color_pause_play_button,self.color_pause_options_button,self.color_pause_quit_button,self.color_succes_button = 7*[(255, 255, 255)]
        
        #COULEURS ITEMS
        self.jouer_color, self.options_color, self.quit_color, self.difficulte_color, self.touches_color, self.retour_color, self.facile_color, self.normal_color, self.difficile_color, self.lettres_color, self.fleches_color,self.succes_color = 12*[(46, 204, 113)]
        
        #MILIEU ECRAN
        mid = self.screen.get_size()[0]/2-90 

        self.position_touches = self.screen.get_size()[0]/2+95
        self.position_back = self.screen.get_size()[0]/2+95+95

        # CREATION BOUTON MENU PAUSE
        self.play_pause_button = pygame.Rect(mid-20, 400, 220 , 60)
        self.options_pause_button = pygame.Rect(mid-20, 480, 220 , 60)
        self.quit_pause_button = pygame.Rect(mid-20, 560, 220 , 60)

        self.succes_rect = pygame.Rect(mid, 400, 180 , 60)

        # ALL BUTTON
        self.hover = {'play': '','options': '','quit': '','level': '','touches': '','back': '','facile': '','moyen': '','difficile': '','letters': '','arrow': '','time': '', 'pause': ''}

        self.color_time = 'white'

        #DIFFICULTES & OPTIONS MENU
        self.difficile_rect = pygame.Rect(0, 0, 0, 0)
        self.difficulte_buttons = False
        self.touches_buttons = False
        self.active_difficulte = 1
        self.active_touches = 0

        self.radius_circle = 0

        # LISTES TOUCHES DE DEPLACEMENT
        self.TD = [[pygame.K_q,pygame.K_d,pygame.K_z,pygame.K_s], [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]]

        # INITIALISATION VARIABLES JEU
        self.level = [1000, 700, 500]
        self.timer = self.level[self.active_difficulte]
        self.count_jump = 0

        # JOUEUR
        self.transparence_player = 255
        self.deplacement = (0,0)
        self.animation = 0
        
        #indexs affichage texts
        self.index_welcome, self.index_sage,self.index_code_sage, self.index_pirate,self.index_renard,self.index_renard1,self.index_yoda,self.index_yoda1,self.index_final = 9*[0]

        #QUETE SAGE
        self.input_sage = ''
        self.have_code_sage = False
        self.parchment_open = False

        #QUETE PIRATE
        self.input_bateau  = ''
        self.indice_pirate = False

        #QUETE RENARD
        self.indice_renard_1 = False
        self.indice_renard_2 = False
        self.have_banana = False
        self.give_banana = False

        #QUETE YODA
        self.indice_yoda_1 = False
        self.indice_yoda_2 = False
        self.have_potion = False
        self.give_potion = False

        #QUETE FINAL
        self.quizz = False
        self.quizz_reponse = 10*[False]
        self.input_final = ''
        
        # TEXTE MENU PAUSE
        self.pause_rect = pygame.Rect(580, 6, 101 , 30)
        self.pause_text = (self.font_render('Minecraft',30)).render('PAUSE',True,'white')

        #LISTE TOUCHE CODE SECRET
        self.keys_final = [pygame.K_0,pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9]

        # MOUSE
        self.cursor = [pygame.transform.scale(pygame.image.load('../assets/others/cursor1.png').convert_alpha(), (10,10)), 
                       pygame.transform.scale(pygame.image.load('../assets/others/cursor2.png').convert_alpha(), (10,10))]
        self.cursor_rect = self.cursor[0].get_rect()

        self.parchment_open = False

        #VERIFIE SI LA TOUCHE SPACE EST LIBRE
        self.space_released = True

        self.teleportation = True

        self.talk = False

    
    def charge(self):
        '''
        Charge le jeu
        '''
        # INITIALISATION JOUEUR
        self.player = Player()
        self.camera = pygame.Rect(1472,2000,1,1)
        
        # INITIALISATION VELO
        self.velos = []
        for i in range(12):
            self.velos.append(PNJ('velo', (20,16), self.player.dict_map['map'].get_object_by_name("spawn_velo"+str(i))))
        self.num_velo = -1
        
        # INITIALISATION FOOT
        self.ball = Ball()

        # INITIALISATION AFFICHAGE MAP
        self.map =Map(self.player, 'map', '', '', self.player.dict_map['map'], self.velos)
        self.anim_trappe = False
        self.anim_cave = False
        self.map.place()
        self.player.new_world('map')
        self.numero = '' # numero de maison

        #MESSAGE BIENVENU
        self.first = ['[ESPACE] : Message suivant','[ECHAP] : Mettre en Pause','[M] : Couper le son','[N] : Activer le son','[E] : Afficher la Map','[H] : Afficher un indice',' Bienvenu Piwi !..','Tu es dans le Village de Keops..', 'Tu as ete enleve..', "Ton objectif est de t'echapper..", 'Pour cela il te faudra..','resoudre differentes quetes..', 'Dechiffre le code secret..', 'Prends le vaisseau et.. ','A toi la liberte !','']
        self.first_renders = [(self.font_render('REDENSEK',40)).render(text, True, (0, 0, 0)) for text in self.first]

    def jump(self):
        """
        Gestion des sauts du joueur.
        """
        if self.count_jump == 0:
            self.camera.y = self.player.rect.y
        self.camera.x = self.player.rect.x
        self.count_jump += 1

        if self.player.jump[1] == 'r':
            self.player.move_right()
            if self.count_jump%2==0:
                self.player.move_right()
            if self.map.name == "boat" and not(300 < self.player.rect.y < 370):
                self.player.move_right()
        if self.player.jump[1] == 'l':
            self.player.move_left()
            if self.count_jump%2==0:
                self.player.move_left()
            if self.map.name == "boat" and not(300 < self.player.rect.y < 370):
                self.player.move_left()
        if self.player.jump[1] == 'u':
            self.camera.y -= self.player.speed
            self.player.move_up()
            if self.map.name == "boat" and not(300 < self.player.rect.y < 370):
                self.camera.y -= self.player.speed
                self.player.move_up()
        if self.player.jump[1] == 'd':
            self.camera.y += self.player.speed
            self.player.move_down()
            if self.map.name == "boat" and not (300 < self.player.rect.y < 370):
                self.camera.y += self.player.speed
                self.player.move_down()

        if self.count_jump <= 10:
            self.player.move_up()
            self.player.move_up()
        elif self.count_jump <= 20:
            self.player.move_down()
            self.player.move_down()
        else:
            self.player.jump[0] = False
            self.count_jump = 0

    def move(self, pressed):
        """
        Gestion mouvements du joueur
        """
        self.camera = pygame.Rect(self.player.rect.x, self.player.rect.y, self.player.rect.width, self.player.rect.height)
        if pressed[self.TD[self.active_touches][0]]:
            self.player.move_left()
            self.hor += 1
            self.press = True
            self.dir = 'l'
        if pressed[self.TD[self.active_touches][1]]:
            self.player.move_right()
            self.hor += 1
            self.press = True
            self.dir = 'r'
        if pressed[self.TD[self.active_touches][2]]:
            self.player.move_up()
            self.ver += 1
            self.press = True
            self.dir = 'u'
        if pressed[self.TD[self.active_touches][3]]:
            self.player.move_down()
            self.ver += 1
            self.press = True
            self.dir = 'd'

    def handle_input(self):
        """
        Initialise les données du jeu, Gère les actions clavier
        """
        self.press = False
        self.ver = 0
        self.hor = 0
        self.dir = ''
        pressed = pygame.key.get_pressed()

        # TIMER
        self.timer += self.go_timer-time.time()
        self.go_timer = time.time()

        if self.player.jump[0]:
            self.jump()

        # on bouge pas si il y a une animation
        elif self.radius_circle <= 0 and not self.anim_cave and not self.anim_trappe:
            self.move(pressed)

        if not self.press : self.player.move = 2

        # si on  gauche + droite seulement
        if self.hor > 1 and self.ver == 0:
            # joueur immobile (image 'stand')
            self.player.move = 2

        # si on a heut + bas seulement 
        if self.ver  > 1 and self.hor == 0:
            self.player.move = 2
        
        # si le player va dans une seule direction cette direction sinon non
        if (self.ver+self.hor)!=1:
            self.dir=''
        
        self.player.animation(self.dir)          

    def carte_handle_input(self, pressed):
        """
        Gère l'Affichage de la carte
        """
        if pressed[self.TD[self.active_touches][0]]:
            if self.carte_rect.x < 0:
                self.carte_rect.x += 2
                self.carte_pos(True)
        if pressed[self.TD[self.active_touches][1]]:
            if self.carte_rect.x > 700-self.carte_rect.w:
                self.carte_rect.x -= 2
                self.carte_pos(True)
        if pressed[self.TD[self.active_touches][2]]:
            if self.carte_rect.y < 0:
                self.carte_rect.y += 2
                self.carte_pos(True)
        if pressed[self.TD[self.active_touches][3]]:
            if self.carte_rect.y+self.carte_rect.h > 700:
                self.carte_rect.y -= 2
                self.carte_pos(True)  

    def change_mode_player(self, change):
        if self.map.name == 'map':
            n = self.player.rect.collidelist(self.velos)  

            if n > -1 and self.player.mode != 'velo':   # si collision
                self.num_velo = n
                self.screen.blit(self.indic,(self.screen.get_size()[0]/2-(self.indic.get_size()[0])/2,500))
                self.display_message('REDENSEK','[A] pour monter a velo', 30, self.screen.get_size()[0]/2, 555, 'white')

                if change:

                    if self.player.mode == 'velo':
                        pos = self.player.change_mode(True, change)
                        self.velos[self.num_velo].rect.center = pos
                    else:
                        self.player.change_mode(True, change)
                        self.velos[self.num_velo].rect.x = -4000

                else:
                    self.player.change_mode(False, change)

            elif change and self.player.mode == 'velo':
                pos = self.player.change_mode(False, change)
                self.velos[self.num_velo ].rect.center = pos

            elif self.player.mode == 'velo':
                pos = self.player.change_mode(False, change)
                if self.player.mode != 'velo':
                    self.velos[self.num_velo].rect.center = pos
                    self.num_velo = -1

            else:
                self.player.change_mode(False, change)

    def transition(self):
        # animation
        if self.animation == 1:
            if self.radius_circle < 500:
                self.radius_circle += 20  
            else:
                self.animation = 0
        elif self.animation == -1:
            if self.radius_circle > 0:
                self.radius_circle -= 20
            else: 
                self.animation = 0

    def update(self):
        self.map.group.update()    

        # animation
        self.transition()    
        
        # GENRAL SWITCH
        if self.map.switch_test()[0]:
            # carte
            if self.map.name == 'map':
                self.coord_player = [self.player.rect.center[0]/2, self.player.rect.center[1]/2]
            # velo
            if self.player.mode == 'velo':
                self.velos[self.num_velo].rect.center = self.player.rect.center
            porte = self.map.switch_test()[1]
            where = self.map.spawn_name(porte)
            # numero de maison
            self.numero = self.map.switch_test()[2]
            # Trappe
            if where == 'trappe' and not self.anim_trappe:
                self.anim_trappe = True
                self.map = Map(self.player, where, porte, '', self.player.dict_map[where], [])
                self.player.new_world(self.map.name)
                
                self.trappe_pos = self.map.tmx_data.get_object_by_name("spawn_pyr_trappe")
                self.deplacement = (self.trappe_pos.x - self.player.rect.x, self.trappe_pos.y - self.player.rect.y)
            ##
            else:
                self.animation = 1
                self.transition()
                if self.animation == 0:
                    self.map = Map(self.player, where, porte, self.numero, self.player.dict_map[where], self.velos)
                    self.map.place()
                    self.player.new_world(self.map.name)
                    self.animation = -1
                    self.player.update()
                    self.camera = pygame.Rect(self.player.rect.x, self.player.rect.y, self.player.rect.width, self.player.rect.height)
                                       
        # Trappe to cave
        if self.anim_cave:    
            if self.player.position[1] < self.map.player_position.y:
                self.player.position[1] += 2
            else:
                self.player.new_world('cave')
                
                self.anim_cave = False
        
        # TRAPPE SWITCH
        if self.anim_trappe:
            if self.transparence_player > 30:
                self.transparence_player -= 2
                self.player.position[0] += (1/113)*self.deplacement[0]
                self.player.position[1] += (1/113)*self.deplacement[1]
                self.player.image.set_alpha(self.transparence_player)
                self.player.update()
            else:
                self.map = Map(self.player, 'cave', 'trappe_cave', '',  self.player.dict_map['cave'], [])
                self.map.place()
                self.transparence_player = 255
                self.player.image.set_alpha(self.transparence_player)
                self.player.position[1]-=100
                self.player.update()
                self.anim_trappe = False
                self.anim_cave = True
        
        # TROU
        if self.map.name == 'trou' and self.player.feet.colliderect(self.player.ordi):
            self.player.dict_map['trou']=self.player.dict_map.pop('trou2')
            self.map = Map(self.player, 'trou', 'trou2', '',  self.player.dict_map['trou'], [])
            
            self.player.new_world(self.map.name)
            
    def font_render(self,font,size):
        font_render = pygame.font.Font('../assets/fonts/'+font+'.ttf',size)
        return font_render      

    def display_message(self,font,text,font_size,x,y,color):
        img = self.font_render(font,font_size).render(text,True,color)
        display_rect = img.get_rect()
        display_rect.center = (x,y)
        self.screen.blit(img, display_rect)

        return display_rect

    def print_button(self, button):
        '''
        Affiche le bouton
        '''
        # TAILLE
        if button in ['play', 'options', 'quit']: taille = 1.5
        else: taille = 1.8
        # BOUTON AVEC 2EME IMG
        if button not in ['level', 'touches']:
            im = pygame.image.load("../assets/buttons/"+button+"_button"+self.hover[button]+".png")
        else:
            im = pygame.image.load("../assets/buttons/"+button+"_button.png")
        im = pygame.transform.scale(im, (im.get_size()[0]/taille, im.get_size()[1]/taille))
        rect = im.get_rect()
        # COORD
        x = 0
        y = 0
        # NIVEAU
        if button == 'facile': x = -200
        elif button == 'difficile': x = 200 
        # TOUCHES
        elif button == 'touches' or button == 'letters' or button == 'arrow': y = 95
        if button == 'back' : y = 190
        elif button == 'letters' : x = -120
        elif button == 'arrow': x = 120
        # MENU
        elif button == 'play': y+=50
        elif button == 'options': y+=50+95
        elif button == 'quit': y+=50+95+95

        rect.center = (self.screen.get_size()[0]/2+x,self.screen.get_size()[0]/2+y)
        self.screen.blit(im, rect)

        return rect

    def print_image(self,path,x,y):
        img = pygame.image.load(path)
        img_rect= img.get_rect()
        img_rect.center = (x,y)
        self.screen.blit(img, img_rect)
    
    def init_menu(self, pause):
        # BACKGROUND
        if pause:
            self.screen.blit(self.screenshot, (0,0))
            self.print_image("../assets/texts/logo_keops.png",self.screen.get_size()[0]/2,200)
        else:
            self.screen.blit(self.background, (0,0))
        # BUTTON
        self.play_button = self.print_button('play')
        self.options_button = self.print_button('options')
        self.quit_button = self.print_button('quit')

    def init_succes(self, hover):
        # BACKGROUND
        self.screen.blit(self.background_succes, (0,0))
        # BUTTON
        if hover:
            self.quit_button = self.draw_button(self.succes_rect,self.color_succes_button,'../assets/buttons/quit_button1.png')
        else:
            self.quit_button = self.draw_button(self.succes_rect,self.color_succes_button,'../assets/buttons/quit_button.png')

    def init_intro(self,time):
        fade_time = 0.5
        type_fade = lambda x: x  # Linear

        logo = pygame.image.load('../assets/texts/logo.png')
        logo_size = logo.get_rect(center=(700 / 2, 700 / 2))
        
        time -= fade_time   
                
        alpha = type_fade(1.0 * time / fade_time)

        surface_logo = pygame.surface.Surface((logo_size.width, logo_size.height))
        surface_logo.set_alpha(255 * alpha)

        if int(alpha) == 1 and not self.c:
            self.charge()
            self.c = True

        self.screen.fill((0, 0, 0))
        surface_logo.blit(logo, (0, 0))
        self.screen.blit(surface_logo, logo_size)

    def init_options(self):
        # BACKGROUND
        self.screen.blit(self.background_options, (0,0))
        
        # NIVEAU
        if not self.hover['level']:
            self.lev_button = self.print_button('level')
        else:
            self.easy_button = self.print_button('facile')
            self.moy_button = self.print_button('moyen')
            self.diff_button = self.print_button('difficile')
            self.levels_rect = pygame.Rect(self.easy_button.x, self.easy_button.y, self.diff_button.x+self.diff_button.w-self.easy_button.x, self.easy_button.h)
        # TOUCHES
        if not self.hover['touches']:
            self.touches_button = self.print_button('touches')
        else:
            self.letters_button = self.print_button('letters')
            self.arrow_button = self.print_button('arrow')
            self.touches_rect = pygame.Rect(self.letters_button.x, self.letters_button.y, self.arrow_button.x+self.arrow_button.w-self.letters_button.x, self.letters_button.h)
        # RETOUR
        self.back_button = self.print_button('back')

    def init_data(self, hover):
        '''
        Init bouton time et pause ds le jeu
        '''
        # PAUSE
        self.pause = pygame.image.load("../assets/buttons/pause"+hover['pause']+".png")
        self.pause = pygame.transform.scale(self.pause, (self.pause.get_size()[0]/3, self.pause.get_size()[1]/3))
        self.pause_button = self.pause.get_rect()
        self.pause_button.center = (630,30)
        # TIME 
        self.time = pygame.image.load("../assets/buttons/time"+hover['time']+".png")
        self.time = pygame.transform.scale(self.time, (self.time.get_size()[0]/3, self.time.get_size()[1]/3))
        self.time_button = self.time.get_rect()
        self.time_button.center = (90,30)

        self.time_large = pygame.image.load("../assets/buttons/time_big.png")
        self.time_large = pygame.transform.scale(self.time_large, (self.time_large.get_size()[0]/2, self.time_large.get_size()[1]/2))
        self.time_large_button = self.time_large.get_rect()
        self.time_large_button.center = (self.screen.get_size()[0]/2,130)

    def draw(self,m):
        hover = self.hover.copy()

        if int(self.timer) < 120:
            self.time_color = 'red'
            
        if self.pause_button.collidepoint(m):
            self.hover['pause'] = '1'
        elif self.hover['pause'] == '1':
            self.hover['pause'] = ''
        
        if self.time_button.collidepoint(m):
            self.color_time = (85,48,6)
            self.hover['time'] = '1'
            self.screen.blit(self.time_large,self.time_large_button)
            self.screen.blit((self.font_render('Minecraft',30)).render(str(int(self.timer))+'s',True,'white'), (315, 120))
        elif self.hover['time'] == '1':
            self.color_time = 'white'
            self.hover['time'] = ''
            
        if self.hover != hover:
            self.init_data(self.hover)

        self.screen.blit(self.pause,self.pause_button)
        self.screen.blit(self.time,self.time_button)
        self.screen.blit((self.font_render('Minecraft',15)).render(str(int(self.timer))+'s',True,self.color_time), (110, 24))
        # CIRCLE ANIM
        if self.radius_circle > 0:
            pygame.draw.circle(self.screen, (0,0,0), (self.screen.get_size()[0]/2, self.screen.get_size()[0]/2), self.radius_circle)        

    def draw_button(self,o,n,p):
        o = pygame.image.load(p)
        o = pygame.transform.scale(o, (o.get_size()[0]/1.5, o.get_size()[1]/1.5))
        n = o.get_rect()
        n.center = (self.screen.get_size()[0]/2,400)
        self.screen.blit(o,n)
        return n
        
    def hover_menu(self,page_menu,mouse,pause):
        hover = self.hover.copy()
        
        if page_menu == 'options':
            # LEVEL_liste                
            if self.hover['level'] == '1':
                if self.easy_button.collidepoint(mouse) or self.active_difficulte == 0:
                    self.hover['facile'] = '1'
                elif self.hover['facile'] == '1' and not self.active_difficulte == 0:
                    self.hover['facile'] = ''
                if self.moy_button.collidepoint(mouse) or self.active_difficulte == 1:
                    self.hover['moyen'] = '1'
                elif self.hover['moyen'] == '1' and not self.active_difficulte == 1:
                    self.hover['moyen'] = ''
                if self.diff_button.collidepoint(mouse) or self.active_difficulte == 2:
                    self.hover['difficile'] = '1'
                elif self.hover['difficile'] == '1' and not self.active_difficulte == 2:
                    self.hover['difficile'] = ''
            # LEVEL
            if self.lev_button.collidepoint(mouse):
                self.hover['level'] = '1'
            elif self.hover['level'] and not self.levels_rect.collidepoint(mouse):
                self.hover['level'] = ''

            # TOUCHES liste                  
            if self.hover['touches'] == '1':
                if self.letters_button.collidepoint(mouse) or self.active_touches == 0:
                    self.hover['letters'] = '1'
                elif self.hover['letters'] == '1' and not self.active_touches == 0:
                    self.hover['letters'] = ''
                if self.arrow_button.collidepoint(mouse) or self.active_touches == 1:
                    self.hover['arrow'] = '1'
                elif self.hover['arrow'] == '1' and not self.active_touches == 1:
                    self.hover['arrow'] = ''
            # TOUCHES
            if self.touches_button.collidepoint(mouse):
                self.hover['touches'] = '1'
            elif self.hover['touches'] == '1' and not self.touches_rect.collidepoint(mouse):
                self.hover['touches'] = ''

            # RETOUR
            if self.back_button.collidepoint(mouse):
                self.hover['back'] = '1'
            else:
                self.hover['back'] = ''
    
        if page_menu == 'menu':  
            #PLAY
            if self.play_button.collidepoint(mouse):
                self.hover['play'] = '1'
            else:
                self.hover['play'] = ''
            # OPTIONS
            if self.options_button.collidepoint(mouse):
                self.hover['options'] = '1'
            else:
                self.hover['options'] = ''
            # RETOUR
            if self.quit_button.collidepoint(mouse):
                self.hover['quit'] = '1'
            else:
                self.hover['quit'] = ''

        if list(self.hover.values())[:3] != list(hover.values())[:3]:
            self.init_menu(pause)
        elif self.hover != hover:
            self.init_options()

    def hover_succes(self,mouse):
        if self.quit_button.collidepoint(mouse):
            self.hover['quit'] = '1'
            self.init_succes(True)
        elif self.hover['quit'] == '1':
            self.init_succes(False)
            
    def message(self,pressed):
        
        if (self.index_welcome+1) != len(self.first_renders):
            self.screen.blit(self.bubble,(self.screen.get_size()[0]/2-(self.bubble.get_size()[0])/2,500))
            self.screen.blit(self.first_renders[self.index_welcome], (self.screen.get_size()[0]/2-(self.first_renders[self.index_welcome].get_size()[0])/2,535))

            if pressed[pygame.K_SPACE]  and self.space_released:
                self.space_released = False
                self.index_welcome = (self.index_welcome + 1) if (self.index_welcome) != len(self.first_renders) else 0
                if self.index_welcome != 0:
                    self.screen.blit(self.first_renders[self.index_welcome], (self.screen.get_size()[0]/2-(self.first_renders[self.index_welcome].get_size()[0])/2,540))

            elif not pressed[pygame.K_SPACE]:
                self.space_released = True

        #MESSAGE FIN DE JEU CODDE LIBERATION
        self.text_s = ['Entrez le code secret...',self.input_final]
        self.text_sortie = [(self.font_render('REDENSEK',40)).render(text, True, (0, 0, 0)) for text in self.text_s]
        
        if self.player.feet.colliderect(self.map.ROCKET.rect):
            self.screen.blit(self.bubble,(self.screen.get_size()[0]/2-(self.bubble.get_size()[0])/2,500))
            self.screen.blit(self.text_sortie[self.index_final], (self.screen.get_size()[0]/2-(self.text_sortie[self.index_final].get_size()[0])/2,535))
            
            if pressed[pygame.K_SPACE] and self.space_released:
                self.index_final = 1
                self.screen.blit(self.text_sortie[self.index_final], (self.screen.get_size()[0]/2-(self.text_sortie[self.index_final].get_size()[0])/2,540))
            elif not pressed[pygame.K_SPACE]:
                self.space_released = True

    def quete_sage(self):
        pressed = pygame.key.get_pressed()

        #MESSAGE PREMIERE QUETE
        self.text = ['Bonjour cher inconnu !', 'Un vieux proverbe egyptien', 'nous dit que la cle de tous','les secrets se trouve dans','la premiere merveille du monde', "revenez me voir avec l'indice",'']
        self.text_renders = [(self.font_render('REDENSEK',40)).render(text, True, (0, 0, 0)) for text in self.text]

        self.text_d = ['Entrez le code secret...',self.input_sage,'Allez voir le pirate sur son bateau']
        self.text_debut = [(self.font_render('REDENSEK',40)).render(text, True, (0, 0, 0)) for text in self.text_d]

        if not self.parchment_open:
            #MESSAGE VIEUX SAGE SANS CODE
            if (self.index_sage+1) != len(self.text_renders):
                    
                self.screen.blit(self.bubble,(self.screen.get_size()[0]/2-(self.bubble.get_size()[0])/2,500))
                if pressed[pygame.K_SPACE] and self.space_released:
                    self.space_released = False
                    self.index_sage += 1
                elif not pressed[pygame.K_SPACE]:
                    self.space_released = True
                self.screen.blit(self.text_renders[self.index_sage], (self.screen.get_size()[0]/2-(self.text_renders[self.index_sage].get_size()[0])/2,535))
            else:
                self.index_sage = 0
        else:
            #MESSAGE VIEUX SAGE AVEC CODE                
            self.screen.blit(self.bubble,(self.screen.get_size()[0]/2-(self.bubble.get_size()[0])/2,500))
            if pressed[pygame.K_SPACE] and self.space_released:
                self.space_released = False
                self.index_code_sage = 1
            elif not pressed[pygame.K_SPACE]:
                self.space_released = True
            
            if "PIVERT" in self.input_sage.upper() and self.space_released:
                self.index_code_sage = 2
            
            self.screen.blit(self.text_debut[self.index_code_sage], (self.screen.get_size()[0]/2-(self.text_debut[self.index_code_sage].get_size()[0])/2,535))

    def quete_pirate(self,collid):
        pressed = pygame.key.get_pressed()

        self.pirate_m = ['Repondez à cette question :', 'Sur quel port, la pyramide de', 'KEOPS garde un oeil ?',self.input_bateau]
        self.pirate_message = [(self.font_render('REDENSEK',40)).render(text, True, (0, 0, 0)) for text in self.pirate_m]

        if pressed[pygame.K_h]:
            self.print_image("../assets/quetes/quete 2 - bateau/help.png",self.screen.get_size()[0]/2,self.screen.get_size()[0]/2)
        if collid:
            if not self.indice_pirate:
                self.screen.blit(self.bubble,(self.screen.get_size()[0]/2-(self.bubble.get_size()[0])/2,500))
                self.screen.blit(self.pirate_message[self.index_pirate], (self.screen.get_size()[0]/2-(self.pirate_message[self.index_pirate].get_size()[0])/2,535))
                if pressed[pygame.K_SPACE] and self.space_released and self.index_pirate < 3:
                    self.space_released = False
                    self.index_pirate = self.index_pirate + 1
                    if self.index_pirate != 0:
                        self.screen.blit(self.pirate_message[self.index_pirate], (self.screen.get_size()[0]/2-(self.pirate_message[self.index_pirate].get_size()[0])/2,540))
                elif not pressed[pygame.K_SPACE]:
                    self.space_released = True
                        
                if self.input_bateau.upper() in ["ALEXANDRIE", "Alexandrie","alexandrie"] and self.space_released:
                    self.screen.blit(self.indic,(self.screen.get_size()[0]/2-(self.indic.get_size()[0])/2,500))
                    self.display_message('REDENSEK','[V] pour afficher le parchemin', 30, self.screen.get_size()[0]/2, 555, 'white')
        if pressed[pygame.K_v]:
            self.indice_pirate = True

        #AFFICHE SOLUTION SI COLLISION ET INDICE TRUE
        if collid and self.indice_pirate:
            self.print_image("../assets/quetes/quete 2 - bateau/indice_pirate.png",self.screen.get_size()[0]/2,self.screen.get_size()[0]/2)

    def grab(self,pressed,element):
        if element == 'banana':
            if pressed[pygame.K_p] and not self.have_banana:
                self.have_banana = True
                self.map.group.remove(self.map.BANANA)
            
            return self.have_banana
        
        if element == 'potion':
            if pressed[pygame.K_p] and not self.have_potion:
                self.have_potion = True
                self.map.group.remove(self.map.POTION)
            
            return self.have_potion
    
    def quete_renard(self):
        pressed = pygame.key.get_pressed()

        #SI LE JOUEUR N'A PAS LES BANANES
        if not self.grab(pressed,'banana'):
            self.renard_m = ["IAZJDDOPFDS?", "HSQOIJFOVOND", "AZEPKODNFKIPDS","OPSDNVJKLBKAZNZ",""]
            self.renard_message = [(self.font_render('REDENSEK',40)).render(text, True, (0, 0, 0)) for text in self.renard_m]

            if (self.index_renard+1) != len(self.renard_message) and not self.indice_renard_1:
                    self.screen.blit(self.bubble,(self.screen.get_size()[0]/2-(self.bubble.get_size()[0])/2,500))
                    self.screen.blit(self.renard_message[self.index_renard], (self.screen.get_size()[0]/2-(self.renard_message[self.index_renard].get_size()[0])/2,535))
                    if pressed[pygame.K_SPACE] and self.space_released:
                        self.space_released = False
                        self.index_renard = (self.index_renard + 1) if (self.index_renard + 1) != len(self.renard_message) else 0
                        if self.index_renard != 0:
                            self.screen.blit(self.renard_message[self.index_renard], (self.screen.get_size()[0]/2-(self.renard_message[self.index_renard].get_size()[0])/2,535))

                    elif not pressed[pygame.K_SPACE]:
                        self.space_released = True
            else:
                self.indice_renard_1 = True
            
            if not self.grab(pressed,'banana') and self.indice_renard_1:
                self.print_image("../assets/quetes/quete 3 - renard/translate.png",self.screen.get_size()[0]/2,self.screen.get_size()[0]/2)

        #SI LE JOUEUR A LES BANANES
        if self.grab(pressed,'banana') and not self.indice_renard_2:
            self.renard_m2 = ["Merci beacoup mon ami !","Tu as mérité que je t'aide",""]
            self.renard_message2 = [(self.font_render('REDENSEK',40)).render(text, True, (0, 0, 0)) for text in self.renard_m2]

            self.screen.blit(self.indic,(self.screen.get_size()[0]/2-(self.indic.get_size()[0])/2,500))
            self.display_message('REDENSEK','[V] pour donner les bananes', 30, self.screen.get_size()[0]/2, 555, 'white')
            if pressed[pygame.K_v]:
                self.index_renard = 0
                self.give_banana = True
            
            if self.give_banana:
                if (self.index_renard+1) != len(self.renard_message2):
                        
                    self.screen.blit(self.bubble,(self.screen.get_size()[0]/2-(self.bubble.get_size()[0])/2,500))
                    self.screen.blit(self.renard_message2[self.index_renard], (self.screen.get_size()[0]/2-(self.renard_message2[self.index_renard].get_size()[0])/2,535))
                    if pressed[pygame.K_SPACE] and self.space_released:
                        self.space_released = False
                        self.index_renard = (self.index_renard + 1) if (self.index_renard + 1) != len(self.renard_message2) else 0
                        if self.index_renard != 0:
                            self.screen.blit(self.renard_message2[self.index_renard], (self.screen.get_size()[0]/2-(self.renard_message2[self.index_renard].get_size()[0])/2,535))

                    elif not pressed[pygame.K_SPACE]:
                        self.space_released = True
                else:
                    self.indice_renard_2 = True

        #AFFICHE LA SOLUTION QUAND LE RENARD A FINIT DE PARLER
        if self.indice_renard_2 and self.grsab(pressed,'banana'):
                self.index_seconde_quete = 0
                self.print_image("../assets/quetes/quete 3 - renard/indice_banana.png",self.screen.get_size()[0]/2,self.screen.get_size()[0]/2)
      
    def quete_yoda(self):
        pressed = pygame.key.get_pressed()
        if not self.grab(pressed,'potion'):
            self.wizard_m = ["D'une traduction besoin tu as ?", "1000 langues traduire je peux", "des animaux aussi","du Renard la langue besoin","vous semblez avoir. Une potion de","traduction pour cela il me faut","à la maison du pecheur", "trouverez vous la...",'']
            self.wizard_message = [(self.font_render('REDENSEK',40)).render(text, True, (0, 0, 0)) for text in self.wizard_m]
            if (self.index_yoda+1) != len(self.wizard_message) and not self.indice_yoda_1:
                        
                    self.screen.blit(self.bubble,(self.screen.get_size()[0]/2-(self.bubble.get_size()[0])/2,500))
                    self.screen.blit(self.wizard_message[self.index_yoda], (self.screen.get_size()[0]/2-(self.wizard_message[self.index_yoda].get_size()[0])/2,535))
                    if pressed[pygame.K_SPACE] and self.space_released:
                        self.space_released = False
                        self.index_yoda = (self.index_yoda + 1) if (self.index_yoda + 1) != len(self.wizard_message) else 0
                        if self.index_yoda != 0:
                            self.screen.blit(self.wizard_message[self.index_yoda], (self.screen.get_size()[0]/2-(self.wizard_message[self.index_yoda].get_size()[0])/2,535))

                    elif not pressed[pygame.K_SPACE]:
                        self.space_released = True
            else:
                self.index_yoda = 0
            

        if self.grab(pressed,'potion') and not self.indice_yoda_1:
            self.wizard_m2 = ["Merci beacoup mon ami !","Voici le message du renard :",""]
            self.wizard_message2 = [(self.font_render('REDENSEK',40)).render(text, True, (0, 0, 0)) for text in self.wizard_m2]

            self.screen.blit(self.indic,(self.screen.get_size()[0]/2-(self.indic.get_size()[0])/2,500))
            self.display_message('REDENSEK','[V] pour donner la potion', 30, self.screen.get_size()[0]/2, 555, 'white')
            if pressed[pygame.K_v]:
                self.index_yoda = 0
                self.give_potion = True
            
            if self.give_potion:
                if (self.index_yoda+1) != len(self.wizard_message2):
                        
                    self.screen.blit(self.bubble,(self.screen.get_size()[0]/2-(self.bubble.get_size()[0])/2,500))
                    self.screen.blit(self.wizard_message2[self.index_yoda], (self.screen.get_size()[0]/2-(self.wizard_message2[self.index_yoda].get_size()[0])/2,535))
                    if pressed[pygame.K_SPACE] and self.space_released:
                        self.space_released = False
                        self.index_yoda = (self.index_yoda + 1) if (self.index_yoda + 1) != len(self.wizard_message2) else 0
                        if self.index_yoda != 0:
                            self.screen.blit(self.wizard_message2[self.index_yoda], (self.screen.get_size()[0]/2-(self.wizard_message2[self.index_yoda].get_size()[0])/2,535))

                    elif not pressed[pygame.K_SPACE]:
                        self.space_released = True
                else:
                    self.indice_yoda_1 = True

        if self.indice_yoda_1 and self.grab(pressed,'potion'):
                self.print_image("../assets/quetes/quete 4 - yoda/indice_wizard.png",self.screen.get_size()[0]/2,self.screen.get_size()[0]/2)

    def final_quete(self):
            pressed = pygame.key.get_pressed()
        
            self.final_m = ["Bonjour, repondez à ce quizz", "de 10 questions pour","obtenir le code final",'']
            self.final_message = [(self.font_render('REDENSEK',40)).render(text, True, (0, 0, 0)) for text in self.final_m]

            
            if not self.quizz and (self.quizz_reponse == 10*[False]):
                if (self.index_final+1) != len(self.final_message):
                            self.screen.blit(self.bubble,(self.screen.get_size()[0]/2-(self.bubble.get_size()[0])/2,500))
                            self.screen.blit(self.final_message[self.index_final], (self.screen.get_size()[0]/2-(self.final_message[self.index_final].get_size()[0])/2,535))
                            if pressed[pygame.K_SPACE] and self.space_released:
                                self.space_released = False
                                self.index_final = (self.index_final + 1) if (self.index_final + 1) != len(self.final_message) else 0
                                if self.index_final != 0:
                                    self.screen.blit(self.final_message[self.index_final], (self.screen.get_size()[0]/2-(self.final_message[self.index_final].get_size()[0])/2,535))

                            elif not pressed[pygame.K_SPACE]:
                                self.space_released = True
                else:
                    self.screen.blit(self.indic,(self.screen.get_size()[0]/2-(self.indic.get_size()[0])/2,500))
                    self.display_message('REDENSEK','[C] POUR COMMENCER', 30, self.screen.get_size()[0]/2, 555, 'white')
                    
            if pressed[pygame.K_c]:
                self.quizz = True
            
            if self.quizz:
                #QUESTION 1
                if not self.quizz_reponse[0]:
                    self.print_image("../assets/quetes/quete 5 - final/quizz/1.png",self.screen.get_size()[0]/2,self.screen.get_size()[0]/2)

                    if pressed[pygame.K_2]:
                        self.quizz_reponse[0] = True

                #QUESTION 2
                if (not self.quizz_reponse[1]) and (self.quizz_reponse[0]):
                    self.print_image("../assets/quetes/quete 5 - final/quizz/2.png",self.screen.get_size()[0]/2,self.screen.get_size()[0]/2)

                    if pressed[pygame.K_2]:
                        self.quizz_reponse[1] = True

                #QUESTION 3
                if (not self.quizz_reponse[2]) and (self.quizz_reponse[1]):
                    self.print_image("../assets/quetes/quete 5 - final/quizz/3.png",self.screen.get_size()[0]/2,self.screen.get_size()[0]/2)

                    if pressed[pygame.K_3]:
                        self.quizz_reponse[2] = True
                
                #QUESTION 4
                if (not self.quizz_reponse[3]) and (self.quizz_reponse[2]):
                    self.print_image("../assets/quetes/quete 5 - final/quizz/4.png",self.screen.get_size()[0]/2,self.screen.get_size()[0]/2)

                    if pressed[pygame.K_2]:
                        self.quizz_reponse[3] = True
                
                #QUESTION 5
                if (not self.quizz_reponse[4]) and (self.quizz_reponse[3]):
                    self.print_image("../assets/quetes/quete 5 - final/quizz/5.png",self.screen.get_size()[0]/2,self.screen.get_size()[0]/2)

                    if pressed[pygame.K_3]:
                        self.quizz_reponse[4] = True

                #QUESTION 6
                if (not self.quizz_reponse[5]) and (self.quizz_reponse[4]):
                    self.print_image("../assets/quetes/quete 5 - final/quizz/6.png",self.screen.get_size()[0]/2,self.screen.get_size()[0]/2)

                    if pressed[pygame.K_2]:
                        self.quizz_reponse[5] = True

                #QUESTION 7
                if (not self.quizz_reponse[6]) and (self.quizz_reponse[5]):
                    self.print_image("../assets/quetes/quete 5 - final/quizz/7.png",self.screen.get_size()[0]/2,self.screen.get_size()[0]/2)

                    if pressed[pygame.K_1]:
                        self.quizz_reponse[6] = True

                #QUESTION 8
                if (not self.quizz_reponse[7]) and (self.quizz_reponse[6]):
                    self.print_image("../assets/quetes/quete 5 - final/quizz/8.png",self.screen.get_size()[0]/2,self.screen.get_size()[0]/2)

                    if pressed[pygame.K_1]:
                        self.quizz_reponse[7] = True
                
                #QUESTION 9
                if (not self.quizz_reponse[8]) and (self.quizz_reponse[7]):
                    self.print_image("../assets/quetes/quete 5 - final/quizz/9.png",self.screen.get_size()[0]/2,self.screen.get_size()[0]/2)

                    if pressed[pygame.K_2]:
                        self.quizz_reponse[8] = True
                
                #QUESTION 10
                if (not self.quizz_reponse[9]) and (self.quizz_reponse[8]):
                    self.print_image("../assets/quetes/quete 5 - final/quizz/10.png",self.screen.get_size()[0]/2,self.screen.get_size()[0]/2)

                    if pressed[pygame.K_2]:
                        self.quizz_reponse[9] = True
                        self.quizz = False
                        self.index_final = 0
                
            if self.quizz_reponse == 10*[True] and not self.quizz:
                self.final_s = ["Félicitations, un vrai génie !", "Le code secret est ton", "code actuel auquel tu enlèves","le nombre d'étoiles sur le drapeau", "des USA !",'']
                self.final_success = [(self.font_render('REDENSEK',40)).render(text, True, (0, 0, 0)) for text in self.final_s]

                if (self.index_final+1) != len(self.final_success):
                    self.screen.blit(self.bubble,(self.screen.get_size()[0]/2-(self.bubble.get_size()[0])/2,500))
                    self.screen.blit(self.final_success[self.index_final], (self.screen.get_size()[0]/2-(self.final_success[self.index_final].get_size()[0])/2,535))
                    if pressed[pygame.K_SPACE] and self.space_released:
                        self.space_released = False
                        self.index_final = (self.index_final + 1) if (self.index_final + 1) != len(self.final_success) else 0
                        if self.index_final != 0:
                            self.screen.blit(self.final_success[self.index_final], (self.screen.get_size()[0]/2-(self.final_success[self.index_final].get_size()[0])/2,535))

                    elif not pressed[pygame.K_SPACE]:
                        self.space_released = True
                else:
                    self.index_final = 0
            
    def gestion_quete(self,pressed):
        if self.map.name == "map":
            self.message(pressed)
            if self.player.feet.colliderect(self.map.PNJ.rect):
                self.quete_sage()
            elif self.player.feet.colliderect(self.map.MONK.rect):
                self.quete_renard()

            elif self.player.feet.colliderect(self.map.WIZARD.rect):
                self.quete_yoda()

            elif self.player.feet.colliderect(self.map.PNJ2.rect):
                self.final_quete()
            else: 
                self.teleportation = True
                
        elif self.map.name == "inboat":
            if self.player.feet.colliderect(self.map.PIRATE.rect):
                self.collid =True
                self.quete_pirate(self.collid)
            else: 
                self.teleportation = True
                   
        elif self.map.name == 'farmetage':
            if self.player.feet.colliderect(self.map.BANANA) and not self.have_banana:
                self.screen.blit(self.indic,(self.screen.get_size()[0]/2-(self.indic.get_size()[0])/2,500))
                self.display_message('REDENSEK','[P] pour prendre les bananes', 30, self.screen.get_size()[0]/2, 555, 'white')
                self.grab(pressed,'banana')
            else: 
                self.teleportation = True

        elif self.map.name == 'loti':
            if self.player.feet.colliderect(self.map.POTION) and not self.have_potion:
                self.screen.blit(self.indic,(self.screen.get_size()[0]/2-(self.indic.get_size()[0])/2,500))
                self.display_message('REDENSEK','[P] pour prendre la potion', 30, self.screen.get_size()[0]/2, 555, 'white')
                self.grab(pressed,'potion')
            else: 
                self.teleportation = True
                
        elif self.map.name == 'housecave':
            # self.have_code_sage = True ##################################################################################################
            # if 5<=self.player.feet.x<20 and 129<self.player.feet.y<=138 and not self.parchment_open: ################# coord!!!! ####
            #     self.screen.blit(self.indic,(self.screen.get_size()[0]/2-(self.indic.get_size()[0])/2,500))
            #     self.display_message('REDENSEK','[V] pour afficher le parchemin', 30, self.screen.get_size()[0]/2, 555, 'white')
                    
            # if pressed[pygame.K_v] :
            #     self.parchment_open = True

            # if 5<=self.player.feet.x<20 and 129<self.player.feet.y<=138 and self.parchment_open :    
            #     self.print_image("../assets/quetes/quete 1 - sage/table.png",self.screen.get_size()[0]/2,self.screen.get_size()[0]/2)
                
            if self.player.feet.colliderect(self.map.PARCHEMIN.rect) :
                if not self.parchment_open: 
                    self.screen.blit(self.indic,(self.screen.get_size()[0]/2-(self.indic.get_size()[0])/2,500))
                    self.display_message('REDENSEK','[V] pour afficher le parchemin', 30, self.screen.get_size()[0]/2, 555, 'white')
                    if pressed[pygame.K_v] :
                        self.parchment_open = True
                else:
                    self.print_image("../assets/quetes/quete 1 - sage/table.png",self.screen.get_size()[0]/2,self.screen.get_size()[0]/2)
            else: 
                self.teleportation = True

    def take_screenshot(self):
        pygame.image.save(self.screen,"../assets/backgrounds/screenshot.png")
        OriImage = Image.open('../assets/backgrounds/screenshot.png')
        self.screenshot = OriImage.filter(ImageFilter.GaussianBlur(radius=10))
        self.screenshot.save("../assets/backgrounds/screenshot.png")
        self.screenshot = pygame.image.load("../assets/backgrounds/screenshot.png")

    def carte_pos(self, pause):
        '''
        Renvoie les coordonnées de la carte
        O: (x,y)
        '''    
        if self.map.name == 'map':
            # COORD PLAYER
            coord = self.player.rect.center[0]/2, self.player.rect.center[1]/2
        else:
            coord = self.coord_player
        # POS PLAYER CARTE
        rect = pygame.Rect(self.player.rect.x, self.player.rect.y, self.player.rect.w, self.player.rect.h)
        rect.midbottom = coord
        self.carte.blit(self.player.down_images[2], rect)
        #carte 
        if not pause:
            # RECHARGE MAP
            self.carte = pygame.image.load("../assets/gps/map.png").convert()
            self.carte = pygame.transform.scale(self.carte, (self.carte.get_size()[0]/2, self.carte.get_size()[1]/2))
            self.carte_rect.center = (self.screen.get_size()[0]/2, self.screen.get_size()[0]/2)
            self.carte_rect.x += self.carte_mid[0]-coord[0]
            self.carte_rect.y += self.carte_mid[1]-coord[1]
            self.carte_rect.x = max(min((1504/2),self.carte_rect.center[0]), -(1504/2)+700) - (1504/2)
            self.carte_rect.y = max(min((1064/2),self.carte_rect.center[1]), -(1064/2)+700) - (1064/2)
            self.carte.blit(self.player.down_images[2], rect)
            
        self.screen.blit(self.carte, self.carte_rect)
        #rect
        self.keops_carte = pygame.image.load("../assets/buttons/keops_map.png").convert_alpha()
        self.keops_carte = pygame.transform.scale(self.keops_carte, (self.keops_carte.get_size()[0]/2, self.keops_carte.get_size()[1]/2))
        self.keops_carte_rect = self.keops_carte.get_rect()
        self.keops_carte_rect.center = (self.screen.get_size()[0]/2, 50)
        self.screen.blit(self.keops_carte,self.keops_carte_rect)
        #self.display_message('CARTE', 40, self.screen.get_size()[0]/2, 25, 'white')
        #pin
        if self.pin_pos[0] < 1600:
            self.trajet = True
            self.montre = pygame.image.load("../assets/gps/phone.png").convert_alpha()
            self.montre = pygame.transform.scale(self.montre, (self.montre.get_size()[0]/3, self.montre.get_size()[1]/3))
            self.montre_rect.bottomleft = (10, 690)
        self.pin_rect.midbottom = (self.pin_pos[0]+self.carte_rect.x, self.pin_pos[1]+self.carte_rect.y)
        self.screen.blit(self.pin, self.pin_rect)

    def gps(self):
        self.fleche_rect.center = self.montre_rect.center
        self.fleche_rect.y -= 12
        x = self.pin_pos[0]-self.player.rect.x/2
        y = self.pin_pos[1]-self.player.rect.y/2
        if x>0 and y<0:
            self.angle = numpy.degrees(numpy.arccos(x/numpy.sqrt(x**2+y**2)))
        elif x<0 and y<0:
            self.angle = 270 - numpy.degrees(numpy.arccos(y/numpy.sqrt(x**2+y**2)))
        elif x<0 and y>0:
            self.angle = -numpy.degrees(numpy.arccos(x/numpy.sqrt(x**2+y**2)))
        elif x>0 and y>0:
            self.angle = 270 + numpy.degrees(numpy.arccos(y/numpy.sqrt(x**2+y**2)))
        self.active_fleche = pygame.transform.rotate(self.fleche, self.angle)
        # DISTANCE
        d = int(numpy.sqrt(x**2+y**2)/5)
        if d < 2:
            self.montre = pygame.image.load("../assets/gps/phone_end.png").convert_alpha()
            self.montre = pygame.transform.scale(self.montre, (self.montre.get_size()[0]/3, self.montre.get_size()[1]/3))
            self.screen.blit(self.montre, self.montre_rect)
            self.anim_montre = True
            self.chrono = time.time()
            self.trajet = False
            self.pin_pos = [1600, 0]
        else:
            # AFFICHAGE
            rect = self.active_fleche.get_rect(center = self.fleche_rect.center)
            self.screen.blit(self.montre, self.montre_rect)
            self.screen.blit(self.active_fleche, rect)
            self.display_message('Minecraft','distance : ', 15, self.montre.get_size()[0]/2+10, 645, 'black')
            self.display_message('Minecraft',str(d)+' m', 20, self.montre.get_size()[0]/2+10, 665, (46, 204, 113))

    def run(self):
        clock = pygame.time.Clock()

        running = True
        chargement = True
        menu = False
        pause = False
        succes = False
        carte = False
        page_menu = 'menu'
        jeu = False
        
        mixer.music.load('../assets/audio/audio2.mp3')
        mixer.music.play(-1)
        mixer.music.set_volume(0.3)
        mixer.music.pause()
        
        debut = time.time()
        
        while running:
            
            while chargement:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        debut = 10000000000000
                        running = False

                state_time = time.time() - debut
                self.init_intro(state_time)
                
                if time.time()-debut > 2:
                    chargement = False
                    menu = True
                    self.init_menu(pause)

                pygame.display.flip()    
                clock.tick(120)
           
            while menu: 
                mixer.music.unpause()
                mouse = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        menu = False
                        running = False
                    
                    if page_menu == 'menu':
                        # QUITTER
                        if self.quit_button.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN:
                                menu = False
                                running = False
                        # JOUEUR
                        elif (self.play_button.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN) or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                            menu = False
                            self.timer = self.level[self.active_difficulte]
                            self.go_timer = time.time() # à deplacer en f° du scenar/ à mettre à la fin du tuto !!!!!!!!!!!!!!!!!!!!!!
                            jeu = True
                            self.init_data(self.hover)
                        # OPTIONS
                        elif self.options_button.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN:                                
                                page_menu = 'options'
                                self.init_options()

                    elif page_menu == 'options':   
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            # LEVEL Liste
                            if self.hover['level'] == '1':
                                if self.easy_button.collidepoint(mouse):
                                    self.active_difficulte = 0
                                if self.moy_button.collidepoint(mouse):
                                    self.active_difficulte = 1
                                if self.diff_button.collidepoint(mouse):
                                    self.active_difficulte = 2
                            # TOUCHES Liste
                            if self.hover['touches'] == '1':
                                if self.letters_button.collidepoint(mouse):
                                        self.active_touches = 0
                                if self.arrow_button.collidepoint(mouse):
                                        self.active_touches = 1
                            # RETOUR
                            if self.back_button.collidepoint(mouse):                                
                                page_menu = 'menu'
                                self.init_menu(pause)
                                
                self.hover_menu(page_menu,mouse, pause)
                pygame.display.flip()     
                clock.tick(120)
                
            while pause:

                mouse = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pause = False
                        running = False
                        # voulez vraiment quitter
                    
                    if page_menu == 'menu':
                        # QUITTER
                        if self.quit_button.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN:
                                pause = False
                                running = False
                        # JOUER
                        elif (self.play_button.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                            pause = False
                            self.timer -= self.go_timer-time.time()
                            jeu = True
                            self.init_data(self.hover)
                        # OPTIONS
                        elif self.options_button.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN:                                
                            page_menu = 'options'
                            self.init_options()

                    elif page_menu == 'options' and event.type == pygame.MOUSEBUTTONDOWN:
                        # LEVEL Liste
                        if self.hover['level'] == '1':
                            if self.easy_button.collidepoint(mouse):
                                self.timer -= self.level[self.active_difficulte]
                                self.active_difficulte = 0
                                self.timer += self.level[self.active_difficulte]
                            if self.moy_button.collidepoint(mouse):
                                self.timer -= self.level[self.active_difficulte]
                                self.active_difficulte = 1
                                self.timer += self.level[self.active_difficulte]
                            if self.diff_button.collidepoint(mouse):
                                self.timer -= self.level[self.active_difficulte]
                                self.active_difficulte = 2
                                self.timer += self.level[self.active_difficulte]
                        # TOUCHES Liste
                        if self.hover['touches'] == '1':
                            if self.letters_button.collidepoint(mouse):
                                    self.active_touches = 0
                            if self.arrow_button.collidepoint(mouse):
                                    self.active_touches = 1
                        # RETOUR
                        if self.hover['back'] == '1':                                
                                page_menu = 'menu'
                                self.init_menu(pause)
                
                self.hover_menu(page_menu, mouse, pause)
                pygame.display.flip()     
                clock.tick(120)       
            
            while succes:
                
                mouse = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (self.quit_button.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN):
                        succes = False
                        running = False
                                
                self.hover_succes(mouse)

                pygame.display.flip()   
                clock.tick(120)  

            while carte:

                pressed = pygame.key.get_pressed()
                self.carte_handle_input(pressed)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        carte = False
                        running = False   
                    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse = pygame.mouse.get_pos()
                        self.pin_pos = [mouse[0]-self.carte_rect.x, mouse[1]-self.carte_rect.y]
                        self.carte_pos(True)

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_e and self.teleportation:
                            self.timer -= self.go_timer-time.time()
                            jeu = True
                            self.init_data(self.hover)
                            carte = False

                pygame.display.flip()  
                clock.tick(120)

            while jeu:

                pressed = pygame.key.get_pressed()
                mouse = pygame.mouse.get_pos()

                self.handle_input()
                self.update()
                self.map.group.center(self.camera.center)
                self.map.group.draw(self.screen)

                # AFFICHAGE STADE
                if self.player.rect.colliderect(self.player.stade):
                    s = self.player
                    self.map.BALL.move(s.body, s.lignes_terrain_hor,s.lignes_terrain_ver, s.but_bleu, s.but_rouge, s.terrain, self.screen)
                self.draw(mouse)

                # GESTION MUSIC
                if pressed[pygame.K_m]:
                    mixer.music.pause()
                elif pressed[pygame.K_n]:
                    mixer.music.unpause()
                
                self.gestion_quete(pressed)

                #CONDITION FIN DE JEU
                if self.input_final == "231":
                    if self.radius_circle < 500:
                        self.animation = 1
                        self.transition()
                    else:
                        succes = True
                        self.init_succes(False)
                        jeu = False

                #VELO
                a = False

                # TELEPHONE TRAJET
                if self.trajet:
                    self.gps()

                elif self.anim_montre:
                    if time.time()-self.chrono > 2:
                        self.montre_rect.y += 1
                    self.screen.blit(self.montre, self.montre_rect)
                    if self.montre_rect.top > 700:
                        self.anim_montre = False

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        jeu = False
                        running = False   

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a:
                                a = True
                        if event.key == pygame.K_e and self.teleportation:
                                self.carte_pos(False)
                                carte = True
                                jeu = False

                    if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or (self.pause_button.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONDOWN):
                            pause = True
                            self.take_screenshot()
                            self.init_menu(pause)
                            jeu=False    
                    
                    if self.map.name == "inboat" and self.player.feet.colliderect(self.map.PIRATE.rect):
                            self.teleportation = False
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_BACKSPACE:
                                    self.input_bateau = self.input_bateau[:-1]
                                else:
                                    if event.key not in [pygame.K_q,pygame.K_z,pygame.K_s,pygame.K_h,pygame.K_SPACE,pygame.K_v]:
                                        self.input_bateau += event.unicode

                    elif self.map.name == 'map':
                        if self.player.feet.colliderect(self.map.PNJ.rect):
                            self.teleportation = False
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_BACKSPACE:
                                    self.input_sage = self.input_sage[:-1]
                                else:
                                    if event.key not in [pygame.K_q,pygame.K_z,pygame.K_s,pygame.K_d,pygame.K_SPACE]:
                                        self.input_sage += event.unicode

                        elif self.player.feet.colliderect(self.map.ROCKET.rect):
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_BACKSPACE:
                                    self.input_final = self.input_final[:-1]
                                else:
                                    if event.key in self.keys_final:
                                        self.input_final += event.unicode

                self.change_mode_player(a) 
                pygame.display.flip()
                clock.tick(120)

        pygame.quit()
