import pygame
import os
import time
from random import randrange
import sys

class Settings(object):
    
    #___Game einstellungen___
    width = 1100
    height = 600
    fps = 60
    title = "Pokemon Catch"
    screen = pygame.display.set_mode((1100, 600))

    #___Dateipfade___
    file_path = os.path.dirname(os.path.abspath(__file__))
    images_path = os.path.join(file_path, "images")
    sounds_path = os.path.join(file_path, "sounds")
    
    #___Boolvariablen___
    pause = False
    collision = False
    gameover = False
    
    #___Intvariablen___
    time_unit = 60
    boardersize = 10
    score = 0

    staticmethod
    def get_dim():
        return (Settings.width, Settings.height)

class Pokeball(pygame.sprite.Sprite):
    def __init__(self, pygame):
        super(). __init__()
        self.time = 0
        self.radius = 5
        self.image = pygame.image.load(os.path.join(Settings.images_path, "Pokeball.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(self.radius*2), int(self.radius*2)))
        self.rect = self.image.get_rect()
        self.cx = self.rect.centerx
        self.cy = self.rect.centery
        self.update()
        self.rect.left = randrange(0 + Settings.boardersize, Settings.width - self.radius*2 - Settings.boardersize)
        self.rect.top = randrange(0 + Settings.boardersize, Settings.height - self.radius*2 - Settings.boardersize)
        #___zufallszahl zwischen 1 bis 4 für das Wachstum
        self.grow = randrange(1 , 4)

    def update(self):
        #___verlangsamt das Wachstum auf 1sek
        self.time += 1
        if self.time >= Settings.time_unit:
            #___wachstum
            self.radius += self.grow
            self.image = pygame.image.load(os.path.join(Settings.images_path, "Pokeball.png")).convert_alpha()
            self.image = pygame.transform.scale(self.image, (int(self.radius*2), int(self.radius*2)))
            self.cx = self.rect.centerx
            self.cy = self.rect.centery
            self.rect = self.image.get_rect()
            self.rect.centerx = self.cx
            self.rect.centery = self.cy
            self.time = 0
        #___Pokeball kollisiontsabfrage mit der Maus
        if pygame.mouse.get_pressed()[0] == True:
            if pygame.mouse.get_pos()[0] <= self.cx + self.radius:
                if pygame.mouse.get_pos()[0] >= self.cx - self.radius:
                    if pygame.mouse.get_pos()[1] <= self.cy + self.radius:
                        if pygame.mouse.get_pos()[1] >= self.cy - self.radius:
                            self.kill()
                            self.burst_sound = pygame.mixer.Sound("C:/Users/Lars/Documents/Bublles_Projekt_Trenczek_ITA19b/sounds/Coin_sound.mp3")
                            self.burst_sound.set_volume(.15)
                            self.burst_sound.play()
                            Settings.score += int(self.radius/15)

        #___Pokeball kollisionsabfrag untereinander
        for pokeballs in game.all_pokeballs:
            if pokeballs is self:
                continue
            if pygame.sprite.collide_mask(self, pokeballs):
                Settings.gameover = True

class Mouse(pygame.sprite.Sprite):
    def __init__(self, pygame):
        super(). __init__()
        self.image_original = pygame.image.load(os.path.join(Settings.images_path, "coursor.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image_original, (50, 50))
        self.rect = self.image_original.get_rect()
        self.update()


    def update(self):
        self.rect.left = pygame.mouse.get_pos()[0]
        self.rect.top = pygame.mouse.get_pos()[1]
        #setzt die Maus auf die Mitte des Bilds
        self.rect.left -= 25
        self.rect.top -= 25


class Pause():
    def __init__(self):
        self.screen = pygame.display.set_mode(Settings.get_dim())
        self.fade = pygame.Surface((Settings.width, Settings.height)) 
        self.fade.fill((0, 0, 0))
        self.fade.set_alpha(100)
        self.end_pause = False
        self.clock = pygame.time.Clock()
        #Objekt der Klasse Text
        self.text = Text()

    def pause_screen(self):
        self.screen.blit(self.fade,( 0, 0))
        while self.end_pause == False:
            self.clock.tick(60)
            pygame.mixer.music.pause()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.end_pause = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.end_pause = True
                        game.run()
            self.text.render("Pause")
            pygame.display.flip()

            

class Text(object):
    def __init__ (self):
        #___erstellt fonts
        pygame.font.init()
        self.font = pygame.font.SysFont("Comicsans", 44)
        self.punkte_font = pygame.font.SysFont("Comicsans", 34)

    def render(self, Game_over):
        #___font für Game Over und Pause
        text = self.font.render(Game_over, True, (255,255,255))
        Settings.screen.blit(text, ((Settings.width / 2, Settings.height / 2)))

    def render_punkte(self, Punkte):
        #___font für Punktestand
        text = self.punkte_font.render(Punkte, True, (255,255,255))
        Settings.screen.blit(text, (( 0 , 0 )))

class Game(object):
    def __init__(self):
        self.screen = pygame.display.set_mode(Settings.get_dim())
        pygame.display.set_caption(Settings.title)
        self.background = pygame.image.load(os.path.join(Settings.images_path, "background2.0.png")).convert()
        self.background = pygame.transform.scale(self.background, (Settings.width, Settings.height))
        self.background_rect = self.background.get_rect()

        self.clock = pygame.time.Clock()
        self.done = False

        self.time_unit_reducer = 0
        self.gameover = 0

        #___erstellt die Spritegroup all_pokeballs
        self.all_pokeballs = pygame.sprite.Group()
        self.time = 0

        #___erstellt die Spritegroup all_mouse
        self.all_mouse = pygame.sprite.Group()
        #___erstellt ein Objekt der Klasse Mouse
        self.mouse = Mouse(pygame)
        #___fügt das gerade erstellte Objekt der Spritegroup zu 
        self.all_mouse.add(self.mouse)
        #___stellt ein das die Originalmaus nichtmehr sichbar ist
        pygame.mouse.set_visible(False)

        #___erstellt ein Objekt der Klasse Pause
        self.pause = Pause()

        #___erstellt ein Objekt der Klasse Text
        self.text = Text()

        #_______________________________________________Musik_____________________________________________________
        pygame.mixer.music.load(os.path.join(Settings.sounds_path, "Dire, Dire Docks.mp3"))
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(.10)
        #_________________________________________________________________________________________________________

    def run(self):
        while not self.done:
            self.clock.tick(Settings.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True

                
                #___überprüft ob ein Taste gerdrückt wird
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.done = True
                
                #___überpüft ob eine Taste losgelassen wird
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_p:
                        self.pause.pause_screen()
                        self.pause.end_pause = False
                        pygame.mixer.music.unpause()
                
                #___überprüft ob die Variable gameover aus der Klasse Settings den Status True hat und spielt fals ja den Gameoversound ab 
                if Settings.gameover == True:
                    if self.gameover <= 0:
                        self.gameover_sound = pygame.mixer.Sound("C:/Users/Lars/Documents/Bublles_Projekt_Trenczek_ITA19b/sounds/gameover_sound.wav")
                        self.gameover_sound.set_volume(.15)
                        self.gameover_sound.play()
                        self.gameover += 1

                #___überprüft erst ob eine taste gedrückt wird und ob Settings.gamover den Status True hat,
                #___falls ja überprüft es dann ob die taste r gedrückt wurde und starten falls ja dann das Spiel neu
                if event.type == pygame.KEYDOWN and Settings.gameover:
                    if event.key == pygame.K_r:
                        os.execv(sys.executable, ['python'] + sys.argv)
                        sys.exit()

            #___zeigt den Punktestand an
            self.text.render_punkte(f"punktestand:{str(Settings.score)}")
            pygame.display.flip() 

            #___erhöht die Variable die die Zeiteinheit reduzieren soll
            self.time_unit_reducer += 1

            #___überprüft ob die zeiteinheit größer als 10 ist
            if Settings.time_unit > 10:
                #___überprüft die oben erhöhte Variable 120 mal erhöht wurde
                if self.time_unit_reducer == 120:
                    #___reduziert die Zeiteinheit
                    Settings.time_unit -= 1
                    #___setzt die Variable von oben auf 0
                    self.time_unit_reducer = 0
            
            #___überprüft ob settings.gamover den Status False hat
            if Settings.gameover == False:
                #___die Funktionen die unten stehen
                self.limiter()
                self.collision()
                self.change_mouse()
            #___wenn Settings.gamover nicht den Status False hat werden die sachen von drunter ausgeführt
            else:
                #___pausiert die Musik
                pygame.mixer.music.pause()
                #___Schreibt den Text Game_over in die oben Linke
                self.text.render("Game_over")
                #___Zeichnet den Text von drüber
                pygame.display.flip()


    #_____________________________________________Kollision_________________________________________________    
    def collision(self):
        if pygame.sprite.spritecollide(self.mouse, self.all_pokeballs, False):
            Settings.collision = True
        else:
            Settings.collision = False
    #______________________________________________________________________________________________________________             

    #______________________________________________Maus ändern_____________________________________________________
    def change_mouse(self):
        if Settings.collision == True:
            self.mouse.image = pygame.image.load(os.path.join(Settings.images_path, "coursor_gedreht.png")).convert_alpha()
            self.mouse.image = pygame.transform.scale(self.mouse.image, (50, 50))
        else:
            self.mouse.image = pygame.image.load(os.path.join(Settings.images_path, "coursor.png")).convert_alpha()
            self.mouse.image = pygame.transform.scale(self.mouse.image, (50, 50))
    #______________________________________________________________________________________________________________

    #_____________________________________________Limiter und zeichnen_____________________________________________
    def limiter(self):
        self.all_pokeballs.update()
        self.time += 1
        if self.time >= Settings.time_unit:
            if len(self.all_pokeballs) < 30:
                self.pokeball = Pokeball(pygame)
                self.all_pokeballs.add(self.pokeball)
            self.time = 0


        self.screen.blit(self.background, self.background_rect)
        self.all_pokeballs.draw(self.screen)
        self.all_pokeballs.update()
        self.all_mouse.draw(self.screen)
        self.all_mouse.update()
        pygame.display.flip()
    #______________________________________________________________________________________________________________

if __name__ == '__main__': 
                                    
    pygame.init() 
    #___erstellt ein Objekt der Klasse Game
    game = Game()
    #___führt die run funktion des run mit dem Objekt game aus
    game.run()

    pygame.quit()