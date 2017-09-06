from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
from threading import Thread

import math

from numpy.lib.function_base import angle


class Visualization:
    rotate_x = 0
    rotate_y = 0
    rotate_z = 0
    update = 0

    def __init__(self):
        thread = Thread(target=self.main)
        thread.start()

    def main(self):

        glutInit(sys.argv)
        glutKeyboardFunc(self.keyPressed)

        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(800,600)
        glutCreateWindow(b'IMU')

        glClearColor(0.,0.,0.,1.)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_CULL_FACE)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        lightZeroPosition = [10.,4.,10.,1.]
        lightZeroColor = [0.8,1.0,0.8,1.0] #green tinged
        glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
        glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
        glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
        glEnable(GL_LIGHT0)

        glutKeyboardFunc(self.keyPressed)
        glutIdleFunc(self.display)
        glutDisplayFunc(self.display)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(40.,1.,1.,40.)
        glMatrixMode(GL_MODELVIEW)
        gluLookAt(0,0,10,
                  0,0,0,
                  0,1,0)
        glPushMatrix()
        glutMainLoop()
        return

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)


        #glPushMatrix()

        color = [1.0,0.,0.,1.]
        glMaterialfv(GL_FRONT,GL_DIFFUSE,color)

        glPushMatrix()
        if self.update:
            glRotate(self.rotate_x, 1, 0, 0)
            glRotate(self.rotate_y, 0, 1, 0)
            glRotate(self.rotate_z, 0, 0, 1)
            #self.rotate_x, self.rotate_y, self.rotate_z = 0, 0, 0
            #self.update = 0
        glutSolidCube(2)
        glPopMatrix()

        glPushMatrix()
        glBegin(GL_LINE_LOOP)
        i = 0
        angle =  0
        for i in range(360):
             angle_d = 360 / 360
             angle += angle_d
             x = math.cos(angle)
             y = math.sin(angle)
             i+=1
             glVertex2d(x+3, y)
        glEnd()
        glPopMatrix()


        glPushMatrix()
        glBegin(GL_LINE_LOOP)
        glVertex2d(0 + 3, 0)
        glVertex2d(0 + 3, 1)
        glEnd()
        glPopMatrix()

        glPushMatrix()
        color = [0, 1, 0., 1.]
        glMaterialfv(GL_FRONT, GL_DIFFUSE, color)

        glBegin(GL_LINE_LOOP)
        glVertex2d(0 + 3, 0)
        glVertex2d(0 + 3, -1)
        glEnd()
        glPopMatrix()


        #glPopMatrix()




        glutSwapBuffers()
        return

    def keyPressed(self,*args):
        print( str(args[0]))
        # If escape is pressed, kill everything.

        if args[0] == b'a':
            self.rotate_x += 1.1
            print(self.rotate_x)
            self.update = 1




    def rotate_rpy(self,rpy_values):
        print("rotate_rpy")
        self.rotate_x, self.rotate_y, self.rotate_z = rpy_values
        self.update = 1

vis = Visualization()
