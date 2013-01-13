from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import numpy
from scipy import misc

# node graph
class graph(dict):
    def __init__(self, *args, **kwds):
        super(graph, self).__init__(*args, **kwds)
        self.__dict__ = self

# node composite
def composite_(cached_a,cached_b,job):
    if (job=='plus'):
        out=cached_a+cached_b
    if (job=='minus'):
        out=cached_a-cached_b
    if (job=='multiply'):
        out=cached_a*cached_b
    print '->composite',job
    return out;

# node size
def size_(cached,size,w,h):
    if (size>0):
        S= int(round(h*size)), int(round(w*size))
        out=misc.imresize(cached,S,'bilinear','RGB')
    if (size<0):
        S= int(round(h/abs(size))),int(round(w/abs(size)))
        out=misc.imresize(cached,S,'bilinear','RGB')
    print '->size',S
    return out;

# node Color Correct (CC)
def CC_(cached,bright,contrast):
    out_cc = Image.fromarray(cached)
    enhancer = ImageEnhance.Brightness(out_cc) # Brightness
    out_cc = enhancer.enhance(bright)
    enhancer = ImageEnhance.Contrast(out_cc) # Contrast
    out = numpy.array(enhancer.enhance(contrast))
    print '->Color Correct: bright=',bright,' contrast=',contrast
    return out;

# node rotate
def rotate_(cached,angle):
    out=misc.imrotate(cached,angle,'bilinear')
    print '->rotate',angle
    return out;

# node blur
def blur_(cached,size):
    out=cached
    for k in range(size):
        out=misc.imfilter(out,'blur')
        print '.',
    print '->blur'
    return out;

# node sharpen
def sharpen_(cached,size):
    out=cached
    for k in range(size):
        out=misc.imfilter(out,'sharpen')
        print '.',
    print '->sharpen'
    return out;

