import matplotlib.pyplot as plt
from threading import Thread

from matplotlib.figure import Figure
from matplotlib import animation

from pytest import PytestAssertRewriteWarning
from genart import genart
from random import choice, randint

import datetime

fig = plt.figure()
threads = []
axes = []
gens = []
gens2 = []

def gen():
    global gens
    
    r = range(1, 5)
    ran = [c for r in [[n] * r[-n] for n in r] for c in r]

    roc = choice(ran) - 0.5
    goc = choice(ran) - 0.5
    boc = choice(ran) - 0.5

    rse = randint(0, 1000)
    gse = randint(0, 1000)
    bse = randint(0, 1000)

    gen_ = genart((roc, goc, boc), (rse, gse, bse))
    gens.append((gen_, (roc, goc, boc), (rse, gse, bse)))
    return gen_

def genp():
    return
    
def normalize(v, x, m=0):
    return (v - m) / (x - m)

def multiple(w, h, info=False):
    t = 0
    for a in range(w*h):
        print(f'Started {a+1}th of {w*h} thread', end='\r')
        threads.append(Thread(target=gen, daemon=True))
        threads[-1].start()
        
    print()
    while any(thread.is_alive() for thread in threads):
        print('Calculating', end='\r')
        
    print('\nPlotting')
    for i, ge in enumerate(gens):
        axes.append(fig.add_subplot(w, h, i+1))
        
        if info:
            axes[-1].set_title(f'{i+1} {ge[1]} {ge[2]}', fontsize=6, pad=2)
            plt.xticks([])
            plt.yticks([])
            
        plt.imshow(ge[0])

    plt.show()
    
    
def single():
    print(f'Calculating', end='\r')
    p = gen()
    plt.imshow(p)
    
    plt.show()    
        
def shift():
    pass
        
class Anim:
    init = []
    
    def __init__(self):
        axes = []
        fig = plt.figure()
        
        r = range(1, 5)
        ran = [c for r in [[n] * r[-n] for n in r] for c in r]

        roc = choice(ran) - 0.5
        goc = choice(ran) - 0.5
        boc = choice(ran) - 0.5

        rse = randint(0, 1000)
        gse = randint(0, 1000)
        bse = randint(0, 1000)
        
        axes.append(fig.add_subplot(121))
        plt.imshow(genart(size=1000, scale=100, seeds=(rse, gse, bse), octaves=(roc, goc, boc)))
        
        axes.append(fig.add_subplot(122))
        plt.imshow(genart(size=1000, scale=100, seeds=(rse, gse, bse), octaves=(roc, goc, boc), shifts=(100, 0, 0)))
        plt.show()
        
        now = datetime.datetime.now()
        params = (
            (
                now.second
            )
        )
        
        self.frame = self.ax.imshow(genart(*params), interpolation="none", cmap="gist_ncar", animated=True)
    
    def updatefig(self):
        self.frame
    
if __name__ == '__main__':
    multiple(5, 5, True)
    