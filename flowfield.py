import numpy as np
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise

from datatypes import Vector, Particle, Pos
from copy import copy

def tdperlin(octaves, seeds):
    rpn = PerlinNoise(octaves=octaves[0], seed=seeds[0])
    gpn = PerlinNoise(octaves=octaves[1], seed=seeds[1])
    bpn = PerlinNoise(octaves=octaves[2], seed=seeds[2])

    gsi = 100

    rma, gma, bma = ([[pn([i/gsi, j/gsi]) for j in range(gsi)] for i in range(gsi)] for pn in [rpn, gpn, bpn]) # Create maps each corresponding to R G and B respectively
    mrma, mgma, mbma = (-min([c for r in ma for c in r]) for ma in [rma, gma, bma]) # Get each minimum values
    xrma, xgma, xbma = (max([c for r in ma for c in r]) for ma in [rma, gma, bma]) # Get each maximum values

    crma, cgma, cbma = ([[max(min((j / (xma + mma) + mma), 1), 0) for j in i] for i in ma] for ma, mma, xma in zip([rma, gma, bma], [mrma, mgma, mbma], [xrma, xgma, xbma])) # normnalize values between 0 and 1
    
    return [[(r, g, b) for r, g, b in zip(rr, gr, br)] for rr, gr, br in zip(crma, cgma, cbma)]

class VelocityMap:
    vmap: np.array = np.array([])
    
    def __init__(self, precision=None):
        self.precision = precision
        
    def generateVMap(self, size=None, **kwargs):
        if 'concatenatedArray' in kwargs.keys():
            aConc = kwargs['concatenatedArray']
            aConc = np.array(aConc) if type(aConc) != np.array else aConc
            
            if not size: size = (len(aConc[0]), len(aConc))
            vmap = np.array([np.array([Vector().setWithAngle(angle=aConc[y][x][0], forces=(1, 1)) for x in range(size[0])]) for y in range(size[1])])
            
            self.vmap = vmap
            
            return vmap
        
        else:
            raise AttributeError()

    def __repr__(self):
        return self.vmap.__repr__()

class Flowfield:
    ffmap: np.array = np.array([])
    
    def generateFlowfield(self, vectorMap, size, density, particles: list[Particle]=[], particle: Particle=None, influenced=lambda x: x < 20):
        ffmap = np.zeros((size, size))
        amntPer = int(size * density)
        vectorCoords = np.array([np.array([Pos(x, y) for x in range(amntPer, size, amntPer)]) for y in range(amntPer, size, amntPer)])
        
        ffmap[particle.x, particle.y] = 1
        
        iteration = 0
        
        while particle.x < size and particle.y < size and iteration < 10:
            for crow, vrow in zip(vectorCoords, vectorMap):
                for coords, vec in zip(crow, vrow):
                    dist = coords.distanceBetween(particle.p)
                    
                    if influenced(dist):
                        vc = copy(vec)
                        particle.applyForce(vc, dist=dist)
                   
            if influenced(dist):
                particle.roundPos()
                ffmap[particle.p.x, particle.p.y] = 1
        
            iteration += 1
            
        self.ffmap = ffmap
        
        return ffmap
        
    
if __name__ == '__main__':
    density = 0.01
    size = 100
    amntPer = int(size * density)
    fig = plt.figure()
    axes = []

    ### RGB Visual
    r = np.random.randint(0, 1000, 3)
    concArray = tdperlin((1.5, 1.5, 2.5), r)
    axes.append(fig.add_subplot(131))
    axes[-1].set_title(str(r))
    plt.imshow(concArray, origin='lower')

    ### Vector map
    vmap = VelocityMap()
    normalizedConcArray = np.array([[(360 * concArray[j][i][0], concArray[j][i][1]-0.5, concArray[j][i][2]-0.5) for i in range(amntPer, len(concArray[0]), amntPer)] for j in range(amntPer, len(concArray), amntPer)])
    vmap.generateVMap(concatenatedArray=normalizedConcArray)
    axes.append(fig.add_subplot(132))
    plt.quiver([[j for j in range(amntPer, size, amntPer)] for i in range(amntPer, size, amntPer)], [[i for j in range(amntPer, size, amntPer)] for i in range(amntPer, size, amntPer)], [[v[0] for v in x] for x in vmap.vmap], [[v[1] for v in x] for x in vmap.vmap], scale=30)

    ### Flow field map
    ffmap = Flowfield()
    particle = Particle(p=Pos(50, 50))
    ffmap.generateFlowfield(vmap.vmap, size, density, particle=particle)
    axes.append(fig.add_subplot(133))
    plt.imshow(ffmap.ffmap, cmap='Greys')

    plt.show()