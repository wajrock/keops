import pygame
import pytmx

class Player(pygame.sprite.Sprite):

    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3

    def __init__(self):

        super().__init__()

        self.dict_map = {
            'map' : pytmx.util_pygame.load_pygame('./tmx/map.tmx', pixel_alpha = True),  
            'pyr' : pytmx.util_pygame.load_pygame('./tmx/pyr.tmx', pixel_alpha = True),  
            'trappe' : pytmx.util_pygame.load_pygame('./tmx/trappe.tmx', pixel_alpha = True),  
            'cave' : pytmx.util_pygame.load_pygame('./tmx/cave.tmx', pixel_alpha = True),  
            'housecave' : pytmx.util_pygame.load_pygame('./tmx/housecave.tmx', pixel_alpha = True),  
            'house' : pytmx.util_pygame.load_pygame('./tmx/house.tmx', pixel_alpha = True),  
            'boat' : pytmx.util_pygame.load_pygame('./tmx/boat.tmx', pixel_alpha = True),  
            'inboat' : pytmx.util_pygame.load_pygame('./tmx/inboat.tmx', pixel_alpha = True),  
            'trou' : pytmx.util_pygame.load_pygame('./tmx/trou.tmx', pixel_alpha = True) ,
            'trou2' : pytmx.util_pygame.load_pygame('./tmx/trou2.tmx', pixel_alpha = True), 
            'tresor' : pytmx.util_pygame.load_pygame('./tmx/tresor.tmx', pixel_alpha = True),
            'loti' : pytmx.util_pygame.load_pygame('./tmx/loti.tmx', pixel_alpha = True), 
            'farm1' : pytmx.util_pygame.load_pygame('./tmx/farm1.tmx', pixel_alpha = True),
            'farm2' : pytmx.util_pygame.load_pygame('./tmx/farm2.tmx', pixel_alpha = True),
            'farm3' : pytmx.util_pygame.load_pygame('./tmx/farm3.tmx', pixel_alpha = True),
            'farmetage' : pytmx.util_pygame.load_pygame('./tmx/farmetage.tmx', pixel_alpha = True),
            'maisonnette' : pytmx.util_pygame.load_pygame('./tmx/maisonnette.tmx', pixel_alpha = True)
        }

        # definit vers où va le joueur
        self.direction = Player.RIGHT
        # definit l'image du joueur lorsque qu'il bouge
        self.move = 2
        self.count_move = 0
        # MARCHE ------------------
        self.down_images = [
            pygame.transform.scale(pygame.image.load('./assets/pnj/marche/player_f1.png').convert_alpha(), (16,20)),
            pygame.transform.scale(pygame.image.load('./assets/pnj/marche/player_f2.png').convert_alpha(), (16,20)),
            pygame.transform.scale(pygame.image.load('./assets/pnj/marche/player_f0.png').convert_alpha(), (16,20))       
        ]
        self.right_images = [
            pygame.transform.scale(pygame.image.load('./assets/pnj/marche/player_r1.png').convert_alpha(), (16,20)),
            pygame.transform.scale(pygame.image.load('./assets/pnj/marche/player_r2.png').convert_alpha(), (16,20)),
            pygame.transform.scale(pygame.image.load('./assets/pnj/marche/player_r0.png').convert_alpha(), (16,20))
        ] 
        self.left_images = [
            pygame.transform.scale(pygame.image.load('./assets/pnj/marche/player_l1.png').convert_alpha(), (16,20)),
            pygame.transform.scale(pygame.image.load('./assets/pnj/marche/player_l2.png').convert_alpha(), (16,20)),
            pygame.transform.scale(pygame.image.load('./assets/pnj/marche/player_l0.png').convert_alpha(), (16,20))
        ]
        self.up_images = [
            pygame.transform.scale(pygame.image.load('./assets/pnj/marche/player_b1.png').convert_alpha(), (16,20)),
            pygame.transform.scale(pygame.image.load('./assets/pnj/marche/player_b2.png').convert_alpha(), (16,20)),
            pygame.transform.scale(pygame.image.load('./assets/pnj/marche/player_b0.png').convert_alpha(), (16,20))
        ] 
        # NAGE ------------------
        self.down_images_nage = [
            pygame.transform.scale(pygame.image.load('./assets/pnj/nage/player_n_f1.png').convert_alpha(), (16,20)),
            pygame.transform.flip(pygame.transform.scale(pygame.image.load('./assets/pnj/nage/player_n_f1.png').convert_alpha(), (16,20)), 1, 0),
            pygame.transform.scale(pygame.image.load('./assets/pnj/nage/player_n_f0.png').convert_alpha(), (16,20))       
        ]
        self.left_images_nage = [
            pygame.transform.scale(pygame.image.load('./assets/pnj/nage/player_n_l1.png').convert_alpha(), (16,20)),
            pygame.transform.scale(pygame.image.load('./assets/pnj/nage/player_n_l2.png').convert_alpha(), (16,20)),
            pygame.transform.scale(pygame.image.load('./assets/pnj/nage/player_n_l0.png').convert_alpha(), (16,20))
        ]
        self.right_images_nage = [
            pygame.transform.flip(self.left_images_nage[0], 1, 0),
            pygame.transform.flip(self.left_images_nage[1], 1, 0),
            pygame.transform.flip(self.left_images_nage[2], 1, 0)
        ] 
        self.up_images_nage = [
            pygame.transform.scale(pygame.image.load('./assets/pnj/nage/player_n_b1.png').convert_alpha(), (16,20)),
            pygame.transform.flip(pygame.transform.scale(pygame.image.load('./assets/pnj/nage/player_n_b1.png').convert_alpha(), (16,20)), 1, 0),
            pygame.transform.scale(pygame.image.load('./assets/pnj/nage/player_n_b0.png').convert_alpha(), (16,20))
        ] 
        # BIKE ------------------
        self.down_images_bike = [
            pygame.transform.scale(pygame.image.load('./assets/pnj/velo/player_b_f1.png').convert_alpha(), (16,20)),
            pygame.transform.flip(pygame.transform.scale(pygame.image.load('./assets/pnj/velo/player_b_f1.png').convert_alpha(), (16,20)), 1, 0),
            pygame.transform.scale(pygame.image.load('./assets/pnj/velo/player_b_f0.png').convert_alpha(), (16,20))       
        ]
        self.left_images_bike = [
            pygame.transform.scale(pygame.image.load('./assets/pnj/velo/player_b_l1.png').convert_alpha(), (22,20)),
            pygame.transform.scale(pygame.image.load('./assets/pnj/velo/player_b_l2.png').convert_alpha(), (22,20)),
            pygame.transform.scale(pygame.image.load('./assets/pnj/velo/player_b_l0.png').convert_alpha(), (22,20))
        ]
        self.right_images_bike = [
            pygame.transform.flip(self.left_images_bike[0], 1, 0),
            pygame.transform.flip(self.left_images_bike[1], 1, 0),
            pygame.transform.flip(self.left_images_bike[2], 1, 0) 
        ] 
        self.up_images_bike = [
            pygame.transform.scale(pygame.image.load('./assets/pnj/velo/player_b_b1.png').convert_alpha(), (16,20)),
            pygame.transform.flip(pygame.transform.scale(pygame.image.load('./assets/pnj/velo/player_b_b1.png').convert_alpha(), (16,20)), 1, 0),
            pygame.transform.scale(pygame.image.load('./assets/pnj/velo/player_b_b0.png').convert_alpha(), (16,20))
        ] 
        self.go_velo = False
        self.mode = 'marche'
        self.images = {
            'marche': [self.left_images, self.up_images, self.right_images, self.down_images], 
            'nage': [self.left_images_nage, self.up_images_nage, self.right_images_nage, self.down_images_nage],
            'velo': [self.left_images_bike, self.up_images_bike, self.right_images_bike, self.down_images_bike]
        }
        self.image = self.images[self.mode][self.direction][self.move]
        self.rect = self.image.get_rect()
        

        # RECT
        # on definit un rectangle correspondant au pied du joueur pour gérer les collisions
        self.feet_marche = pygame.Rect(0, 0, self.rect.width-5, self.rect.height-14)
        self.feet_velo_ver = pygame.Rect(0, 0, 16, 6)
        self.feet_velo_hor = pygame.Rect(0, 0, 16, 6)
        self.feet = self.feet_marche
        # FOOTBALL
        self.body = pygame.Rect(0, 0, self.rect.width, self.rect.height-4)

        self.position = [0,0]
        self.speed = 1
        # pour definir l'image du sprite à afficher 
        # si la odl_pos est en dessous de la pos alors image du player vers le haut
        self.old_position = [0,0]

        self.jump = [False, '', False] #1 jump ou non #2 jump vers ou #3 collision sur un object passable

    def collision(self):
        '''
        Renvoie True si les pieds du joueur entre en collision avec un mur
        O: bool : collision ou non
        '''
        # velo
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        self.feet[0]-=1
        if not self.jump[0]:
            if self.feet.collidelist(self.walls) > -1:
                return True

    def change_mode(self, velo, a):
        '''
        Renvoie True si les pieds du joueur entre en collision avec de l'eau
        I: velo : bool : collision_velo
           a : bool : touche "a" enfoncée
        O: bool : collision ou non
        '''
        self.feet.midbottom = self.rect.midbottom
        self.feet[0]-=1
        if self.feet.collidelist(self.rect_eau) > -1:
            self.mode = 'nage'
            self.speed = 1
        elif self.mode == 'velo' and a:
            self.mode = 'marche'
            self.speed = 1
        elif velo and a:
            self.mode = 'velo'
            self.speed = 2
        elif self.mode!='marche' and self.mode !='velo':
            self.mode = 'marche'
            self.speed = 1
            
        return self.rect.center

    def detect_jump_ver(self):
        '''
        Renvoie True si les pieds du joueur entre en collision avec un mur vertical à sauter
        O: bool : collision ou non et on passe
           str : direction du jump
           bool : si l'element est impassable dans cette direction
        '''
        self.feet.midbottom = self.rect.midbottom
        self.feet[0]-=1
        if self.feet.collidelist(self.pass_ver) > -1:
            if self.mode == 'velo':
                return False, '', True
            if self.old_position[0] < self.position[0]:
                return True, 'r', False
            elif self.old_position[0] > self.position[0]:
                return True, 'l', False
            if self.old_position[1] < self.position[1]:
                return False, '', True
            elif self.old_position[1] > self.position[1]:
                return False, '', True
        return False, '', False

    def detect_jump_hor(self):
        '''
        Renvoie True si les pieds du joueur entre en collision avec un mur horizontale à sauter
        O: bool : collision ou non et on passe
           str : direction du jump
           bool : si l'element est impassable dans cette direction
        '''
        self.feet.midbottom = self.rect.midbottom
        self.feet[0]-=1
        if self.feet.collidelist(self.pass_hor) > -1:
            if self.mode == 'velo':
                return False, '', True
            if self.old_position[1] < self.position[1]:
                return True, 'd', False
            elif self.old_position[1] > self.position[1]:
                return True, 'u', False
            if self.old_position[0] < self.position[0]:
                return False, '', True
            elif self.old_position[0] > self.position[0]:
                return False, '', True
        return False, '', False


    def new_world(self, world):
        
        self.walls = []
        self.pass_ver = []
        self.pass_hor = []
        self.rect_eau = []
        self.velo = []
        self.lignes_terrain_hor = []
        self.lignes_terrain_ver = []
        self.ordi = pygame.Rect(0,0,0,0)

        # pour chaque objets nommés collision 
        # on ajoute son rectangle équivalents dans la liste "self.walls"
        for obj in self.dict_map[world].objects:
            if obj.name == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.name == "eau":
                self.rect_eau.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.name == "pass_ver":
                self.pass_ver.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.name == "pass_hor":
                self.pass_hor.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.name == "collision_ligne_hor":
                self.lignes_terrain_hor.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.name == "collision_ligne_hor":
                self.lignes_terrain_hor.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.name == "collision_ligne_ver":
                self.lignes_terrain_ver.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.name == "collision_velo":
                self.velo.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.name == "collision_rouge":
                self.but_rouge = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            elif obj.name == "collision_bleu":
                self.but_bleu = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            elif obj.name == "collision_terrain":
                self.terrain = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            elif obj.name == "collision_stade":
                self.stade = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            elif obj.name == "collision_ordi":
                self.ordi = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
        
    def animation(self, dir):  
        # si le joueur ne va que dans une seule direction on l'affecte à celle-ci      
        if dir != '':
            if dir == 'l':
                self.direction = Player.LEFT
            elif dir == 'r':
                self.direction = Player.RIGHT
            elif dir == 'u':
                self.direction = Player.UP
            elif dir == 'd':
                self.direction = Player.DOWN

        # sinon on regarde son deplacement
        else:
            if self.old_position[0] < self.position[0]:
                self.direction = Player.RIGHT
            elif self.old_position[0] > self.position[0]:
                self.direction = Player.LEFT        
            if self.old_position[1] < self.position[1]:
                self.direction = Player.DOWN
            elif self.old_position[1] > self.position[1]:
                self.direction = Player.UP

        self.image = self.images[self.mode][self.direction][self.move]
        self.old_position = self.position.copy()

    def move_right(self):
        self.count_move += 1
        if self.count_move%10 == 0: self.move+=1
        self.move = self.move%2
        self.position[0] += self.speed
        self.update()
        # si le joueur entre en collision avec un mur sont deplacement s'annule
        if self.collision() or self.detect_jump_hor()[2]:
            self.position[0] -= self.speed
        if self.detect_jump_ver()[0]:
            self.jump[0] = True
            self.jump[1] = self.detect_jump_ver()[1]
        elif self.detect_jump_ver()[2]:
            self.position[0] -= self.speed

    def move_left(self):
        self.count_move += 1
        if self.count_move%10 == 0: self.move+=1
        self.move = self.move%2
        self.position[0] -= self.speed
        self.update()
        if self.collision() or self.detect_jump_hor()[2]:
            self.position[0] += self.speed
        if self.detect_jump_ver()[0]:
            self.jump[0] = True
            self.jump[1] = self.detect_jump_ver()[1]
        elif self.detect_jump_ver()[2]:
            self.position[0] += self.speed

    def move_up(self):
        self.count_move += 1
        if self.count_move%10 == 0: self.move+=1
        self.move = self.move%2
        self.position[1] -= self.speed
        self.update()
        if self.collision() or self.detect_jump_ver()[2]:
            self.position[1] += self.speed
        if self.detect_jump_hor()[0]:
            self.jump[0] = True
            self.jump[1] = self.detect_jump_hor()[1]
        elif self.detect_jump_hor()[2]:
            self.position[1] += self.speed


    def move_down(self):
        self.count_move += 1
        if self.count_move%10 == 0: self.move+=1
        self.move = self.move%2
        self.position[1] += self.speed
        self.update()
        if self.collision() or self.detect_jump_ver()[2]:
            self.position[1] -= self.speed
        if self.detect_jump_hor()[0]:
            self.jump[0] = True
            self.jump[1] = self.detect_jump_hor()[1]
        elif self.detect_jump_hor()[2]:
            self.position[1] -= self.speed

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        self.body.midbottom = self.rect.midbottom

