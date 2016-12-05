
# coding: utf-8

# In[7]:

import numpy as np
def read_value(file):
    text = file.readline()
    value = float(text[text.find(':')+1:len(text)])
    return value
        
def make_scene(filename):
    file = open(filename,'r')
    text = file.readline()
    Light = [float(text) for text in text[text.find(':')+1:len(text)].split(',')]
    ambient = read_value(file)
    diffuse_c = read_value(file)
    specular = read_value(file)
    specular_k = read_value(file)
    text = file.readline()
    depth_max =  int(text[text.find(':')+1:len(text)])
    text = file.readline()
    O = [float(text) for text in text[text.find(':')+1:len(text)].split(',')]
    text = file.readline()
    Q = [float(text) for text in text[text.find(':')+1:len(text)].split(',')]
    scene=[]
    text = file.readline()
    text = file.readline()
    position = [float(text) for text in text[text.find(':')+1:text.find(';')].split(',')]
    a = text.find(';')+1
    b = text[a:len(text)-1].find(';')+a
    color = [float(text) for text in text[a:b].split(',')]
    a = text[b+1:len(text)-1].find(';')+b
    normal = [float(text) for text in text[b+1:a].split(',')]
    b = text[a+2:len(text)-1].find(';')+a
    diffuse = float(text[a+2:b+2])
    a = text[b+2:len(text)-1].find(';')+b+2
    reflection = float(text[b+3:a+4])
    b = text[a+5:len(text)-1].find(';')+a+5
    specular_c = float(text[b+1:len(text)-1])
    scene.append({'object':'plane','position':np.array(position),'noor':np.array(normal),
                      'color':np.array(color),'diffuse':diffuse,'reflection':reflection, 'specular_c':specular_c})
    text = file.readline()   
    while True:
        text = file.readline()
        if (text!=''):
            position = [float(text) for text in text[text.find(':')+1:text.find(';')].split(',')]
            a=text.find(';')+1
            b=text[a:len(text)-1].find(';')+a
            radius = float(text[a:b])
            a=text[b+1:len(text)-1].find(';')+b
            color = [float(text) for text in text[b+1:a+1].split(',')]
            a = text[b+2:len(text)-1].find(';')+b+2
            reflection = float(text[a+1:len(text)-1])
            scene.append({'object':'sphere','position': np.array(position),'noor':radius, 'color':np.array(color),'reflection':0.2})
        if(text==''):   break
    return Light,ambient,diffuse_c,specular,specular_k,depth_max,O,Q,scene

Light,ambient,diffuse_c,specular,specular_k,depth_max,O,Q,scene = make_scene('data.txt')


# In[ ]:



