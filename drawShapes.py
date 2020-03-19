from OpenGL.GL import *
from OpenGL.GLU import *
import pygame

import math

class Cube:
    def __init__ (self, size = [], localization = [], colorsRGBA = []):
        self.size = size
        self.localization = localization
        self.colorsRGBA = colorsRGBA
        
        self.vertices= [
            [1, -1, -1],
            [1, 1, -1],
            [-1, 1, -1],
            [-1, -1, -1],
            [1, -1, 1],
            [1, 1, 1],
            [-1, -1, 1],
            [-1, 1, 1]]
        self.surfaces = (
            (0,1,2,3),
            (3,2,7,6),
            (6,7,5,4),
            (4,5,1,0),
            (1,5,7,2),
            (4,0,3,6))
        self.edges = (
            (0,1),
            (0,3),
            (0,4),
            (2,1),
            (2,3),
            (2,7),
            (6,3),
            (6,4),
            (6,7),
            (5,1),
            (5,4),
            (5,7))

        #self.drawCube()
        

    def drawCube(self):
        glBindTexture(GL_TEXTURE_2D, 0)
        newVertices = []

        for i in range(0, len(self.vertices)):
            
            for j in range(0, len(self.vertices[i])):
                if(j == 0):
                    a = self.vertices[i][j] * self.size[0]
                if(j == 1):
                    b = self.vertices[i][j] * self.size[1]
                if(j == 2):
                    c = self.vertices[i][j] * self.size[2]
            
            listHolder = [a, b, c]
            newVertices.append(listHolder)
    
        glTranslatef(self.localization[0], self.localization[1], self.localization[2])
        glEnable(GL_BLEND)
        
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glBegin(GL_QUADS)
        for surface in self.surfaces:
            x = 0
            for vertex in surface:
                x+=1
                glColor4f(self.colorsRGBA[0], 
                          self.colorsRGBA[1], 
                          self.colorsRGBA[2], 
                          self.colorsRGBA[3])
                glVertex3fv(newVertices[vertex])
        glEnd()
        
        '''
        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glColor4f(0, 0, 0, 1)
                glVertex3fv(self.vertices[vertex])
        glEnd()
        '''
        glTranslatef(0, 0, 0)
        

    def getLocalization(self):
        return self.localization
    
    def updateLocalization(self, x, y, z, draw):
        self.localization[0] += x
        self.localization[1] += y
        self.localization[2] += z

        if (draw == True):
            self.drawCube()

    def changeLocalization(self, x, y, z, draw):
        self.localization[0] = x
        self.localization[1] = y
        self.localization[2] = z

        if(draw == True):
            self.drawCube()


textures = []

class Plane:
    def __init__ (self, fromToX = [], fromToY = [], fromToZ = [], colorRGBA = [], texture = "", repeatX = 1, repeatY = 1):
        self.fromToX = fromToX
        self.fromToY = fromToY
        self.fromToZ = fromToZ
        self.colorRGBA = colorRGBA
        self.texture = texture
        self.localization = [0, 0, 0]
        if (self.texture != ""):       
            self.textureID = loadTexture(self.texture)
        
        self.repeatX = repeatX
        self.repeatY = repeatY
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
        


    def drawPlaneGround(self):
        
        glPushMatrix()
        
        
        glTranslatef(self.localization[0], self.localization[1], self.localization[2])
        if (self.texture != ""):  
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.textureID)
        else :
            glDisable(GL_TEXTURE_2D) 

        glColor4f(self.colorRGBA[0], 
                  self.colorRGBA[1], 
                  self.colorRGBA[2], 
                  self.colorRGBA[3])
        
        
                  
        glBegin(GL_QUADS)
       
       
        glTexCoord2f(0.0, 1.0 * self.repeatX)
        glVertex3f(self.fromToX[0], self.fromToY[0], self.fromToZ[0])
        glTexCoord2f(0.0, 0.0)
        glVertex3f(self.fromToX[1], self.fromToY[0], self.fromToZ[0])
        glTexCoord2f(1.0 * self.repeatY, 0.0)
        glVertex3f(self.fromToX[1], self.fromToY[1], self.fromToZ[1])
        glTexCoord2f(1.0 * self.repeatY, 1.0 * self.repeatX)
        glVertex3f(self.fromToX[0], self.fromToY[1], self.fromToZ[1])
        glEnd()
        glPopMatrix()
        
    
    def drawPlaneWalls(self):
        glPushMatrix()
        if (self.texture != ""):  
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.textureID)
        
        glTranslatef(self.localization[0], self.localization[1], self.localization[2])
       
        glColor4f(self.colorRGBA[0], 
                  self.colorRGBA[1], 
                  self.colorRGBA[2], 
                  self.colorRGBA[3])
        glBegin(GL_QUADS)
       
        glTexCoord2f(0.0, 1.0 * self.repeatX)
        glVertex3f(self.fromToX[0], self.fromToY[0], self.fromToZ[0])

        glTexCoord2f(0.0, 0.0)
        glVertex3f(self.fromToX[1], self.fromToY[1], self.fromToZ[0])
        
        glTexCoord2f(1.0 * self.repeatY, 0.0)
        #glTexCoord2f(2, 0.0)
        glVertex3f(self.fromToX[1], self.fromToY[1], self.fromToZ[1])

        #glTexCoord2f(1.0 * self.repeat, 1.0 * self.repeat)
        glTexCoord2f(1.0 * self.repeatY, 1.0 * self.repeatX)
        glVertex3f(self.fromToX[0], self.fromToY[0], self.fromToZ[1])
        glEnd()
        glPopMatrix()
        

    def changeLocalization(self, x, y, z): 
        self.localization[0] = x
        self.localization[1] = y
        self.localization[2] = z

        #self.drawPlaneGround()

    def updateLocalization(self, x, y, z):
        self.localization[0] += x
        self.localization[1] += y
        self.localization[2] += z
            

        #self.drawPlaneWalls()

    def getLocalization(self):
        return self.localization



