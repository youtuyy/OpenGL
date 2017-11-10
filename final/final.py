# CSC 240, Fianl Project
# Zhaoyan Lin

import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random
from PIL import Image
import math

updown = 0
elbowAngle = 0
falling = 0
FPS = 60
r1 = 0
r2 = 0
weave = 0
grass = 0

# Handles the keyboard event
def special(key, x, y):
  global elbowAngle
  global updown
  
  
  if key == GLUT_KEY_RIGHT:
    elbowAngle += 5
    elbowAngle = elbowAngle % 360
  elif key == GLUT_KEY_LEFT:
    elbowAngle -= 5
    elbowAngle = elbowAngle % 360
  elif key == GLUT_KEY_UP:
    updown += 0.5
  elif key == GLUT_KEY_DOWN:
    updown -= 0.5
  
  glutPostRedisplay()

# given a filename (string), set up and return the texture
def texture_from_jpg(filename):
    img = Image.open(filename)
    img_data = list(img.getdata())
    
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    
    tex_name = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_name)
    
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    
    return tex_name

def wireBox(width, height, depth):
    glPushMatrix()
    global weave
    
    ambient_color_wire = [1, 1, 1, .1]
    diffuse_color_wire = [1, 1, 1, .1]
    glMaterialfv(GL_FRONT, GL_AMBIENT, ambient_color_wire)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse_color_wire)
    
    glScalef(width, height, depth)
    glutWireCube(1.0)
    glPopMatrix()

def solidBox(width, height, depth):
    glPushMatrix()
    ambient_color_solid = [.1, .5, 1, .1]
    diffuse_color_solid = [.1, .1, 1, .1]
    glMaterialfv(GL_FRONT, GL_AMBIENT, ambient_color_solid)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse_color_solid)
    glScalef(width, height, depth)
    global weave
    glEnable(GL_TEXTURE_2D)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glEnable(GL_TEXTURE_GEN_S)
    glEnable(GL_TEXTURE_GEN_T)
    glBindTexture(GL_TEXTURE_2D, weave)
    glutSolidCube(1.0)
    glDisable(GL_TEXTURE_GEN_S)
    glDisable(GL_TEXTURE_GEN_T)
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()

def fall():
    glPushMatrix()
    global falling
    global r1
    global r2
    if falling >= 30.0:
        r1 = 4*random.random()
        r2 = -4*random.random()
        glTranslatef(0, 20, 0)
        falling = 0
    
    falling += 0.05
    glTranslatef(0, -falling, 0)
    glTranslatef(0, 20, 3)
    ball()


def ball():
    ambient_color_ball = [1, .5, 0, .1]
    diffuse_color_ball = [1, .5, 0, .1]
    emission_color_ball = [.1, 0, 0, .1]
    glMaterialfv(GL_FRONT, GL_AMBIENT, ambient_color_ball)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse_color_ball)
    glMaterialfv(GL_FRONT, GL_EMISSION, emission_color_ball)
    glLightfv(GL_LIGHT1, GL_POSITION, [0, 0, 0, 1])
    glutSolidSphere(0.2, 16, 16)
    glPopMatrix()

def randomFall():
    glPushMatrix()
    glPushMatrix()
    glTranslatef(r1, 0, -r2/2)
    fall()
    glPopMatrix()
    glPushMatrix()
    glTranslatef(10, 0, 0)
    glTranslatef(r1, 0, r1/2)
    fall()
    glPopMatrix()
    glPushMatrix()
    glTranslatef(15, 0, 0)
    glTranslatef(r2, 0, r1/2)
    fall()
    glPopMatrix()
    glPopMatrix()

def floor():
    global grass
    ambient_color_floor = [1, 1, 1, 0]
    diffuse_color_floor = [1, 1, 1, 0]
    glMaterialfv(GL_FRONT, GL_AMBIENT, ambient_color_floor)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse_color_floor)
    
    glTranslatef(0,-1,0)
    glScalef(40,0.5,40)
    glEnable(GL_TEXTURE_2D)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glEnable(GL_TEXTURE_GEN_S)
    glEnable(GL_TEXTURE_GEN_T)
    glBindTexture(GL_TEXTURE_2D, grass)
    glutSolidCube(1.0)
    glDisable(GL_TEXTURE_GEN_S)
    glDisable(GL_TEXTURE_GEN_T)
    glDisable(GL_TEXTURE_2D)

