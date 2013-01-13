import json, sys
from node_lib import *
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import numpy
from scipy import misc

print 'Node image tools (core) v01a'

# Read node file *.json
file_node=sys.argv[1] #file read 'composite.json'
with open(file_node) as jdf:
    data_io = json.load(jdf)

# Bringing format node to object type and sort by ID
G = graph
sorted_names=sorted(data_io, key=lambda x : data_io[x]['id'])

cached={} #create cached list

for _name in sorted_names:
    node = G(data_io[_name]) #list[properties] to node.properties

    if (node.type=='read'):
        img = Image.open(node.file)
        width, height = img.size
        cached[node.name] = numpy.array(img)
        print 'cached->', node.file,'(',width, height,')'

    if (node.type=='cc'):
        cached[node.name]=CC_(cached[node.link],node.bright,node.contrast)

    if (node.type=='size'):
        cached[node.name]=size_(cached[node.link],node.size,width,height)

    if (node.type=='rotate'):
        cached[node.name]=rotate_(cached[node.link],node.angle)

    if (node.type=='composite'):
        cached[node.name]=composite_(cached[node.link_a],cached[node.link_b],node.job)

    if (node.type=='blur'):
        cached[node.name]=blur_(cached[node.link],node.size)

    if (node.type=='sharpen'):
        cached[node.name]=sharpen_(cached[node.link],node.size)

    if (node.type=='write'):
        out_img = Image.fromarray(cached[node.link])
        out_img.save(node.file)
        print 'write->', node.file
