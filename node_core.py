import json, sys
from node_lib import *
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import numpy
from scipy import misc

print '\nNode image tools (core) v01a\n'

# Read node file *.json
try:
    file_node=sys.argv[1]
except:
    print '->Error. No script'
    sys.exit (0)
    
with open(file_node) as jdf:
    data_io = json.load(jdf)

# Bringing format node to object type and sort by ID
G = graph
sorted_names=sorted(data_io, key=lambda x : data_io[x]['id'])

cached={} #create cached list

for _name in sorted_names:
    node = G(data_io[_name]) #list[properties] to node.properties

    if (node.type=='read'):
        try:
            img = Image.open(node.file)
        except:
            print '->Error. No such file', node.file
            sys.exit (0)        
        width, height = img.size
        cached[node.name] = numpy.array(img)
        print 'cached->', node.file,'(',width, height,')'

    if (node.type=='cc'):
        cached[node.name]=CC_(cached[node.link],node.bright,node.contrast)

    if (node.type=='size'):
        cached[node.name]=size_(cached[node.link],node.size,width,height)

    if (node.type=='rotate'):
        cached[node.name]=rotate_(cached[node.link],node.angle)

    if (node.type=='gradient'):
        cached[node.name]=gradient_(node.width,node.height)

    if (node.type=='composite'):
        if(node.job!='mask'):
            cached[node.name]=composite_(cached[node.link_a],cached[node.link_b],
            0,node.job)
        if(node.job=='mask'):
            cached[node.name]=composite_(cached[node.link_a],cached[node.link_b],
            cached[node.mask],node.job)

    if (node.type=='blur'):
        cached[node.name]=blur_(cached[node.link],node.size)

    if (node.type=='sharpen'):
        cached[node.name]=sharpen_(cached[node.link],node.size)

    if (node.type=='view'):
        view_img = Image.fromarray(cached[node.link])
        view_img.show()

    if (node.type=='write'):
        out_img = Image.fromarray(cached[node.link])
        out_img.save(node.file)
        print 'write->', node.file

print '\nScript:',file_node,'completed'
