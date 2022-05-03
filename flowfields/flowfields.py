import numpy as np
import matplotlib.pyplot as plt

from perlin_noise import PerlinNoise

import json, os, sys, typing

from datatypes import Particle, Pos

try:
    from alive_progress import alive_bar
    __bar = True
except:
    __bar = False
    

def tdperlin(size: int, octaves: typing.Union[int, tuple, list], seeds: typing.Union[int, tuple, list]):
    if len(octaves) != len(seeds): 
        raise ValueError(f'Parameters "octaves" and "seeds" must be of same length')
    length = len(octaves)    
        
    pns = [PerlinNoise(octaves=octaves[i], seed=seeds[i]) for i in range(length)]
    maps = [[np.array([pn([i/size, j/size]) for j in range(size)]) for i in range(size)] for pn in pns]
    
    mins = (-min([val for row in _map for val in row]) for _map in maps)
    maxes = (max([val for row in _map for val in row]) for _map in maps)
    
    normalized = [[(row - np.min(_map)) / (np.max(_map) - np.min(_map)) for row in _map] for _map, _min, _max in zip(maps, mins, maxes)]
    
    return [[vals if length > 1 else vals[0] for vals in zip(*rows)] for rows in zip(*normalized)]
    
class Flowfields:
    def __init__(self, arr: list[list], density, precision=0.1):
        self.size = len(arr)
        self.amntPer = int(self.size * density)
        angleMap = Flowfields.generateAngleMap(fromArray=arr, amntPer=self.amntPer)
        self.oldAmap = angleMap
        angleCaster = Flowfields.generateAngleMap(np.full((size, size), 0), amntPer=self.amntPer)
        self.amap = Flowfields.castAngleMap(angleMap, angleCaster, weight=2)
        self.aposmap = np.array([np.array([Pos(x, y) for x in range(self.amntPer, self.size, self.amntPer)]) for y in range(self.amntPer, self.size, self.amntPer)])
        self.precision = precision
    
    @staticmethod
    def generateAngleMap(fromArray, amntPer, size=None):
        if not size: size = len(fromArray)
        return np.array([np.array([fromArray[y][x] * 360 for x in range(amntPer, size, amntPer)]) for y in range(amntPer, size, amntPer)])
    
    @staticmethod
    def castAngleMap(angleMap1, angleMap2, weight=1):
        return np.average(np.array([angleMap1, angleMap2]), axis=0, weights=[1, weight])
    
    def drawParticle(self, particle: Particle, maxIterations=np.inf, separateXY=False, scaledSize=None):
        size = scaledSize if scaledSize else self.size
        
        iteration = 0
        path =  []
        pathx = []
        pathy = []
        
        while particle.x < size > particle.y and iteration < maxIterations:
            for crow, arow in zip(self.aposmap, self.amap):
                for pos, ang in zip(crow, arow):
                    dist = particle.p.distanceBetween(pos)
                    particle.applyAngle(ang, weight=(142 - dist) / 142)
                    particle.calcPos(self.precision)
            
            particleCoords = particle.toCoords()
            
            if separateXY:
                pathx.append(particleCoords[0])
                pathy.append(particleCoords[1])
                
            else:    
                path.append(particle.toCoords())
                    
            iteration += 1
            
        return np.array(pathx), np.array(pathy) if separateXY else np.array(path)
            
        
if __name__ == '__main__':
    size = 100 # Canvas size
    aDensity = 0.1 # Force vectors density (size * aDensity)
    amntAPer = int(size * aDensity) # Amount of force vectors 
    channels = 1 # Amount of channels for the initial perlin noise image generation
    lineRateScale = 0.5 # Amount of lines drawn on the final canvas (used as the step argument in range(0, size, lineRateScale))
    
    fig = plt.figure()
    axes = []
    
    ### Initial noise
    hasCache = False
    
    # TODO fix bugs that most likely exist
    with open('cache.json', 'r') as f:
        if '--useCache' in sys.argv:
            data = json.loads(f.read())
            cached = data.get('cached', [])
            
            for cache in cached:
                if cache.get('map', None) and cache.get('size', None) == size and not '--newCache' in sys.argv:
                    print('Using cached noise map')
                    hasCache = True
                    initNoiseMap = cache['map']
                    break
            
    if not hasCache:
        print('Generating noise map')
        r = np.random.randint(0, 1000, channels)
        initNoiseMap = tdperlin(size, (1.5,) * channels, r)
        
        with open('cache.json', 'w') as f:
            if not data.get('cached', None):
                data['cached'] = []
            data['cached'].append({'size': size, 'map': initNoiseMap})
            json.dump(data, f)
            print('Cached map')
    
    axes.append(fig.add_subplot(141))
    plt.imshow(initNoiseMap, origin='lower')
    
    ## Flow field
    ff = Flowfields(initNoiseMap, aDensity)
    
    ### Angle map
    print('Generating angle map')
    axes.append(fig.add_subplot(142))
    axes[-1].set_aspect('equal')
    plt.quiver(
        [[j for j in range(amntAPer, size, amntAPer)] for i in range(amntAPer, size, amntAPer)], 
        [[i for j in range(amntAPer, size, amntAPer)] for i in range(amntAPer, size, amntAPer)], 
        [[np.cos(v * np.pi / 180) for v in x] for x in ff.oldAmap], 
        [[np.sin(v * np.pi / 180) for v in x] for x in ff.oldAmap], 
        scale=30
    )
    
    axes.append(fig.add_subplot(143))
    axes[-1].set_aspect('equal')
    plt.quiver(
        [[j for j in range(amntAPer, size, amntAPer)] for i in range(amntAPer, size, amntAPer)], 
        [[i for j in range(amntAPer, size, amntAPer)] for i in range(amntAPer, size, amntAPer)], 
        [[np.cos(v * np.pi / 180) for v in x] for x in ff.amap], 
        [[np.sin(v * np.pi / 180) for v in x] for x in ff.amap], 
        scale=30
    )
    
    ### Flow field map
    print('Drawing lines')
    axes.append(fig.add_subplot(144))
    axes[-1].set_aspect('equal')
    
    scaledSize = size
    
    if lineRateScale < 1:
        scaledSize = int(size / lineRateScale)
        lineRateScale = 1
    
    dPosmap = np.array([np.array([(x, y) for x in range(0, scaledSize, lineRateScale)]) for y in range(0, scaledSize, lineRateScale)])
    edgeCoordinates = np.concatenate([dPosmap[0,:-1], dPosmap[:-1,-1], dPosmap[-1,::-1], dPosmap[-2:0:-1,0]])
    
    def lineStep(coords):
        pathx, pathy = ff.drawParticle(Particle().setPos(*coords), maxIterations=100, scaledSize=scaledSize, separateXY=True)
        pathx[pathx < 0] = 0
        pathy[pathy < 0] = 0
        return pathx, pathy
    
    if __bar:
        with alive_bar(len(edgeCoordinates)) as bar:
            for i, edge in enumerate(edgeCoordinates):
                plt.plot(*lineStep(edge), str(i / len(edgeCoordinates)), linewidth=0.5)
                bar()
                
    else: # yes i know this isn't the cleanest way of doing things
        for i, edge in enumerate(edgeCoordinates):
            plt.plot(*lineStep(edge), str(i / len(edgeCoordinates)), linewidth=0.5)
    
    plt.show()