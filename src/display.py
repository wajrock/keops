import pygame

class Display:
    def __init__(self):
        #INITIALISATION COULEURS BOUTTONS
        self.color_play_button,self.color_options_button,self.color_quit_button,self.color_pause_play_button,self.color_pause_options_button,self.color_pause_quit_button,self.color_succes_button = 7*[(255, 255, 255)]
        
        #COULEURS ITEMS
        self.jouer_color, self.options_color, self.quit_color, self.difficulte_color, self.touches_color, self.retour_color, self.facile_color, self.normal_color, self.difficile_color, self.lettres_color, self.fleches_color,self.succes_color = 12*[(46, 204, 113)]
        
         

        # CREATION BOUTON MENU
        self.play_button = pygame.Rect(mid, 400, 180 , 60)
        self.options_button = pygame.Rect(mid, 480, 180 , 60)
        self.quit_button = pygame.Rect(mid, 560, 180 , 60)

        # CREATION BOUTON MENU PAUSE
        self.play_pause_button = pygame.Rect(mid-20, 400, 220 , 60)
        self.options_pause_button = pygame.Rect(mid-20, 480, 220 , 60)
        self.quitter_pause_rect = pygame.Rect(mid-20, 560, 220 , 60)

        self.succes_rect = pygame.Rect(mid, 400, 180 , 60)

    def hover_menu(self,mouse):
        # interaction quand on survole un bouton
            # DIFFICULTE
            if self.play_button.collidepoint(mouse):
                if self.play_button.height < 70:
                    self.play_button.inflate_ip(2, 2)
                self.jouer_color = (255,255,255)
                self.color_play_button = (46, 204, 113)
                self.init_menu()
            elif self.play_button.height > 60:
                self.play_button.inflate_ip(-2, -2)
                self.jouer_color = (46, 204, 113)
                self.color_play_button = (255,255,255)
                self.init_menu()

            # TOCUHES
            if self.options_button.collidepoint(mouse):
                if self.options_button.height < 70:
                    self.options_button.inflate_ip(2, 2)
                self.options_color = (255,255,255)
                self.color_options_button = (46, 204, 113)
                self.init_menu()
            elif self.options_button.height > 60:
                self.options_button.inflate_ip(-2, -2)
                self.options_color = (46, 204, 113)
                self.color_options_button = (255,255,255)
                self.init_menu()

            # RETOUR
            if self.quit_button.collidepoint(mouse):
                if self.quit_button.height < 70:
                    self.quit_button.inflate_ip(2, 2)
                self.quit_color = (255,255,255)
                self.color_quit_button = (46, 204, 113)
                self.init_menu()
            elif self.quit_button.height > 60:
                self.quit_button.inflate_ip(-2, -2)
                self.quit_color = (46, 204, 113)
                self.color_quit_button = (255,255,255)
                self.init_menu()