def flr():
    glPushMatrix()
    
    glPushMatrix()
    ambient_color_stk = [.4, .5, 0, .1]
    diffuse_color_stk = [.3, .4, 0, .1]
    glMaterialfv(GL_FRONT, GL_AMBIENT, ambient_color_stk)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse_color_stk)
    glScalef(0.02,0.6,0.1)
    glutWireCube(1)
    glPopMatrix()
    
    glPushMatrix()
    ambient_color_lf = [.2, .5, 0, .1]
    diffuse_color_lf = [.1, .4, 0, .1]
    glMaterialfv(GL_FRONT, GL_AMBIENT, ambient_color_lf)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse_color_lf)
    
    glPushMatrix()
    glTranslatef(0.15,0,0)
    glutWireSphere(0.1,8,8)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(-0.15,0,0)
    glutWireSphere(0.1,8,8)
    glPopMatrix()
    
    glPopMatrix()
    
    glPushMatrix()
    ambient_color_flr = [.4, 0, .5, .1]
    diffuse_color_flr = [.3, 0, .5, .1]
    glMaterialfv(GL_FRONT, GL_AMBIENT, ambient_color_flr)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse_color_flr)
    glTranslatef(0,0.3,0)
    glutWireSphere(0.2,8,8)
    glPopMatrix()
    
    glPopMatrix()

def xtree():
    
    ambient_color_trbody = [.2, .5, 0, .1]
    diffuse_color_trbody = [.1, .5, 0, .1]
    glMaterialfv(GL_FRONT, GL_AMBIENT, ambient_color_trbody)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse_color_trbody)
    glPushMatrix()
    glTranslatef(0,1.5,0)
    glPushMatrix()
    glRotatef(-90,1,0,0)
    glutSolidCone(1.5, 3, 10, 2)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0,2,0)
    glPushMatrix()
    glRotatef(-90,1,0,0)
    glutSolidCone(1.0, 3, 10, 2)
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()
    glPushMatrix()
    ambient_color_tbody = [.8, .3, .1, .1]
    diffuse_color_tbody = [.8, .3, .1, .1]
    glMaterialfv(GL_FRONT, GL_AMBIENT, ambient_color_tbody)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse_color_tbody)
    glRotatef(-90,1,0,0)
    glutSolidCone(0.5, 3, 10, 2)
    
    glPopMatrix()

def tree(x1, y1, angle, depth):
    if depth>=0:
        x2 = x1 + int(math.cos(math.radians(angle)) * depth)
        y2 = y1 + int(math.sin(math.radians(angle)) * depth)
        glBegin(GL_LINES)
        glVertex2f(x1, y1)
        glVertex2f(x2, y2)
        glEnd()
        tree(x2, y2, angle - 20, depth - 1)
        tree(x2, y2, angle + 20, depth - 1)

def man():
    ambient_color_body = [.8, .8, .8, .1]
    diffuse_color_body = [.8, .8, .8, .1]
    glMaterialfv(GL_FRONT, GL_AMBIENT, ambient_color_body)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse_color_body)
    glPushMatrix()
    glTranslatef(0,1,0)
    glPushMatrix()
    glutSolidSphere(0.75, 20, 20)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.0, 1.0, 0.0)
    glutSolidSphere(0.5, 20, 20)
    
    glPushMatrix()
    glTranslatef(0.0, 0.0, 0.1)
    glPushMatrix()
    ambient_color_eye = [0, 0, 0, .1]
    diffuse_color_eye = [.5, 0, .5, .1]
    glMaterialfv(GL_FRONT, GL_AMBIENT, ambient_color_eye)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse_color_eye)
    glTranslatef(-0.2, 0.4, 0.3)
    glutSolidSphere(0.05, 10, 10)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(+0.2, 0.4, 0.3)
    glutSolidSphere(0.05, 10, 10)
    glPopMatrix()
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0.0, 0.05, 0.5)
    ambient_color_nose = [.5, 0, 0, .1]
    diffuse_color_nose = [.5, 0, 0, .1]
    glMaterialfv(GL_FRONT, GL_AMBIENT, ambient_color_nose)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse_color_nose)
    glutSolidCone(0.08, 0.5, 10, 2)
    glPopMatrix()
    
    glPopMatrix()
    glPushMatrix()
    glScalef(1.0, 1.0, 0.0)
    glutSolidSphere(0.75, 20, 20)

    glPopMatrix()
    glPopMatrix()


