# commands: q - Quit, s - Save script, l - Load script, e - Execute script
# p - Print script, d - Delete node in script, g - render script as Graph

import json
import os

print 'Node image tools (writer) v01a\n'
print 'q - Quit, s - Save script, l - Load script, e - Execute script,'
print 'p - Print script, d - Delete node in script, g - render script as Graph\n'

_instruction='i'
id=1
script={} #declaration node script

while (_instruction!='q'):
    _instruction=raw_input('Instruction:')
    # Node 'Read'
    if (_instruction=='read'):
        node_name=raw_input('-> node name:')
        file_name=raw_input('-> file name:')
        N_root='node'+str(id)
        script[N_root]={'name':node_name,'type':'read',
                        'file':file_name,'id':id}
        id+=1
    # Node 'Write'
    if (_instruction=='write'):
        node_name=raw_input('-> node name:')
        link_name=raw_input('-> link name:')
        file_name=raw_input('-> file name:')
        N_root='node'+str(id)
        script[N_root]={'name':node_name,'type':'write','link':link_name,
                        'file':file_name,'id':id}
        id+=1
    # Node 'Blur'
    if (_instruction=='blur'):
        node_name=raw_input('-> node name:')
        link_name=raw_input('-> link name:')
        size=int(raw_input('-> size:'))
        N_root='node'+str(id)
        script[N_root]={'name':node_name,'type':'blur','link':link_name,
                        'size':size,'id':id}
        id+=1
    # Node 'Invert'
    if (_instruction=='invert'):
        node_name=raw_input('-> node name:')
        link_name=raw_input('-> link name:')
        N_root='node'+str(id)
        script[N_root]={'name':node_name,'type':'invert','link':link_name,
                        'id':id}
        id+=1
    # Script save
    if (_instruction=='s'):
        S_name=raw_input('-> save script name:')
        with open(S_name, 'wb') as outfile:
          json.dump(script, outfile)
        print 'Scrpt save to',S_name
    # Script load
    if (_instruction=='l'):
        S_name=raw_input('-> load script name:')
        with open(S_name) as jdf:
            script = json.load(jdf)
        print 'Load Scrpt:',S_name
    # Print script
    if (_instruction=='p'):
        print 'script:\n',json.dumps(script,sort_keys=True, indent=2)    
    # Render script as graph
    if (_instruction=='g'):
        G_name=raw_input('-> render script name:')
        os.system(r'node_graph.py '+G_name)
    # Delete node
    if (_instruction=='d'):
        del_node=raw_input('-> del node name:')
        for i in script.keys():
            if (script[i]['name']==del_node):
                print 'del:',script[i]['name']
                del script[i]
    # Execute script
    if (_instruction=='e'):
        E_name=raw_input('-> execute script name:')
        os.system(r'node_core.py '+E_name)
print 'quit'
