import copy
import math

class Vector:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.magnitude = math.sqrt(x*x + y*y)

  def __add__(self, other):
    return Vector(self.x + other.x, self.y + other.y)

  def __sub__(self, other):
    return Vector(self.x - other.x, self.y - other.y)

  def __mul__(self, other):
    return Vector(self.x * other, self.y * other) 

  def unit(self):
    if self.magnitude == 0:
      return Vector(0, 0)
    return Vector(self.x/self.magnitude, self.y/self.magnitude)

class VectorFunction:
  def __init__(self, origin, func):
    self.origin = origin
    self.func = func

  def evaluate(self, evalAt):
    return self.func(evalAt - self.origin)

class VectorField:
  def __init__(self, dimx, dimy):
    self.dimx = dimx
    self.dimy = dimy
    self.field   = [[Vector(0, 0) for i in range(dimy)] for j in range(dimx)]
    self.origins = [[Vector(0, 0) for i in range(dimy)] for j in range(dimx)]
    self.funcs   = []

  def setValue(self, dimx, dimy, value):
    if dimx < 0 or dimx > self.dimx or dimy < 0 or dimy > self.dimy:
      raise ValueError("Index out of bounds")
    elif type(value) != "Vector":
      raise ValueError("Value must be a Vector")
    self.field[dimx][dimy] = copy.copy(value)

  def getValue(self, dimx, dimy):
    if dimx < 0 or dimx > self.dimx or dimy < 0 or dimy > self.dimy:
      raise ValueError("Index out of bounds")
    return self.field[dimx][dimy]

  def calculateValues(self):
    for i in range(self.dimx):
      for j in range(self.dimy):
        netVec = Vector(0, 0)
        for func in self.funcs: 
          netVec += func.evaluate(self.origins[i][j])
        self.field[i][j] = netVec

  def addFunction(self, func):
    if type(func).__name__ != "VectorFunction":
      raise ValueError("Must be of type VectorFunction")
    self.funcs.append(func)
    
