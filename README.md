# Art Generator

## Flowfield

Flowfield follows these 3 somewhat simple steps:
1. Generate a 2D map of arrays of floats between 0 and 1 of length 3
   - The first plot uses these values as RGB
2. Generate a velocity map using said values
   - The first value `a` corresponds to the angle: <img src='https://latex.codecogs.com/gif.latex?u_i,v_i=cos(a_i*360),%20sin(a_i*360)'>
   - It is casted to another angle map pointing in a single direction to make the final product more harmonious
3. Release particles across the borders and let them flow through the force field
   - Keep in mind, the example code uses matplotlib.pyplot, which is tremendously slow. I'm working on a Processing version, which will be way faster.

You can visualise all 3 steps by running flowfield.py
```
python3 flowfields.py [--useCache, --newCache]
```
`--useCache`: Use a JSON cache for the first map as it can take quite a long time depending on what size it is
`--newCache`: Delete the old cache and generate a new one (if `--useCache` is specified)
