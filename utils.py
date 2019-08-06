import os
import numpy as np
import matplotlib.pyplot as plt


def normalize(x):
    """Function for normalization of vector x
       Returns a normalized vector"""
    x /= np.linalg.norm(x)
    return x


def ray_intersects(objectType, position, normal, startPoint, directionPoint):
    """
    Function which detect ray intersections with the object of the scene
    
    :param objectType: the type of object in our program is either a sphere or a plane
    :param position: depending on the object either the radius vector (the plane),
                  or the position in three-dimensional space (sphere)
    :param normal: depending on the object is either normal (plane) or radius (sphere)
    :param startPoint: startpoint of the ray
    :param directionPoint: direction of the ray
    
    :return: the point of intersection with the ray
    """
    if objectType == 'plane':
        normal = normal
        radiusVector = position
        cosA = np.dot(directionPoint, normal)
        if np.abs(cosA) < 1e-6:
            return np.inf
        d = np.dot(radiusVector - startPoint, normal) / cosA
        if d < 0:
            return np.inf
        return d
    elif objectType == 'sphere':
        position = position
        radius = normal
        a = np.dot(directionPoint, directionPoint)
        startPosition = startPoint - position
        b = 2 * np.dot(directionPoint, startPosition)
        c = np.dot(startPosition, startPosition) - radius * radius
        disc = b * b - 4 * a * c
        if (disc > 0):
            distSqrt = np.sqrt(disc)
            q = (-b - distSqrt) / 2.0 if b < 0 else (-b + distSqrt) / 2.0
            t0 = q / a
            t1 = c / q
            t0, t1 = min(t0, t1), max(t0, t1)
            if t1 >= 0:
                return t1 if t0 < 0 else t0
    else:
        raise Assertionerror('Wrong object type')
    return np.inf


def normal(obj, M):
    """
    Function, which returns normal of object
    :param obj: object of the scene
    :param M: point of intersection
    """
    if obj.get('object') == 'sphere':
        N = normalize(M - obj.get('position'))
    elif obj.get('object') == 'plane':
        N = obj.get('noor')
    return N


def tracing(startPoint, directionPoint, data, color_light):
    """"
    A function that finds the closest object that intersects 
    with the ray, checks whether in the shadow of the object 
    and other objects and adds the color of the light intensity 
    according to the Lambert and Phong models.
    
    :param startPoint: startpoint of the ray
    :param directionPoint: direction of the ray
    :param scene: three-dimensional scene
    
    :return: the closest object that intersects with the ray, 
             the point of intersection, 
             the object and the normal color
    """
    L, ambient, diffuse_c, specular_c, specular_k, depth_max, O, Q, scene = data
    t = np.inf
    n = len(scene)
    for i in range(n):
        distance = ray_intersects(scene[i].get('object'),
                                  scene[i].get('position'),
                                  scene[i].get('noor'),
                                  startPoint,
                                  directionPoint)
        if distance < t:
            t, index = distance, i
    if t == np.inf:
        return
    obj = scene[index]
    M = startPoint + directionPoint * t
    N = normal(obj, M)
    color = obj.get('color')
    directionL = normalize(L - M)
    directionO = normalize(O - M)
    l = [ray_intersects(scene[i].get('object'),
                        scene[i].get('position'),
                        scene[i].get('noor'),
                        M + N * .0001,
                        directionL) 
         for k in range(n) if k != index]
    if l and min(l) < np.inf:
        return
    col_ray = ambient
    col_ray += obj.get('diffuse',1.0) * max(np.dot(N, directionL), 0) * color
    sp_c = obj.get('specular_c', specular_c)
    y = max(np.dot(N, normalize(directionL + directionO)), 0)
    col_ray += sp_c*y**specular_k*color_light
    return obj, M, N, col_ray


def make_3Dimage(filename, w, h, s_filename):
    """
    The function cretes and save image
    :param filename: the name of text file that contains information 
                     about the objects in the scene
    :param w: the width of the image
    :param h: the height of the image
    """
   
    data = make_scene(filename)
    L, ambient, diffuse_c, specular_c, specular_k, depth_max, O, Q, scene = data
    L, O, Q = np.array(L), np.array(O), np.array(Q)
    color_light = np.ones(3)
    col = np.zeros(3) 
    img = np.zeros((h, w, 3))
    for i, x in enumerate(np.linspace(-1, 1, w)):
        for j, y in enumerate(np.linspace(-1, 1, h)):
            col = np.zeros(3) 
            Q[:2] = (x, y)
            D = normalize(Q - O)
            depth = 0
            rayO, rayD = O, D
            reflection = 1.
            while depth < depth_max:
                traced = tracing(rayO, rayD, data, color_light)
                if not traced:
                    break
                obj, M, N, col_ray = traced
                rayO, rayD = M + N * .0001, normalize(rayD - 2 * np.dot(rayD, N) * N)
                depth += 1
                col += reflection * col_ray
                reflection *= obj.get('reflection', 1.)
            img[h - j - 1, i, :] = np.clip(col, 0, 1)
    plt.imsave(s_filename, img)

    
def read_value(file):
    text = file.readline()
    value = float(text[text.find(':')+1:len(text)])
    return value


def make_scene(filename):
    file = open(filename,'r')
    text = file.readline()
    Light = [float(text) 
             for text in text[text.find(':')+1:len(text)].split(',')]
    ambient = read_value(file)
    diffuse_c = read_value(file)
    specular = read_value(file)
    specular_k = read_value(file)
    text = file.readline()
    depth_max =  int(text[text.find(':')+1:len(text)])
    text = file.readline()
    O = [float(text) 
         for text in text[text.find(':')+1:len(text)].split(',')]
    text = file.readline()
    Q = [float(text) 
         for text in text[text.find(':')+1:len(text)].split(',')]
    scene=[]
    text = file.readline()
    text = file.readline()
    position = [float(text) 
                for text in text[text.find(':')+1:text.find(';')].split(',')]
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
    scene.append({'object':'plane',
                  'position':np.array(position),
                  'noor':np.array(normal),
                  'color':np.array(color),
                  'diffuse':diffuse,
                  'reflection':reflection,
                  'specular_c':specular_c})
    text = file.readline()   
    while True:
        text = file.readline()
        if (text!=''):
            position = [float(text) 
                        for text in text[text.find(':')+1:text.find(';')].split(',')]
            a=text.find(';')+1
            b=text[a:len(text)-1].find(';')+a
            radius = float(text[a:b])
            a=text[b+1:len(text)-1].find(';')+b
            color = [float(text) for text in text[b+1:a+1].split(',')]
            a = text[b+2:len(text)-1].find(';')+b+2
            reflection = float(text[a+1:len(text)-1])
            scene.append({'object':'sphere',
                          'position': np.array(position),
                          'noor':radius,
                          'color':np.array(color),
                          'reflection':0.2})
        if text == '':
            break
    data = [Light, ambient, diffuse_c,
           specular, specular_k, depth_max,
           O, Q, scene]
    return data