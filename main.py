import pygame, math, sys
from pygame.locals import *
import colorsys

pygame.init()
root = pygame.display.set_mode((480,360))
reflection = 15/100
def sin(theta):
  return math.sin(math.radians(theta))
def cos(theta):
  return math.cos(math.radians(theta))
def acos(x):
  return math.degrees(math.acos(x))
def atan(x):
  return math.degrees(math.atan(x))
def tan(theta):
  return math.tan(math.radians(theta))
xy=0
fov = atan(240/420)*2
graphics = [[1,2,4,3],[1,5,6,2],[1,3,7,5],[6,8,4,2],[3,4,8,7],[7,8,6,5]]
for i in range(len(graphics)):
  for j in range(len(graphics[i])):
    graphics[i][j]-=1
  
x = [50,-50,50,-50,50,-50,50,-50]
y = [50,50,-50,-50,50,50,-50,-50]
z = [50,50,50,50,-50,-50,-50,-50]
scr = 700
light = (-100,200,400)
color = [58,100,100]
def rgb(hsv, shade):
  h = hsv[0]/100
  s = hsv[1]/100
  v = hsv[2]*shade/100
  return tuple([x*255 for x in list(colorsys.hsv_to_rgb(h,s,v))])

class main:
  def __init__(self):
    self.pers = screen*500/scr
    self.xto = []
    self.yto = []
    self.zto = []
    self.points = [[],[]]
    self.direction = []
    self.shader = []
    self.polygons = []
  def zsort(self):
    result = []
    temp = []
    for i in self.polygons:
      temp.append(i[5])
    temp2 = sorted(temp)
    for i in temp2:
      for j in [k for k, x in enumerate(temp) if x == i]:
        if j in result:
          pass
        else:
          result.append(j)
    return result
  def calcdirection(self, g):
    self.vector = []
    self.vector.append(self.xto[g[0]])
    self.vector.append(self.yto[g[0]])
    self.vector.append(self.zto[g[0]])
    self.vector.append(self.xto[g[1]]-self.vector[0])
    self.vector.append(self.yto[g[1]]-self.vector[1])
    self.vector.append(self.zto[g[1]]-self.vector[2])
    self.vector.append(self.xto[g[-1]]-self.vector[0])
    self.vector.append(self.yto[g[-1]]-self.vector[1])
    self.vector.append(self.zto[g[-1]]-self.vector[2])
    self.vector.append(self.vector[4]*self.vector[8]-self.vector[5]*self.vector[7])
    self.vector.append(self.vector[5]*self.vector[6]-self.vector[3]*self.vector[8])
    self.vector.append(self.vector[3]*self.vector[7]-self.vector[4]*self.vector[6])
    self.vector.append(0-self.vector[0])
    self.vector.append(0-self.vector[1])
    self.vector.append(self.pers-self.vector[2])
    self.direction.append(acos((self.vector[9]*self.vector[12]+self.vector[10]*self.vector[13]+self.vector[11]*self.vector[14])/math.sqrt((self.vector[9]**2+self.vector[10]**2+self.vector[11]**2)*(self.vector[12]**2+self.vector[13]**2+self.vector[14]**2))))
    self.vector[0:3]=[0,0,0]
    for i in g:
      self.vector[0]+=self.xto[i]/len(g)
      self.vector[1]+=self.yto[i]/len(g)
      self.vector[2]+=self.zto[i]/len(g)
    self.vector.append(light[0]-self.vector[0])
    self.vector.append(light[1]-self.vector[1])
    self.vector.append(light[2]-self.vector[2])
    self.shader.append(acos((self.vector[9]*self.vector[15]+self.vector[10]*self.vector[16]+self.vector[11]*self.vector[17])/math.sqrt((self.vector[9]**2+self.vector[10]**2+self.vector[11]**2)*(self.vector[15]**2+self.vector[16]**2+self.vector[17]**2))))
    if self.shader[-1]>90:
      self.shader[-1]=90
  def mov(self,x,y,z):
    self.xto.append(cos(zx)*cos(xy)*x-cos(zx)*sin(xy)*y+sin(zx)*z)
    self.yto.append((sin(yz)*sin(zx)*cos(xy)+cos(yz)*sin(xy))*x+(-1*sin(yz)*sin(zx)*sin(xy)+cos(yz)*cos(xy))*y-sin(yz)*cos(zx)*z)
    self.zto.append((-1*cos(yz)*sin(zx)*cos(xy)+sin(yz)*sin(xy))*x+(cos(yz)*sin(zx)*sin(xy)+sin(yz)*cos(xy))*y+cos(yz)*cos(zx)*z)

while True:
  root.fill((255,255,255))
  mouseX, mouseY = pygame.mouse.get_pos()
  zx = mouseX*3/4+240
  yz = -1*mouseY+180
  screen = 240/tan(fov/2)
  exe = main()
  for i in range(len(x)):
    exe.mov(x[i],y[i],z[i])
    exe.points[0].append(exe.xto[i]*screen/(exe.pers-exe.zto[i]))
    exe.points[1].append(exe.yto[i]*screen/(exe.pers-exe.zto[i]))
  for i in range(len(graphics)):
    exe.calcdirection(graphics[i])
    if exe.direction[i]<90:
      temp = 2
      while temp != len(graphics[i]):
        exe.polygons.append([i, graphics[i][0], graphics[i][temp-1], graphics[i][temp], cos(exe.shader[i])*(1-reflection)+reflection, (exe.zto[graphics[i][0]]+exe.zto[graphics[i][-2]]+exe.zto[graphics[i][-1]])/3])
        temp += 1
  zsorted = exe.zsort()
  #graphic
  for i in zsorted:
    temp = exe.polygons[i]
    pygame.draw.polygon(
      root, rgb(color, temp[4]), #TODO shading
      [
        (exe.points[0][temp[1]]+240,exe.points[1][temp[1]]+180),
        (exe.points[0][temp[2]]+240,exe.points[1][temp[2]]+180),
        (exe.points[0][temp[3]]+240,exe.points[1][temp[3]]+180)
      ],
      0
    )
  pygame.display.update()
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()