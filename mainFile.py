import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.WGL import *


from drawShapes import *


import math
import numpy
from numpy.linalg import inv



pygame.init()
display = (1280, 720)
#display = (640, 480)
screen = pygame.display.set_mode(display, pygame.OPENGL|pygame.DOUBLEBUF)


glEnable(GL_NORMALIZE)
glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LESS)
glEnable(GL_LIGHTING)
glShadeModel(GL_SMOOTH)
glEnable(GL_COLOR_MATERIAL)
glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)


glEnable(GL_LIGHT0)
glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5, 0.5, 0.5, 1])
glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1])


sphere = gluNewQuadric() # Create a poligono temp

#-------------------- PROJECTION MATRIX SET --------------------#

glMatrixMode(GL_PROJECTION)
gluPerspective(45, (display[0]/display[1]), 0.1, 100.0)



#--------------------  END OF PROJECTION MATRIX SET --------------------#


#-------------------- PYGAME MOUSE AND RUN VARIABLES SET --------------------#

# init mouse movement and center mouse on screen
displayCenter = [screen.get_size()[i] // 2 for i in range(2)]
mouseMove = [0, 0]
pygame.mouse.set_pos(displayCenter)

up_down_angle = 0.0
paused = False
run = True


pygame.mouse.set_visible(0)

clock = pygame.time.Clock()

#-------------------- END OF PYGAME VARIABLES SET --------------------#

#-------------------- LOAD .CHRISTIAN SOURCE --------------------#

f = open("archs/source.christian", "r")

Lines = f.readlines()

scenarioWall = []
scenarioGroundRoof = []

for line in Lines:
    l = line.split(" ")
    if (l[0] == 'w'):
        #print(l)
        planeWall = Plane([float(l[1]), float(l[2])],
                      [float(l[3]), float(l[4])],
                      [float(l[5]), float(l[6])],
                      [float(l[7]), float(l[8]), float(l[9]), float(l[10])],
                      l[11],
                      float(l[12]),
                      float(l[13]))

        scenarioWall.append(planeWall)

    if (l[0] == 'gr'):
        #print(l)
        planeGR = Plane([float(l[1]), float(l[2])],
                      [float(l[3]), float(l[4])],
                      [float(l[5]), float(l[6])],
                      [float(l[7]), float(l[8]), float(l[9]), float(l[10])],
                      l[11],
                      float(l[12]), 
                      float(l[13]))

        scenarioGroundRoof.append(planeGR)

    if (l[0] == 'pp'):
        #print(l)
        playerPositionX = float(l[1])
        playerPositionY = float(l[2])
    

#-------------------- END OF LOAD .CHRISTIAN SOURCE --------------------#

#-------------------- QUICK MODELVIEW CONFIGURATION --------------------#
glMatrixMode(GL_MODELVIEW)
gluLookAt(playerPositionX, playerPositionY, 0, 0, 0, 0, 0, 0, 1)
viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
glLoadIdentity()
#-------------------- END OF MODELVIEW CONFIGURATION --------------------#


# cummom objects
cubeGun = Cube([0.5, 0.5, 1], [0, 0, 0], [0, 1.0, 0, 1])
cubeHitBox = Cube([1, 1, 1], [-3.5, 0, 0], [0.692424669, 1.0, 0, 0])

planeGun = Plane([-0.5, 0.5], [-0.5, 0.5], [0, 0], [1, 1, 1, 1], "archs/textures/gun/gun_doom.png", 1)
planeEnemie = Plane([-1, 1], [-1, -1], [-1, 1], [1, 1, 1, 1], "archs/textures/enemies/enemie.png", 1)



bullets = []
enemies = []


global_time = 0
eye_x = 0
shoot = 0
reset = 0
ang = 1

testSum = 0.1

cubo = ObjLoader('cube.obj', [0, 0, 0])
textureCubo = loadTexture('archs/textures/enemies/rubik.png')

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                run = False
            if event.key == pygame.K_PAUSE or event.key == pygame.K_p:
                paused = not paused
                pygame.mouse.set_pos(displayCenter) 
            if event.key == pygame.K_x:
                shoot = 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            shoot = 1

        if not paused: 
            if event.type == pygame.MOUSEMOTION:
                mouseMove = [event.pos[i] - displayCenter[i] for i in range(2)]
            pygame.mouse.set_pos(displayCenter)    

    if not paused:
        
        

        dt = clock.tick()
        global_time += dt

        # get keys
        keypress = pygame.key.get_pressed()
        #mouseMove = pygame.mouse.get_rel()

        #-----------------------------------------------------#

        # init model view matrix
        glLoadIdentity()

        # apply the look up and down
        up_down_angle += mouseMove[1]*0.1
        if (up_down_angle > 45):
            up_down_angle = 45
        if (up_down_angle < -45):
            up_down_angle = -45

        glRotatef(up_down_angle, 1.0, 0.0, 0.0)
        #print(up_down_angle)

        # init the view matrix
        glPushMatrix()
        glLoadIdentity()

        # apply the movment
        x = 0
        y = 0
        z = 0 
        if keypress[pygame.K_w]:
            #glTranslatef(0,0,0.1)
            z = 0.2
        if keypress[pygame.K_s]:
            #glTranslatef(0,0,-0.1)
            z = -0.2
        if keypress[pygame.K_d]:
            #glTranslatef(-0.1,0,0)
            x = -0.2
        if keypress[pygame.K_a]:
            #glTranslatef(0.1,0,0)
            x = 0.2
        if keypress[pygame.K_w] and keypress[pygame.K_LSHIFT]:
            #glTranslatef(0,0,0.3)
            z = 0.5
        
        if keypress[pygame.K_z]:
            #glTranslatef(0,0,0.3)
            reset = 1
        
        glTranslatef(x, y, z)
        
        # apply the left and right rotation
        left_right_angle = mouseMove[0]*0.1
        glRotatef(left_right_angle, 0.0, 1.0, 0.0)
        #print(left_right_angle)

        eye_x += left_right_angle
        

        
        
        # multiply the current matrix by the get the new view matrix and store the final view matrix 
        glMultMatrixf(viewMatrix)
        
        viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        inV = numpy.array(viewMatrix)
        inv = numpy.linalg.inv(inV)
        camera_pos = inv[3]

        #print(inv[2] * (-1))
        #print(camera_pos)
        #print("\n")

        

        # apply view matrix
        glPopMatrix()
        glMultMatrixf(viewMatrix)
        
        #-----------------------------------------------------#
        #glLightfv(GL_LIGHT0, GL_POSITION, [1, -1, 1, 0])
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        #Add ambient light:
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT,[1,1,1,1.0])
        
        #Add positioned light:
        glLightfv(GL_LIGHT0,GL_DIFFUSE, [1, -1, 1, 0])
        glLightfv(GL_LIGHT0,GL_POSITION,[1, -1, 1, 0])
        
        glPushMatrix()

        dx = inv[3][0]
        dy = inv[3][1]


        #-------------------- RENDER OBJECTS --------------------#
        
        

       
        
        # hitbox
        glPushMatrix()

        glDisable(GL_DEPTH_TEST)
        cubeHitBox.changeLocalization(dx, dy, 0, True)
        
        glEnable(GL_DEPTH_TEST)
        glPopMatrix()


        # cubo seeker

        glPushMatrix()
        '''
        #glMaterialfv(GL_FRONT, GL_EMISSION, [1, 1, 1, 1])
        glTranslatef(-1.5, 0, 0)
        glColor4f(0.5, 0.2, 0.2, 1)
        gluSphere(sphere, 1.0, 32, 16) 
        '''
        #testSum += 0.1
        #glTranslatef(4, 0, 0)
        #glRotatef(90, 1, 0 ,0)
        #hol = cubo.getLocalization()
        #dx1 = dx - hol[0]
        #dy2 = dy - hol[1] 
        
        #glTranslatef(testSum, testSum, 0)
        #cubo.updateLocalization(0.01*dx1, 0.01*dy2, 0)
        #glColor4f(1, 1, 1, 1)
        #cubo.render_texture(textureCubo,((0,0),(1,0),(1,1),(0,1)))
              
        #cubo.render_scene()


        glPopMatrix()
        
        #-------------------- END OF RENDER OBJECTS --------------------#

        #-------------------- RENDER TEXTURE OBJECTS --------------------#
        glPushMatrix()
        
        if (scenarioWall):
            for a in scenarioWall:
                a.drawPlaneWalls()
                        
                
        if (scenarioGroundRoof):
            for a in scenarioGroundRoof:
                a.drawPlaneGround()  
        
        glPopMatrix()

        glPushMatrix()
        
        
        if (shoot == 1):  
            speedXY = 1
            speedZ = 1
            x = math.sin(math.radians(eye_x))
            y =  math.cos(math.radians(eye_x))
            z = math.sin(math.radians(up_down_angle))
            #print(eye_x, up_down_angle, x, y, -z)
    
            #cubeBullet = Cube([0.05, 0.05, 0.05], [dx + x, dy + y, 0 - z], [1, 0, 0, 1])
            planeBullet = Plane([-1, 1], [-1, 1], [-2, 3], [1, 1, 1, 0.3], "", 1)
            planeBullet.changeLocalization(dx, dy, 0)
            punch_start = global_time
            punch_duration = 600 

            bullets.append([planeBullet, 
                            speedXY * math.sin(math.radians(eye_x)), 
                            speedXY * math.cos(math.radians(eye_x)),
                            -speedZ * math.sin(math.radians(up_down_angle)),
                            punch_start,
                            punch_duration])
            shoot = 0
                   
       
        
        count = 0
        if (bullets):
            for i in bullets:
                glPushMatrix()
                i[0].updateLocalization(i[1], 
                                        i[2], 
                                        i[3])
                
                i[0].drawPlaneWalls()
                #print(i[0].getLocalization())
                #print('\n')
                if (global_time > i[4] + i[5]):
                    del(bullets[count])
                
                glPopMatrix()
            count += 1
        
        
        #print(bullets)

        
        if (reset == 1):
            bullets = []
            
        glPopMatrix()

        '''
        # gun
        glPushMatrix()
        glLoadIdentity()  
        #cubeGun.changeLocalization(0.0, -1.5, -3, True)   
        glClear(GL_DEPTH_BUFFER_BIT)  
        planeGun.changeLocalization(-0.2, -1.3, -4.3)
        planeGun.drawPlaneGround()
        #planeGun.updateLocalization(-10, -1.0, -9)
        #print(planeGun.getLocalization())
        

        glPopMatrix()
        '''
          

        glPopMatrix()



        reset = 0
        
        pygame.display.flip()
        #pygame.time.wait(10)

        
        #clock.tick()
        fps = clock.get_fps()
        print("fps: " + str(fps))
        

pygame.quit()


