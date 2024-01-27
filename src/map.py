import pygame
import pyscroll

from rocket import Rocket
from pnj import PNJ
from ball import Ball

class Map:

    def __init__(self, player, where, spawn, n, tmx_data, velos):

        self.name = where
        self.player = player
        if self.name == 'map':
            self.PNJ = PNJ('pnj1', (16,20),tmx_data.get_object_by_name("spawn_pnj1"))
            self.PNJ2 = PNJ('pnj_home', (16,20), tmx_data.get_object_by_name("spawn_home"))
            self.WIZARD = PNJ('wizard', (43.6/1.3,28.2/1.3), tmx_data.get_object_by_name("spawn_wizard"))
            self.ROCKET = Rocket(428, 735)
            self.BALL = Ball()
            self.MONK = PNJ('monkey', (20,20), tmx_data.get_object_by_name("spawn_monkey"))
        else:
            self.player.mode = 'marche'
            self.player.speed = 1
        if self.name == "housecave":
            self.PARCHEMIN = PNJ('parchment', (27,10), tmx_data.get_object_by_name("spawn_parchemin"))
        if self.name == 'inboat':
            self.PIRATE = PNJ('pirate', (30,30), tmx_data.get_object_by_name("spawn_pirate"))
            self.player.mode = 'marche'
            self.player.speed = 1
        if self.name == 'farmetage':
            self.BANANA = PNJ('banana', (17,15), tmx_data.get_object_by_name("spawn_banana"))
            self.player.mode = 'marche'
            self.player.speed = 1
        elif self.name == 'loti':
            self.POTION = PNJ('potion',(12,13), tmx_data.get_object_by_name("spawn_potion"))

        # DIMENSION
        l = ['tresor', 'loti', 'farm1', 'farmetage', 'farm2', 'farm3', 'maisonnette']
        if "house" in self.name or "trou" in self.name or self.name in l:
            dim = (350, 350)
        elif self.name == 'cave':
            dim = (500, 500)
        else:
            dim = (700, 700)

        # charger carte
        self.tmx_data = tmx_data
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, dim)
        map_layer.zoom = 2        

        # draw calques group
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer = 7)
        self.group.add(self.player)
        if where == 'map':
            self.group.add(self.PNJ)
            self.group.add(self.PNJ2)
            self.group.add(self.ROCKET)
            self.group.add(self.BALL)
            self.group.add(self.MONK)
            self.group.add(self.WIZARD)
            self.group.add(velos)
        elif where == 'housecave':
            self.group.add(self.PARCHEMIN)
        elif where == 'inboat':
            self.group.add(self.PIRATE)
        elif where == 'farmetage':
            self.group.add(self.BANANA)
        elif where == 'loti':
            self.group.add(self.POTION)

        # dictionnaire des rect
        self.rect_porte = {}
        for porte in self.tmx_data.objects:
            if ("collision" not in porte.name) and ("pass" not in porte.name) and ("eau" not in porte.name) and ("spawn" not in porte.name):
                self.rect_porte[str(porte.name)] = pygame.Rect(porte.x, porte.y, porte.width, porte.height)

        # spawn
        self.n = n
        if spawn == 'house_map':
            self.player_position = self.tmx_data.get_object_by_name("spawn_"+spawn+n)
        else:
            self.player_position = self.tmx_data.get_object_by_name("spawn_"+spawn)

    def place(self):
        self.player.position[0] = self.player_position.x-self.player.rect.width/2
        self.player.position[1] = self.player_position.y

    def switch_test(self):
        '''
        Test si le player entre ds une porte
        O: porte
        '''
        for porte in self.rect_porte:
            if self.player.feet.colliderect(self.rect_porte[porte]):
                # si porte == 'map*_house'
                if porte.startswith('map') and porte.endswith('house'):
                    return True, 'map_house', self.num(porte, self.spawn_name(porte))
                else:
                    return True, porte, self.n
        return False, None, ''

    def spawn_name(self, porte):
        '''
        On recup le lieu de spawn (=la fin du nom de la porte)
        O: str : nom du lieu
        '''
        where = ''
        while not porte.endswith('_'):  
            where+=porte[-1]   
            porte=porte[:-1]
        where = where[::-1]
        return where

    def num(self, porte, spawn):
        '''
        On recup le numero de spawn pour les maison (=le nb apres 'map')
        O: str : numero
        '''
        n = ''
        while not porte.endswith('_'):
            porte=porte[:-1]
        porte=porte[:-1]
        n = porte[-1]
        return n



