# Art Generator

## Flowfield

Flowfield follows these 3 somewhat simple steps:
1. Generate a 2D map of arrays of floats between 0 and 1 of length 3
   - The first plot uses these values as RGB
2. Generate a velocity map using said values
   - The first value `a` corresponds to the angle: <img src='https://latex.codecogs.com/gif.latex?u_i,v_i=cos(a_i*360),%20sin(a_i*360)'>
3. Release particles across the borders and let them flow through the force field

You can visualise all 3 steps by running `flowfield.py`