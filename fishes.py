import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from modes import ModeController
from sprites import fishesprites

class Fish(Entity):
    def __init__(self, node, pacman=None, blinky=None):
        Entity.__init__(self, node)
        self.name = FISH
        self.points = 200
        self.goal = Vector2()
        self.directionMethod = self.goalDirection
        self.pacman = pacman
        self.mode = ModeController(self)
        self.blinky = blinky
        self.homeNode = node

    def reset(self):
        Entity.reset(self)
        self.points = 200
        self.directionMethod = self.goalDirection

    def update(self, dt):
        self.sprites.update(dt)
        self.mode.update(dt)
        if self.mode.current is SCATTER:
            self.scatter()
        elif self.mode.current is CHASE:
            self.chase()
        Entity.update(self, dt)

    def scatter(self):
        self.goal = Vector2()

    def chase(self):
        self.goal = self.pacman.position

    def spawn(self):
        self.goal = self.spawnNode.position

    def setSpawnNode(self, node):
        self.spawnNode = node

    def startSpawn(self):
        self.mode.setSpawnMode()
        if self.mode.current == SPAWN:
            self.setSpeed(95)
            self.directionMethod = self.goalDirection
            self.spawn()

    def startFreight(self):
        self.mode.setFreightMode()
        if self.mode.current == FREIGHT:
            self.setSpeed(50)
            self.directionMethod = self.randomDirection         

    def normalMode(self):
        self.setSpeed(95)
        self.directionMethod = self.goalDirection
        self.homeNode.denyAccess(DOWN, self)




class Blinky(Fish):
    def __init__(self, node, pacman=None, blinky=None):
        Fish.__init__(self, node, pacman, blinky)
        self.name = BLINKY
        self.colour = RED
        self.sprites = fishesprites(self)


class Pinky(Fish):
    def __init__(self, node, pacman=None, blinky=None):
        Fish.__init__(self, node, pacman, blinky)
        self.name = PINKY
        self.colour = PINK
        self.sprites = fishesprites(self)

    def scatter(self):
        self.goal = Vector2(TILEWIDTH*NCOLS, 0)

    def chase(self):
        self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4


class Inky(Fish):
    def __init__(self, node, pacman=None, blinky=None):
        Fish.__init__(self, node, pacman, blinky)
        self.name = INKY
        self.colour = TEAL
        self.sprites = fishesprites(self)

    def scatter(self):
        self.goal = Vector2(TILEWIDTH*NCOLS, TILEHEIGHT*NROWS)

    def chase(self):
        vec1 = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 2
        vec2 = (vec1 - self.blinky.position) * 2
        self.goal = self.blinky.position + vec2


class Clyde(Fish):
    def __init__(self, node, pacman=None, blinky=None):
        Fish.__init__(self, node, pacman, blinky)
        self.name = CLYDE
        self.colour = ORANGE
        self.sprites = fishesprites(self)

    def scatter(self):
        self.goal = Vector2(0, TILEHEIGHT*NROWS)

    def chase(self):
        d = self.pacman.position - self.position
        ds = d.magnitudeSquared()
        if ds <= (TILEWIDTH * 8)**2:
            self.scatter()
        else:
            self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4


class FishGroup(object):
    def __init__(self, node, pacman):
        self.blinky = Blinky(node, pacman)
        self.pinky = Pinky(node, pacman)
        self.inky = Inky(node, pacman, self.blinky)
        self.clyde = Clyde(node, pacman)
        self.fishes = [self.blinky, self.pinky, self.inky, self.clyde]

    def __iter__(self):
        return iter(self.fishes)

    def update(self, dt):
        for fish in self:
            fish.update(dt)

    def startFreight(self):
        for fish in self:
            fish.startFreight()
        self.resetPoints()

    def setSpawnNode(self, node):
        for fish in self:
            fish.setSpawnNode(node)

    def updatePoints(self):
        for fish in self:
            fish.points *= 2

    def resetPoints(self):
        for fish in self:
            fish.points = 200

    def hide(self):
        for fish in self:
            fish.visible = False

    def show(self):
        for fish in self:
            fish.visible = True

    def reset(self):
        for fish in self:
            fish.reset()

    def render(self, screen):
        for fish in self:
            fish.render(screen)

