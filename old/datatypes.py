from dataclasses import dataclass

import numpy as np

@dataclass
class Vector:
    u: int = 0
    v: int = 0
    
    def __repr__(self):
        return f'({self.u} {self.v})'
    
    def __getitem__(self, v):
        if 0 > v > 1: raise ValueError('Expected a number within [0, 1]')
        
        return self.v if v else self.u
    
    @staticmethod
    def angleToVector(angle, **kwargs):
        if 'forces' in kwargs.keys(): forces = kwargs['forces']
        elif 'forcex' and 'forcey' in kwargs.keys(): forces = (kwargs['forcex'], kwargs['forcey'])
        elif 'force' in kwargs.keys(): forces = (kwargs['force'], kwargs['force'])
        
        return Vector(np.cos(angle) * forces[0], np.sin(angle) * forces[1])
    
    def setWithAngle(self, angle, **kwargs):
        if 'forces' in kwargs.keys(): forces = kwargs['forces']
        elif 'forcex' and 'forcey' in kwargs.keys(): forces = (kwargs['forcex'], kwargs['forcey'])
        elif 'force' in kwargs.keys(): forces = (kwargs['force'], kwargs['force'])
        
        self.u = np.cos(angle) * forces[0]
        self.v = np.sin(angle) * forces[1]
        
        return self
    
    def __mul__(self, val):
        self.u *= val
        self.v *= val
        return self
        
    def __rmul__(self, val):
        self.u *= val
        self.v *= val
        return self
    
    def applyForce(self, v: 'Vector', dist=1):
        self.u += (v.u * dist)
        self.v += (v.v * dist)
    
@dataclass
class Pos:
    x: int = 0
    y: int = 0
    
    def __repr__(self):
        return f'{self.x}, {self.y}'
    
    def distanceBetween(self, p):
        return np.sqrt((self.x - p.x)**2 + (self.y - p.y)**2)
    
@dataclass    
class Particle:
    p: Pos = Pos()
    v: Vector = Vector() # velocity
    
    def __repr__(self):
        return f'Pos: {self.p} | Velocity: {self.v}'
    
    def __getattr__(self, a):
        if a == 'pos': return self.p
        if a == 'vel' or a == 'velocity': return self.v
        
        try:
            return getattr(self.p, a)
        except:
            try:
                return getattr(self.v, a)
            except:
                return AttributeError(a)
    
    def applyForce(self, v: Vector, dist=1, time=1):
        self.v.applyForce(v, dist)
        self.calcPos(time=time)
        
        return self
    
    def calcPos(self, time=1):
        self.p.x *= self.v.u * time
        self.p.y *= self.v.v * time
        
        return self
        
    def toCoords(self):
        x = round(self.p.x)
        y = round(self.p.y)
        
        return (x, y)