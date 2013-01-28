import Image
import ImageDraw
import ImageFilter
import ImageEnhance
import numpy
from scipy import misc

# node graph
class graph(dict):
    def __init__(self, *args, **kwds):
        super(graph, self).__init__(*args, **kwds)
        self.__dict__ = self

# node composite
def composite_(cached_a,cached_b,mask,job):
    if (job=='mask'):
        aCom = Image.fromarray(cached_a)
        bCom = Image.fromarray(cached_b)
        iMask = Image.fromarray(mask)
        out = numpy.array(Image.composite(aCom, bCom, iMask))
    if (job=='plus'):
        out=cached_a+cached_b
    if (job=='minus'):
        out=cached_a-cached_b
    if (job=='multiply'):
        out=cached_a*cached_b
    if (job=='over'):
        aCom = Image.fromarray(cached_a)
        bCom = Image.fromarray(cached_b)
        try:
            alphaData = aCom.tostring("raw", "A")
            alpha = Image.fromstring("L", aCom.size, alphaData)
        except:
            print '->Error. No alpha data. Alpha=Constant(130)'
            alpha = Image.new("L", aCom.size,130)  
        out = numpy.array(Image.composite(aCom, bCom, alpha))
    print '->Composite',job
    return out;

# node size
def size_(cached,size,w,h):
    if (size>0):
        S= int(round(h*size)), int(round(w*size))
        out=misc.imresize(cached,S,'bilinear','RGB')
    if (size<0):
        S= int(round(h/abs(size))),int(round(w/abs(size)))
        out=misc.imresize(cached,S,'bilinear','RGB')
    print '->Size',S
    return out;

# node Color Correct (CC)
def CC_(cached,bright,contrast):
    out_cc = Image.fromarray(cached)
    enhancer = ImageEnhance.Brightness(out_cc) # Brightness
    out_cc = enhancer.enhance(bright)
    enhancer = ImageEnhance.Contrast(out_cc) # Contrast
    out = numpy.array(enhancer.enhance(contrast))
    print '->Color correct: bright=',bright,' contrast=',contrast
    return out;

# node rotate
def rotate_(cached,angle):
    out=misc.imrotate(cached,angle,'bilinear')
    print '->Rotate',angle
    return out;

# node blur
def blur_(cached,size):
    from scipy import ndimage
    r = cached[:, :, 0]
    g = cached[:, :, 1]
    b = cached[:, :, 2]
    r = ndimage.gaussian_filter(r,order=0, sigma=size)
    g = ndimage.gaussian_filter(g,order=0, sigma=size)
    b = ndimage.gaussian_filter(b,order=0, sigma=size)
    cached=numpy.dstack((r, g, b))
    print '->Blur',size
    return cached;

# node sharpen
def sharpen_(cached,size):
    for k in range(size):
        cached=misc.imfilter(cached,'sharpen')
        print '.',
    print '->Sharpen',size
    return cached;

# node gradient
def gradient_(width,height):
    im = Image.new("L", (1, height))
    draw = ImageDraw.Draw(im)
    for l in xrange(height):
        G=255 * l/height
        colour = (G)
        draw.line((0, l, height, l), fill=colour)
    im=im.resize((width, height), Image.NEAREST)
    out = numpy.array(im)
    del draw
    print '->Gradient: width=',width,' height=',height
    return out;

# node invert
def invert_ (cached):
    from PIL import ImageChops
    out = numpy.array(ImageChops.invert(Image.fromarray(cached)))
    print '->Invert'
    return out;
    
    


