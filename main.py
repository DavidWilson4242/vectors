from vector import Vector, VectorFunction, VectorField
import pygame
import random
import math

# game constants
SCREEN_SX = 800
SCREEN_SY = 800
COLORS = {
  "RED": (255, 0, 0),
  "GREEN": (0, 255, 0),
  "BLUE": (0, 0, 255),
  "BLACK": (0, 0, 0),
  "WHITE": (255, 255, 255),
  "TEAL": (0, 128, 128)
}

class GameState:
  def __init__(self):
    self.initVectorField()
    self.initPygame()

  def initVectorField(self):
    self.field = VectorField(20, 20)
    
    padX = SCREEN_SX // (self.field.dimx + 1)
    padY = SCREEN_SY // (self.field.dimy + 1)

    for i in range(self.field.dimx):
      for j in range(self.field.dimy):
        self.field.origins[i][j] = Vector((i + 1)*padX, (j + 1)*padY)
        self.field.field[i][j] = Vector(0, 0)

    # create some sort of function
    self.mouseFunc0 = VectorFunction(Vector(0, 0), lambda v: Vector(-v.y, v.x)*0.01)
    self.field.addFunction(self.mouseFunc0)

    self.mouseFunc1 = VectorFunction(Vector(0, 0), lambda v: Vector(0, 0))
    self.field.addFunction(self.mouseFunc1)

  def initPygame(self):
    pygame.init()
    self.screen = pygame.display.set_mode((SCREEN_SX, SCREEN_SY))

  def update(self):
    pos = pygame.mouse.get_pos()
    self.mouseFunc0.origin = Vector(pos[0], pos[1])
    self.mouseFunc1.origin = Vector(pos[0], pos[1])
    self.field.calculateValues()

  def draw(self):
    self.screen.fill(COLORS["BLACK"])
    for i in range(self.field.dimx):
      for j in range(self.field.dimy):
        origin = self.field.origins[i][j]
        vec = self.field.field[i][j]
        startPos = (origin.x, origin.y)
        endPos = (origin.x + vec.x*20, origin.y + vec.y*20)
        pygame.draw.line(self.screen, COLORS["TEAL"], startPos, endPos, 3)

        # calculate theta angle of line
        unit =  vec.unit()
        theta = math.atan2(unit.y, unit.x)
        tdown = theta + 9*math.pi/8
        tup   = theta - 9*math.pi/8
        topLen = 6
        
        tDownStart = (endPos[0], endPos[1])
        tDownEnd   = (endPos[0] + math.cos(tdown)*topLen, endPos[1] + math.sin(tdown)*topLen)
        tUpStart   = (endPos[0], endPos[1])
        tUpEnd     = (endPos[0] + math.cos(tup)*topLen, endPos[1] + math.sin(tup)*topLen)

        pygame.draw.line(self.screen, COLORS["TEAL"], tDownStart, tDownEnd, 3)
        pygame.draw.line(self.screen, COLORS["TEAL"], tUpStart, tUpEnd, 3)

    pygame.display.flip()

  def gameLoop(self):
    running = True
    while running:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False
      
      self.update()
      self.draw()

if __name__ == "__main__":
  game = GameState()
  game.gameLoop()
