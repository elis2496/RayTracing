
# coding: utf-8

# In[13]:

import readfile2
import numpy as np
import matplotlib.pyplot as plt

"""The main function takes as input:
    filename - the name of text file that contains information about the objects in the scene
    w - the width of the image
    h - the length of the image
    Make and save imagine"""
def normalize(x):
    """Function for normalization of vector x
    Returns a normalized vector"""
    x /= np.linalg.norm(x)
    return x

def ray_intersects(objectType,parameter1, parameter2, startPoint,directionPoint):
    """Function which detect ray intersections with the object of the scene
        objectType - the type of object in our program is either a sphere or a plane
        parameter1 - depending on the object either the radius vector (the plane), or the position in three-dimensional space (sphere)
        parameter2 - depending on the object is either normal (plane) or radius (sphere)
        startPoint - startpoint of the ray
        directionPoint - direction of the ray
        Returns the point of intersection with the ray"""
    if(objectType=='plane'):
        normal=parameter2
        radiusVector=parameter1
        cosA = np.dot(directionPoint, normal)
        if np.abs(cosA) < 1e-6:
            return np.inf
        d = np.dot(radiusVector - startPoint, normal) / cosA
        if d < 0:
            return np.inf
        return d
    if(objectType=='sphere'):
        position=parameter1
        radius=parameter2
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
    return np.inf

def normal(obj, M):
    """Function, which returns normal of object
        obj - object of the scene
        M - point of intersection"""
    if obj.get('object') == 'sphere':
        N = normalize(M - obj.get('position'))
    elif obj.get('object') == 'plane':
        N = obj.get('noor')
    return N
       

def tracing(startPoint, directionPoint,scene):
        """"
        A function that finds the closest object that intersects with the ray, checks whether in the shadow of the object 
        and other objects and adds the color of the light intensity according to the Lambert and Phong models
        startPoint - startpoint of the ray
        directionPoint - direction of the ray
        scene - three-dimensional scene
        Returns the closest object that intersects with the ray, the point of intersection, the object and the normal color
        """
    t = np.inf
    n = len(scene)
    for i in range(n):
        distance = ray_intersects(scene[i].get('object'),scene[i].get('position'),scene[i].get('noor'),startPoint, directionPoint)
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
    l = [ray_intersects(scene[i].get('object'),scene[i].get('position'),scene[i].get('noor'),M + N * .0001, directionL) for k in range(n) if k != index]
    if l and min(l) < np.inf:
        return
    col_ray = ambient
    col_ray += obj.get('diffuse',1.0) * max(np.dot(N, directionL), 0) * color
    col_ray += obj.get('specular_c', specular_c) * max(np.dot(N, normalize(directionL + directionO)), 0) ** specular_k * color_light
    return obj, M, N, col_ray

L,ambient,diffuse_c,specular_c,specular_k,depth_max,O,Q,scene = readfile2.make_scene(filename)
L, O, Q = np.array(L),np.array(O), np.array(Q)
color_light = np.ones(3)
col = np.zeros(3) 
img = np.zeros((h, w, 3))
for i, x in enumerate(np.linspace(-1, 1, w)):
    for j, y in enumerate(np.linspace(-1, 1, h)):
        col = np.zeros(3) 
        Q[:2]=(x,y)
        D = normalize(Q - O)
        depth = 0
        rayO, rayD = O, D
        reflection = 1.
        while depth < depth_max:
            traced = tracing(rayO, rayD, scene)
            if not traced:
                break
            obj, M, N, col_ray = traced
            rayO, rayD = M + N * .0001, normalize(rayD - 2 * np.dot(rayD, N) * N)
            depth += 1
            col += reflection * col_ray
            reflection *= obj.get('reflection', 1.)
        img[h - j - 1, i, :] = np.clip(col, 0, 1)

plt.imsave('fig.png', img)

    


# In[ ]:




# In[ ]:



