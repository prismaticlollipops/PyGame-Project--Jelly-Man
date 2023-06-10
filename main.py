import pygame, sys
import os
import math
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from fishes import FishGroup
from fruit import Fruit
from pauser import Pause
from text import TextGroup
from sprites import LifeSprites
from sprites import MazeSprites
from mazedata import MazeData

pygame.init()

clock = pygame.time.Clock()
FPS = 12
pygame.mixer.init() #sound effects
BACKGROUND_MUSIC = pygame.mixer.Sound(os.path.join('assets', 'gelato beach.mp3'))
BACKGROUND_MUSIC.play(-1)
PELLETSOUND = pygame.mixer.Sound(os.path.join('assets', 'soundeffect.mp3'))

def show_start_menu():
    pygame.init()
    screen = pygame.display.set_mode((448, 576))
    pygame.display.set_caption("Jelly Man!")
    font_path = os.path.join('PressStart2P.ttf')
    font = pygame.font.Font(font_path, 29)
    surf = font.render('Play', True, 'white')
    surf3 = font.render('How to Play', True, 'white')
    surf2 = font.render('Quit', True, 'white')

#create scrolling background
    bg = pygame.image.load(os.path.join('assets', 'menubg.png')).convert()
    bg = pygame.transform.scale(bg, (448, 576))
    bg_width = bg.get_width()
    bg_rect = bg.get_rect()

    scroll = 0
    tiles = math.ceil(SCREENWIDTH / bg_width) + 1

    # dimensions of menu buttons
    play_button = pygame.Rect(130, 200, 200, 60)
    instructions_button = pygame.Rect(60, 280, 340, 60)
    quit_button = pygame.Rect(130, 360, 200, 60)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if play_button.collidepoint(event.pos):
                        return "play"
                    elif quit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                    if instructions_button.collidepoint(event.pos):
                        show_instructions() 

        font = pygame.font.Font(font_path, 20)
        text = font.render("Welcome to Jelly Man!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(224, 100))
        screen.blit(text, text_rect)

        clock.tick(FPS)

        for i in range(0, tiles):
            screen.blit(bg, (i * bg_width + scroll, 0))
            bg_rect.x = i * bg_width + scroll

            # scroll background
            scroll -= 5

            # reset scroll
            if abs(scroll) > bg_width:
                scroll = 0
                screen.blit(bg, (0, 0))
        # play button
        font = pygame.font.Font(None, 24)
        pygame.draw.rect(screen, (128, 128, 128), play_button)
        text = font.render("Play", True, (255, 255, 255))
        text_rect = text.get_rect(center=(230, 250))
        screen.blit(text, text_rect)
        a, b = pygame.mouse.get_pos()
        if play_button.x <= a <= play_button.x + 110 and play_button.y <= b <= play_button.y + 60:
            pygame.draw.rect(screen, (100, 180, 180), play_button)
        else:
            pygame.draw.rect(screen, (110, 110, 110), play_button)
        screen.blit(surf, (play_button.x + 44, play_button.y + 15))

#instructions button
        pygame.draw.rect(screen, (128, 128, 128), instructions_button)
        text = font.render("How to Play", True, (255, 255, 255))
        text_rect = text.get_rect(center=(230, 330))
        screen.blit(text, text_rect)
        c, d = pygame.mouse.get_pos()
        if instructions_button.x <= c <= instructions_button.x + 110 and instructions_button.y <= d <= instructions_button.y + 60:
            pygame.draw.rect(screen, (100, 180, 180), instructions_button)
        else:
            pygame.draw.rect(screen, (110, 110, 110), instructions_button)
        screen.blit(surf3, (instructions_button.x + 10, instructions_button.y + 15))

#quit button
        pygame.draw.rect(screen, (128, 128, 128), quit_button)
        text = font.render("Quit", True, (255, 255, 255))
        text_rect = text.get_rect(center=(230, 400))
        screen.blit(text, text_rect)
        e, f = pygame.mouse.get_pos()
        if quit_button.x <= e <= quit_button.x + 110 and quit_button.y <= f <= quit_button.y + 60:
            pygame.draw.rect(screen, (100, 180, 180), quit_button)
        else:
            pygame.draw.rect(screen, (110, 110, 110), quit_button)
        screen.blit(surf2, (quit_button.x + 45, quit_button.y + 15))

        pygame.display.flip()

def show_instructions():
    bg = pygame.image.load(os.path.join('assets', 'menubg.png')).convert()
    bg = pygame.transform.scale(bg, (450, 580))
    bg_width = bg.get_width()
    bg_rect = bg.get_rect()
    font_path = os.path.join('PressStart2P.ttf')
    font = pygame.font.Font(font_path, 12)
    larger_font = pygame.font.Font(font_path, 24)  # Larger font for "HOW TO PLAY"

    scroll = 0
    tiles = math.ceil(SCREENWIDTH / bg_width) + 1
    screen = pygame.display.set_mode((448, 576))
    pygame.display.set_caption("How to Play")

    # Render the text outside the main loop
    text = larger_font.render("HOW TO PLAY", True, BLACK)
    text1 = font.render("Press UP, DOWN, RIGHT, LEFT to move", True, BLACK)
    text2 = font.render("Don't let the fish eat you!", True, BLACK)
    text3 = font.render("Press SPACEBAR to pause the game", True, BLACK)
    text4 = font.render("Eat power pellets to kill the fish!", True, BLACK)

    text_rect = text.get_rect(center=(SCREENWIDTH // 2, SCREENHEIGHT // 2 - 150))
    text_rect1 = text1.get_rect(center=(SCREENWIDTH // 2, SCREENHEIGHT // 2 - 90))
    text_rect2 = text2.get_rect(center=(SCREENWIDTH // 2, SCREENHEIGHT // 2 - 30))
    text_rect3 = text3.get_rect(center=(SCREENWIDTH // 2, SCREENHEIGHT // 2 + 30))
    text_rect4 = text4.get_rect(center=(SCREENWIDTH // 2, SCREENHEIGHT // 2 + 90))

    back_button = pygame.Rect(20, 20, 100, 40)
    back_text = font.render("BACK", True, WHITE)
    back_text_rect = back_text.get_rect(center=back_button.center)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if back_button.collidepoint(event.pos):
                        return  # Return to the previous menu

        clock.tick(FPS)

        # Blit the background
        for i in range(0, tiles):
            screen.blit(bg, (i * bg_width + scroll, 0))
            bg_rect.x = i * bg_width + scroll

        # Blit the text on the screen
        screen.blit(text, text_rect)
        screen.blit(text1, text_rect1)
        screen.blit(text2, text_rect2)
        screen.blit(text3, text_rect3)
        screen.blit(text4, text_rect4)

        # Blit the back button
        pygame.draw.rect(screen, WHITE, back_button, 2)
        screen.blit(back_text, back_text_rect)

        # Scroll background
        scroll -= 5

        # Reset scroll
        if abs(scroll) > bg_width:
            scroll = 0
            screen.blit(bg, (0, 0))

        pygame.display.flip()

def main():
    while True:
        choice = show_start_menu()
        if choice == "play":
            # Initialize and start the game
            game = GameController()
            game.startGame()
            while True:
                game.update()
        elif choice == "quit":
            break

class GameController(object):
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Jelly Man!")
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.background_norm = None
        self.background_flash = None
        self.clock = pygame.time.Clock()
        self.fruit = None
        self.pause = Pause(True)
        self.level = 0
        self.lives = 5
        self.score = 0
        self.textgroup = TextGroup()
        self.lifesprites = LifeSprites(self.lives)
        self.flashBG = False
        self.flashTime = 0.2
        self.flashTimer = 0
        self.fruitCaptured = []
        self.fruitNode = None
        self.mazedata = MazeData()

    def setBackground(self):
        self.background = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'background.png')), SCREENSIZE)
        self.background_norm = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_flash = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_flash.fill(WHITE)
        self.background = self.mazesprites.constructBackground(self.background, self.level%5)
        self.background_flash = self.mazesprites.constructBackground(self.background_flash, 5)
        self.flashBG = False

    def startGame(self):      
        self.mazedata.loadMaze(self.level)
        self.mazesprites = MazeSprites(self.mazedata.obj.name+".txt", self.mazedata.obj.name+"_rotation.txt")
        self.setBackground()
        self.nodes = NodeGroup(self.mazedata.obj.name+".txt")
        self.mazedata.obj.setPortalPairs(self.nodes)
        self.mazedata.obj.connectHomeNodes(self.nodes)
        self.pacman = Pacman(self.nodes.getNodeFromTiles(*self.mazedata.obj.pacmanStart))
        self.pellets = PelletGroup(self.mazedata.obj.name+".txt")
        self.fishes = FishGroup(self.nodes.getStartTempNode(), self.pacman)

        self.fishes.pinky.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 3)))
        self.fishes.inky.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(0, 3)))
        self.fishes.clyde.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(4, 3)))
        self.fishes.setSpawnNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 3)))
        self.fishes.blinky.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 0)))

        self.nodes.denyHomeAccess(self.pacman)
        self.nodes.denyHomeAccessList(self.fishes)
        self.fishes.inky.startNode.denyAccess(RIGHT, self.fishes.inky)
        self.fishes.clyde.startNode.denyAccess(LEFT, self.fishes.clyde)
        self.mazedata.obj.denyfishesAccess(self.fishes, self.nodes)

    def startGame_old(self):      
        self.mazedata.loadMaze(self.level)
        self.mazesprites = MazeSprites("maze.txt", "maze_rotation.txt")
        self.setBackground()
        self.nodes = NodeGroup("maze.txt")
        self.nodes.setPortalPair((0,17), (27,17))
        homekey = self.nodes.createHomeNodes(11.5, 14)
        self.nodes.connectHomeNodes(homekey, (12,14), LEFT)
        self.nodes.connectHomeNodes(homekey, (15,14), RIGHT)
        self.pacman = Pacman(self.nodes.getNodeFromTiles(15, 26))
        self.pellets = PelletGroup("maze.txt")
        self.fishes = FishGroup(self.nodes.getStartTempNode(), self.pacman)
        self.fishes.blinky.setStartNode(self.nodes.getNodeFromTiles(2+11.5, 0+14))
        self.fishes.pinky.setStartNode(self.nodes.getNodeFromTiles(2+11.5, 3+14))
        self.fishes.inky.setStartNode(self.nodes.getNodeFromTiles(0+11.5, 3+14))
        self.fishes.clyde.setStartNode(self.nodes.getNodeFromTiles(4+11.5, 3+14))
        self.fishes.setSpawnNode(self.nodes.getNodeFromTiles(2+11.5, 3+14))

        self.nodes.denyHomeAccess(self.pacman)
        self.nodes.denyHomeAccessList(self.fishes)
        self.nodes.denyAccessList(2+11.5, 3+14, LEFT, self.fishes)
        self.nodes.denyAccessList(2+11.5, 3+14, RIGHT, self.fishes)
        self.fishes.inky.startNode.denyAccess(RIGHT, self.fishes.inky)
        self.fishes.clyde.startNode.denyAccess(LEFT, self.fishes.clyde)
        self.nodes.denyAccessList(12, 14, UP, self.fishes)
        self.nodes.denyAccessList(15, 14, UP, self.fishes)
        self.nodes.denyAccessList(12, 26, UP, self.fishes)
        self.nodes.denyAccessList(15, 26, UP, self.fishes)

        

    def update(self):
        dt = self.clock.tick(30) / 1000.0
        self.textgroup.update(dt)
        self.pellets.update(dt)
        if not self.pause.paused:
            self.fishes.update(dt)      
            if self.fruit is not None:
                self.fruit.update(dt)
            self.checkPelletEvents()
            self.checkFishEvents()
            self.checkFruitEvents()

        if self.pacman.alive:
            if not self.pause.paused:
                self.pacman.update(dt)
        else:
            self.pacman.update(dt)

        if self.flashBG:
            self.flashTimer += dt
            if self.flashTimer >= self.flashTime:
                self.flashTimer = 0
                if self.background == self.background_norm:
                    self.background = self.background_flash
                else:
                    self.background = self.background_norm

        afterPauseMethod = self.pause.update(dt)
        if afterPauseMethod is not None:
            afterPauseMethod()
        self.checkEvents()
        self.render()

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if self.pacman.alive:
                        self.pause.setPause(playerPaused=True)
                        if not self.pause.paused:
                            self.textgroup.hideText()
                            self.showEntities()
                        else:
                            self.textgroup.showText(PAUSETXT)
                            self.hideEntities()  # Hide entities when the game is paused


    def checkPelletEvents(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if pellet:
            self.pellets.numEaten += 1
            self.updateScore(pellet.points)
            if self.pellets.numEaten == 30:
                self.fishes.inky.startNode.allowAccess(RIGHT, self.fishes.inky)
            if self.pellets.numEaten == 70:
                self.fishes.clyde.startNode.allowAccess(LEFT, self.fishes.clyde)
            self.pellets.pelletList.remove(pellet)
            if pellet.name == POWERPELLET:
                self.fishes.startFreight()
            if self.pellets.isEmpty():
                self.flashBG = True
                self.hideEntities()
                self.pause.setPause(pauseTime=3, func=self.nextLevel)
            PELLETSOUND.play()

    def checkFishEvents(self):
        for fish in self.fishes:
            if self.pacman.collideFish(fish):
                if fish.mode.current is FREIGHT:
                    self.pacman.visible = False
                    fish.visible = False
                    self.updateScore(fish.points)                  
                    self.textgroup.addText(str(fish.points), WHITE, fish.position.x, fish.position.y, 8, time=1)
                    self.fishes.updatePoints()
                    self.pause.setPause(pauseTime=1, func=self.showEntities)
                    fish.startSpawn()
                    self.nodes.allowHomeAccess(fish)
                elif fish.mode.current is not SPAWN:
                    if self.pacman.alive:
                        self.lives -=  1
                        self.lifesprites.removeImage()
                        self.pacman.die()               
                        self.fishes.hide()
                        if self.lives <= 0:
                            self.textgroup.showText(GAMEOVERTXT)
                            self.pause.setPause(pauseTime=3, func=self.restartGame)
                        else:
                            self.pause.setPause(pauseTime=3, func=self.resetLevel)
    
    def checkFruitEvents(self):
        if self.pellets.numEaten == 50 or self.pellets.numEaten == 140:
            if self.fruit is None:
                self.fruit = Fruit(self.nodes.getNodeFromTiles(9, 20), self.level)
                print(self.fruit)
        if self.fruit is not None:
            if self.pacman.collideCheck(self.fruit):
                self.updateScore(self.fruit.points)
                self.textgroup.addText(str(self.fruit.points), WHITE, self.fruit.position.x, self.fruit.position.y, 8, time=1)
                fruitCaptured = False
                for fruit in self.fruitCaptured:
                    if fruit.get_offset() == self.fruit.image.get_offset():
                        fruitCaptured = True
                        break
                if not fruitCaptured:
                    self.fruitCaptured.append(self.fruit.image)
                self.fruit = None
            elif self.fruit.destroy:
                self.fruit = None

    def showEntities(self):
        self.pacman.visible = True
        self.fishes.show()

    def hideEntities(self):
        self.pacman.visible = False
        self.fishes.hide()

    def nextLevel(self):
        self.showEntities()
        self.level += 1
        self.pause.paused = True
        self.startGame()
        self.textgroup.updateLevel(self.level)

    def restartGame(self):
        self.lives = 5
        self.level = 0
        self.pause.paused = True
        self.fruit = None
        self.startGame()
        self.score = 0
        self.textgroup.updateScore(self.score)
        self.textgroup.updateLevel(self.level)
        self.textgroup.showText(READYTXT)
        self.lifesprites.resetLives(self.lives)
        self.fruitCaptured = []

    def resetLevel(self):
        self.pause.paused = True
        self.pacman.reset()
        self.fishes.reset()
        self.fruit = None
        self.textgroup.showText(READYTXT)

    def updateScore(self, points):
        self.score += points
        self.textgroup.updateScore(self.score)

    def render(self):
        self.screen.blit(self.background, (0, 0))
        #self.nodes.render(self.screen)
        self.pellets.render(self.screen)
        if self.fruit is not None:
            self.fruit.render(self.screen)
        self.pacman.render(self.screen)
        self.fishes.render(self.screen)
        self.textgroup.render(self.screen)

        for i in range(len(self.lifesprites.images)):
            x = self.lifesprites.images[i].get_width() * i
            y = SCREENHEIGHT - self.lifesprites.images[i].get_height()
            self.screen.blit(self.lifesprites.images[i], (x, y))

        for i in range(len(self.fruitCaptured)):
            x = SCREENWIDTH - self.fruitCaptured[i].get_width() * (i+1)
            y = SCREENHEIGHT - self.fruitCaptured[i].get_height()
            self.screen.blit(self.fruitCaptured[i], (x, y))

        pygame.display.update()


if __name__ == "__main__":
    main()



