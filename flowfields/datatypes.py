from dataclasses import dataclass
import numpy as np

@dataclass
class Pos:
    x: int = 0
    y: int = 0
    
    def __repr__(self):
        return f'{self.x}, {self.y}'
    
    def distanceBetween(self, p):
        return np.sqrt((self.x - p.x)**2 + (self.y - p.y)**2)
    
    def toArray(self):
        return (self.x, self.y)
    
class Particle:
    p: Pos = Pos()
    a: int = 0 # Facing angle
    
    def __repr__(self):
        return f'Pos: {self.p}, angle: {self.a}'
    
    def __getattr__(self, a):
        if a == 'x': return self.p.x
        if a == 'y': return self.p.y
        
    def setPos(self, x, y):
        self.p.x = x
        self.p.y = y
        
        return self
        
    def random(self, size):
        self.p = Pos(*np.random.randint(0, size, 2))
        return self
        
    def applyAngle(self, a, weight=1):
        self.a = (a * weight + self.a) / 2
        
    def calcPos(self, weight=1):
        self.p.x += np.cos(self.a * np.pi / 180) * weight
        self.p.y += np.sin(self.a * np.pi / 180) * weight
        
        return self
        
    def toCoords(self):
        x = round(self.x)
        y = round(self.y)
        
        return (x, y)