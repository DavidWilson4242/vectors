from vector import Vector, VectorFunction, VectorField
import pygame
import random
import math

# game constants
SCREEN_SX = 1500
SCREEN_SY = 1000
COLORS = {
  "RED": (255, 0, 0),
  "GREEN": (0, 255, 0),
  "BLUE": (0, 0, 255),
  "BLACK": (0, 0, 0),
  "WHITE": (255, 255, 255),
  "TEAL": (0, 128, 128)
}

def constrain(n, minimum, maximum):
  return min(maximum, max(minimum, n))

def mapn(n, a, b, c, d):
  return (n - a)//(b - a) * (d - c) + c

def sgn(n):
  if n < 0:
    return -1
  elif n > 0:
    return 1
  return 0

class GameState:
  def __init__(self):
    self.initVectorField()
    self.initPygame()

  def initVectorField(self):
    self.field = VectorField(30, 20)
    
    padX = SCREEN_SX // (self.field.dimx - 1)
    padY = SCREEN_SY // (self.field.dimy - 1)

    for i in range(self.field.dimx):
      for j in range(self.field.dimy):
        self.field.origins[i][j] = Vector(i*padX, j*padY)
        self.field.field[i][j] = Vector(0, 0)

    # create some sort of function
    self.mouseFunc0 = VectorFunction(Vector(0, 0), lambda v: Vector(5*math.cos(v.x/200+2*v.y/200), 5*math.sin(v.x/200-2*v.y/200)))
    #self.mouseFunc0 = VectorFunction(Vector(0, 0), lambda v: Vector(sgn(v.y)*(v.y/12)**2, sgn(v.x)*(v.x/12)**2)*0.01)
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
        sf = 8

        # scale arrow down if it's too long
        if vec.magnitude > 10:
          sf *= 10/vec.magnitude

        startPos = (origin.x, origin.y)
        endPos = (origin.x + vec.x*sf, origin.y + vec.y*sf)
        
        cval = constrain(vec.magnitude*10, 0, 100) * (255.0 / 100.0)
        color = (cval, 100, 255 - cval)
        pygame.draw.line(self.screen, color, startPos, endPos, 3)

        # calculate theta angle of line
        unit =  vec.unit()
        theta = math.atan2(unit.y, unit.x)
        tdown = theta + 5*math.pi/4
        tup   = theta - 5*math.pi/4
        topLen = 8
        
        tDownEnd   = (endPos[0] + math.cos(tdown)*topLen, endPos[1] + math.sin(tdown)*topLen)
        tUpEnd     = (endPos[0] + math.cos(tup)*topLen, endPos[1] + math.sin(tup)*topLen)
        
        head = [endPos, tDownEnd, tUpEnd]
        pygame.draw.polygon(self.screen, color, head)

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
