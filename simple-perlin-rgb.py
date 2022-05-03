import noise
from random import choice

def genart(size, scale, seeds, shifts=(0, 0, 0), mean_weights=(1, 1, 1), **kwargs):
    gsi = size
    gsc = scale

    # Create maps each corresponding to R G and B respectively
    rma, gma, bma = ([[
        noise.pnoise2(
            i/(gsc+shifts[n]), 
            j/(gsc+shifts[n]),
            int(seeds[n]/max(seeds) * 10)
           ) 
        for j in range(gsi)]
        for i in range(gsi)] for n in range(3))
    
    # Get each minimum values
    mrma, mgma, mbma = (-min([c for r in ma for c in r]) for ma in [rma, gma, bma])
    
    # Get each maximum values
    xrma, xgma, xbma = (max([c for r in ma for c in r]) for ma in [rma, gma, bma])

     # normnalize values between 0 and 1
    crma, cgma, cbma = ([[max(min((j / (xma + mma) + mma), 1), 0) for j in i] for i in ma] for \
        ma, mma, xma in zip([rma, gma, bma], [mrma, mgma, mbma], [xrma, xgma, xbma]))
    
    gd = choice([1])
    rc = choice([1, 0])
    gc = choice([1, 0])
    bc = choice([1, 0])
    
    return [[
        (abs(rc-r), 
         abs(gc-(g/gd)), 
         abs(bc-b))
        for r, g, b in zip(rr, gr, br)] for rr, gr, br in zip(crma, cgma, cbma)]
    
if __name__ == '__main__':
    print('Importing libraries')
    import matplotlib.pyplot as plt
    from random import choice, randint
    
    axes = []
    fig = plt.figure()
    
    print('Generating random numbers')
    r = range(1, 5)
    ran = [c for r in [[n] * r[-n] for n in r] for c in r]

    roc = choice(ran) - 0.5
    goc = choice(ran) - 0.5
    boc = choice(ran) - 0.5

    rse = randint(0, 1000)
    gse = randint(0, 1000)
    bse = randint(0, 1000)
    
    axes.append(fig.add_subplot(121))
    print('Generating first map')
    art1 = genart(size=1000, scale=100, seeds=(1, 1, 1), octaves=(roc, goc, boc))
    print('Plotting first map')
    plt.imshow(art1)
    
    axes.append(fig.add_subplot(122))
    print('Generating second map')
    art2 = genart(size=1000, scale=100, seeds=(rse, gse, bse), octaves=(roc, goc, boc), shifts=(1, 1, 1))
    print('Plotting second map')
    plt.imshow(art2)
    
    print('Showing...')
    plt.show()