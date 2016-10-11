""" TODO: Put your header comment here """

from math import *
import random
from PIL import Image


def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    func_list = ["prod","avg","cos_pi","sin_pi","x","y","ycos_10","xcos_10"]
    index = random.randint(0,len(func_list)-1)
    func = func_list[index]

    if min_depth > 1:
        depth = random.randint(min_depth,max_depth)
        func2 = build_random_function(depth-1,depth-1)
        return [func,func2,func2]
    else:
        return [func]


def evaluate_random_function(f, a, b):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
        >>> evaluate_random_function(['cos_pi',['cos_pi'],['cos_pi']],.5,.5)
        1.0
        >>> evaluate_random_function(['sin_pi',['x',['avg',['prod'],['prod']],['avg',['prod'],['prod']]],['x',['avg',['prod'],['prod']],['avg',['prod'],['prod']]]],0,0)
        0.0
    """
    res = 0
    if len(f)>1:
        res1 = evaluate_random_function(f[1],a,b)
        res2 = evaluate_random_function(f[2],a,b)
        f = [f[0]]
        a = res1
        b = res2

    if f==["prod"]:
        res = a*b
    elif f==["avg"]:
        res =  0.5*(a+b)
    elif f==["cos_pi"]:
        res = cos(pi*a)
    elif f==["sin_pi"]:
        res = sin(pi*a)
    elif f==["x"]:
        res = a
    elif f==["y"]:
        res = b
    elif f==["ycos_10"]:
        res = cos(10*b)
    elif f==["xcos_10"]:
        res = cos(10*a)
    return res

    # Notes: including abs(a) and e^(a-1) got a plaid pattern. I want more rotationally symmetric
    # things, so I think I need to apply the functions to both a and b


def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    res = output_interval_start+(1.0*(val-input_interval_start)*(output_interval_end-output_interval_start)/(input_interval_end-input_interval_start))
    return res


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


### Ignore this, was used for testing
def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)
###

def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(7,9) #["x"]
    green_function = build_random_function(7,9) #["y"]
    blue_function = build_random_function(7,9) #["x"]

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    generate_art("test6.png")
    # test_image("noise.png")
