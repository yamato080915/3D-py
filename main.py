import pygame, math
pygame.init()
screen = pygame.display.set_mode((480,360))
reflection = 15/100
def sin(theta):
  return math.sin(math.radians(theta))
def cos(theta):
  return math.cos(math.radians(theta))
def atan(x):
  return math.degrees(math.atan(x))
def tan(theta):
  return math.tan(math.radians(theta))
xy=0
fov = atan(240/420)*2
graphics = [[1,2,4,3],[1,5,6,2],[1,3,7,5],[6,8,4,2],[3,4,8,7],[7,8,6,5]]
x = [50,-50,50,-50,50,-50,50,-50]
y = [50,50,-50,-50,50,50,-50,-50]
z = [50,50,50,50,-50,-50,-50,-50]
scr = 700

class main:
  def __init__(self):
    self.pers = screen*500/scr
    self.xto = []
    self.yto = []
    self.zto = []
    self.points = [[],[]]
  def direction(self, g):
    self.vector = []
    vector.append(self.xto[g[1]])
    vector.append(self.yto[g[1]])
    vector.append(self.zto[g[1]])
  def mov(self,x,y,z):
    self.xto.append(cos(zx)*cos(xy)*x-cos(zx)*sin(xy)*y+sin(zx)*z)
    self.yto.append((sin(yz)*sin(zx)*cos(xy)+cos(yz)*sin(xy))*x+(-1*sin(yz)*sin(zx)*sin(xy)+cos(yz)*cos(xy))*y-sin(yz)*cos(zx)*z)
    self.zto.append((-1*cos(yz)*sin(zx)*cos(xy)+sin(yz)*sin(xy))*x+(cos(yz)*sin(zx)*sin(xy)+sin(yz)*cos(xy))*y+cos(yz)*cos(zx)*z)

while True:
  mouseX, mouseY = pygame.mouse.get_pos()
  zx = mouseX*3/4
  yz = -1*mouseY
  screen = 240/tan(fov/2)
  exe = main()
  for i in range(len(x)):
    exe.mov(x[i],y[i],z[i])
    exe.points[0].append(exe.xto[i]*screen/(exe.pers-exe.zto[i]))
    exe.points[1].append(exe.yto[i]*screen/(exe.pers-exe.zto[i]))
  for i in graphics:
    exe.direction(i)
  pygame.display.update()
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  