def loadTexture(texture):
    textureSurface = pygame.image.load(texture)
    textureSurface = pygame.transform.rotate(textureSurface, -90)
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
    width = textureSurface.get_width()
    height = textureSurface.get_height()
    

    texid = glGenTextures(1)
    
    

    glBindTexture(GL_TEXTURE_2D, texid)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
    
    #glTexEnviv( GL_TEXTURE_ENV, GL_TEXTURE_ENV_COLOR , [0, 1, 1, 1])

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)


    

    return texid


class ObjLoader(object):
    def __init__(self, filename, localization = [0, 0, 0]):
        self.vertices = []
        self.triangle_faces = []
        self.quad_faces = []
        self.polygon_faces = []
        self.normals = []
        self.localization = localization
        self.ang = 0
        #-----------------------
        try:
            f = open(filename)
            n = 1
            for line in f:
                if line[:2] == "v ":
                    index1 = line.find(" ") +1 #first number index;
                    index2 = line.find(" ",index1+1)  # second number index;
                    index3 = line.find(" ",index2+1) # third number index;
                        
                    vertex = (float(line[index1:index2]),float(line[index2:index3]),float(line[index3:-1]))
                    vertex = (round(vertex[0],2),round(vertex[1],2),round(vertex[2],2))
                    self.vertices.append(vertex)
                    
                elif line[:2] == "vn":
                    index1 = line.find(" ") +1 #first number index;
                    index2 = line.find(" ",index1+1)  # second number index;
                    index3 = line.find(" ",index2+1) # third number index;
                    
                    normal = (float(line[index1:index2]),float(line[index2:index3]),float(line[index3:-1]))
                    normal = (round(normal[0],2),round(normal[1],2),round(normal[2],2)) 
                    self.normals.append(normal)
                    
                elif line[0] == "f":
                    string = line.replace("//","/")
                    #---------------------------------------------------
                    i = string.find(" ")+1
                    face  = []
                    for item in range(string.count(" ")):
                        if string.find(" ",i) == -1:
                            face.append(string[i:-1])
                            break
                        face.append(string[i:string.find(" ",i)])
                        i = string.find(" ",i) +1
                    #---------------------------------------------------
                    if string.count("/") == 3:
                        self.triangle_faces.append(tuple(face))
                    elif string.count("/") == 4:
                        self.quad_faces.append(tuple(face))
                    else:
                        self.polygon_faces.append(tuple(face))
            f.close()
        except IOError:
            print ("Could not open the .obj file...")
            
    def render_scene(self):
        
        if len(self.triangle_faces) > 0:
            #-------------------------------
            glBegin(GL_TRIANGLES)
            for face in (self.triangle_faces):
                n = face[0]
                normal = self.normals[int(n[n.find("/")+1:])-1] 
                glNormal3fv(normal)
                for f in (face):
                    glVertex3fv(self.vertices[int(f[:f.find("/")])-1])
            glEnd()
            #---------------------------------
        
        if len(self.quad_faces) > 0:
            #----------------------------------
            glBegin(GL_QUADS)
            for face in (self.quad_faces):
                n = face[0]
                normal = self.normals[int(n[n.find("/")+1:])-1] 
                glNormal3fv(normal)
                for f in (face):
                    glVertex3fv(self.vertices[int(f[:f.find("/")])-1])
            glEnd()
            #-----------------------------------
            
        if len(self.polygon_faces) > 0:
            #----------------------------------
            for face in (self.polygon_faces):
                #---------------------
                glBegin(GL_POLYGON)
                n = face[0]
                normal = self.normals[int(n[n.find("/")+1:])-1] 
                glNormal3fv(normal)
                for f in (face):
                    glVertex3fv(self.vertices[int(f[:f.find("/")])-1])
                glEnd()
                #----------------------
            #-----------------------------------
        
    def render_texture(self,textureID,texcoord):
        glTranslate(self.localization[0], self.localization[1], self.localization[2])
        glBindTexture(GL_TEXTURE_2D,textureID)
        
        #self.ang += 45
        #glRotatef(self.ang,0,0,1)

        glBegin(GL_QUADS)
        for face in self.quad_faces:
            n = face[0]
            normal = self.normals[int(n[n.find("/")+1:])-1] 
            glNormal3fv(normal)
            for i,f in enumerate(face):
                glTexCoord2fv(texcoord[i])
                glVertex3fv(self.vertices[int(f[:f.find("/")])-1])
        glEnd()
    

    def getLocalization(self):
        return self.localization;

    def updateLocalization(self, x, y, z):
        self.localization[0] += x
        self.localization[1] += y
        self.localization[2] += z

        




