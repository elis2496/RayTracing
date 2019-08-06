import numpy as np
import unittest

from utils import make_scene, ray_intersects


class FTestCase(unittest.TestCase):
    def test_readData(self):
        """Function which checks correct data were read from a text file or not"""
        scene1  =  [{'object': 'plane', 
                   'color': np.array([ 0., 0., 0.]), 
                   'specular_c': 0.5, 
                   'reflection': 0.5, 
                   'noor': np.array([ 0., 1., 0.]), 
                   'position': np.array([ 0., -0.5, 0.]), 
                   'diffuse': 0.5},  
                  {'object': 'sphere', 
                   'position': np.array([ 0.75, 0.1 , 1.]), 
                   'noor': 0.6, 
                   'reflection': 0.2, 
                   'color': np.array([ 0.1, 0., 0.4])},  
                 {'object': 'sphere', 
                  'position': np.array([-0.5, 0.1, 2.25]), 
                  'noor': 0.6, 
                  'reflection': 0.2, 
                  'color': np.array([ 0.7, 0.223, 0.5])},  
                 {'object': 'sphere', 
                  'position': np.array([-2.5, 0.1, 3.]), 
                  'noor': 0.6, 
                  'reflection': 0.2, 
                  'color': np.array([ 0. ,0.572, 0.184])}]
        L1 = [1.0, 5.0, -10.0]
        ambient1 = 0.05
        diffuse_c1 = 1.0
        specular1 = 1.0
        specular_k1 = 50.0
        depth_max1 = 5  
        O1 = [0.0, 0.35, -1.0]
        Q1 = [0.0, 0.0, 0.0]
        filename = 'data.txt'
        L, ambient, diffuse_c, specular, specular_k, depth_max, O, Q, scene = make_scene(filename)
        print(ambient, diffuse_c, specular, specular_k, depth_max)
        self.assertEqual(len(scene1),  len(scene))
        self.assertEqual(L1, L)
        self.assertEqual(ambient1, ambient)
        self.assertEqual(diffuse_c1, diffuse_c)
        self.assertEqual(specular_k1, specular_k)
        self.assertEqual(depth_max1, depth_max)
        self.assertEqual(O1, O)
        self.assertEqual(Q1, Q)
        for obj1,  obj2 in zip(scene1,  scene):
            self.assertEqual(obj1.get('object'), obj2.get('object'))
            for i, j in zip(obj1.get('position'), obj2.get('position')):
                self.assertEqual(i, j)
            self.assertEqual(obj1.get('specular_c', 1), obj2.get('specular_c', 1))
            if (obj1.get('object') == 'sphere'):
                self.assertEqual(obj1.get('noor'), obj2.get('noor'))
            else:    
                for i,  j in zip(obj1.get('noor'), obj2.get('noor')):
                    self.assertEqual(i, j)
                self.assertEqual(obj1.get('reflection'), obj2.get('reflection'))
            for i,  j in zip(obj1.get('color'), obj2.get('color')):    
                self.assertEqual(i, j)
                
    def test_planeInteresect(self):
        """Function which checks correct value were got using 
        function ray_intersects or not"""
        d_1 = 1.0
        d_2 = ray_intersects('plane',
                             np.array([1.,  1.,  1.]),
                             np.array([0.,  1.,  0.]),
                             np.array([0.,  0.,  0.]),
                             np.array([1., 1., 1.]))
        self.assertEqual(d_1, d_2)

    def test_sphereInteresect(self):
        """Function which checks correct value were got using function ray_intersects or not"""
        d_1 = 1.0
        d_2 = ray_intersects('sphere',
                             np.array([1.,  0.,  0.]),
                             1.,
                             np.array([1.,  0.,  0.]),
                             np.array([1., 0., 0.]))
        self.assertEqual(d_1, d_2)

        
testcase = FTestCase()
testcase.test_readData()
testcase.test_planeInteresect()
testcase.test_sphereInteresect()

if __name__  ==  "__main__":
    unittest.main()