def display():


  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

  glMatrixMode(GL_MODELVIEW)


  # RGBA (A=alpha, transparent: alpha=0, opaque: alpha=1)
  ambient_color = [ 1, 1, 1, .1]
  diffuse_color = [2, 2, .1, .5]
          
  # light position (x,y,z,w)
  light_position = [-2, 15, 1, 1]
              
  # properties of GL_LIGHT0 (global light source)
  glLightfv(GL_LIGHT0, GL_AMBIENT, ambient_color)
  glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse_color)
  glLightfv(GL_LIGHT0, GL_POSITION, light_position)
  glPushMatrix()
  ambient_color_floor = [.5, .7, .1, .1]
  diffuse_color_floor = [0, .3, 0, .1]
  glMaterialfv(GL_FRONT, GL_AMBIENT, ambient_color_floor)
  glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse_color_floor)
  glScalef(0.1,0.1,1)
  tree(0, 10, 90, 7)
  tree(-30, 5, 80, 8)
  tree(20, 10, 100, 6)
  tree(65, 5, 90, 6)
  tree(-60, -15, 75, 6)
  tree(-50, -15, 90, 10)
  glPopMatrix()
  
  glPushMatrix()
  glTranslatef(5,-0.3,-1)
  xtree()
  glPopMatrix()
  
  glPushMatrix()
  glTranslatef(3.0, 1.0, 0.0)
  flr()
  glPopMatrix()
  glPushMatrix()
  glTranslatef(3.5, 0.5, 0.0)
  flr()
  glPopMatrix()
  glPushMatrix()
  glTranslatef(2.5, 0.8, 0.0)
  flr()
  glPopMatrix()
  glPushMatrix()
  glTranslatef(-3.0, 0.6, 0.0)
  flr()
  glPopMatrix()

  glPushMatrix()
  randomFall()
  
  glPushMatrix()
  glTranslatef(updown, 0.0, 0.0)
  solidBox(1.0, 0.4, 0.4)
  
  glPushMatrix()
  glRotatef(elbowAngle, 0.0, 1.0, 0.0)
  glPushMatrix()
  man()
  glPopMatrix()
  glRotatef(-90, 0.0, 1.0, 0.0)
  glTranslatef(2.0, 0.0, 0.0)
  solidBox(4.0, 0.4, 0.4)
  glTranslatef(2.5, 0.0, 0.0)
  wireBox(1.0, 1.0, 1.0)
  glPopMatrix()
  glPopMatrix()
  glPopMatrix()

  glPushMatrix()
  floor()
  glPopMatrix()
  glFlush()


# Handles the reshape event by setting the viewport so that it takes up the
# whole visible region, then sets the projection matrix to something reason-
# able that maintains proper aspect ratio.
def reshape(w, h):
  glViewport(0, 0, w, h)
  glMatrixMode(GL_PROJECTION)
  glLoadIdentity()
  gluPerspective(65.0, w/h, 1.0, 20.0)

# Handles the timer by requesting the window to display again. Since the timer
# function is only called once, it sets the same function to be called again.
def timer(v):
    glutPostRedisplay()
    
    # arguments: milliseconds to wait before passing callback, which timer function
    # to call, and a value v (not used here)
    glutTimerFunc(int(1000/FPS), timer, v)

# Perfroms application specific initialization: turn off smooth shading,
# sets the viewing transformation once and for all.  In this application we
# won't be moving the camera at all, so it makes sense to do this.
def init():
  glClearColor(0, 0, 0, 0)
  glEnable(GL_LIGHTING)
  glEnable(GL_LIGHT0)
  glEnable(GL_LIGHT1)
  glEnable(GL_DEPTH_TEST)
  glShadeModel(GL_SMOOTH)
  glMatrixMode(GL_MODELVIEW)
  glLoadIdentity()
  gluLookAt(1,4,12, 0,3,0, 0,1,0)
  global weave
  weave = texture_from_jpg("red.jpg")
  global grass
  grass = texture_from_jpg("grass.jpg")


# Initializes GLUT, the display mode, and main window; registers callbacks;
# does application initialization; enters the main event loop.
if __name__=='__main__':
  glutInit(sys.argv)
  glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
  glutInitWindowPosition(80, 80)
  glutInitWindowSize(800, 600)
  glutCreateWindow(b"Snowmans")
  glutDisplayFunc(display)
  glutReshapeFunc(reshape)
  glutSpecialFunc(special)
  init()
  glutTimerFunc(0, timer, 0) # start the timer (only called once, but then calls itself again)
  glutMainLoop()

