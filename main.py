import pygame, math, sys, json, colorsys
from pygame.locals import *
from tkinter import filedialog
import stl_to_json as stl
from ast import literal_eval
from time import perf_counter

f = filedialog.askopenfilename(title="select 3d data", filetypes=[("supported files", ".json .stl .STL"), ("json files", ".json"), ("stl files", ".stl .STL"), ("all files", "*.*")])
if ".stl" in f.lower():
  data = stl.main(f)
elif ".json" in f:
  with open(f, "r", encoding="utf-8") as f:
    data = json.load(f)
else:sys.exit()

pygame.init()
root = pygame.display.set_mode((480,360))

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

reflection = 15/100
xy=0
yz=0
zx=0
fov = atan(240/420)*2
x = [literal_eval(i)[0] for i in data["points"]]
y = [literal_eval(i)[1] for i in data["points"]]
z = [literal_eval(i)[2] for i in data["points"]]
graphics = [literal_eval(i) for i in data["surface"]]
color= [literal_eval(i) for i in data["color"]]
scr=data["screen"]
light = (-100,-200,400)#???y座標は正じゃないとおかしい　負にすると正しい動作をする
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
    self.sinxy=sin(xy)
    self.cosxy=cos(xy)
    self.sinyz=sin(yz)
    self.cosyz=cos(yz)
    self.sinzx=sin(zx)
    self.coszx=cos(zx)
  def zsort(self):
    result = []
    temp = []
    for i in self.polygons:
      temp.append(i[5])
    temp2 = sorted(temp)
    for i in temp2:
      for j in [k for k, x in enumerate(temp) if x == i]:
        if not j in result:
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
    self.xto.append(self.coszx*self.cosxy*x-self.coszx*self.sinxy*y+self.sinzx*z)
    self.yto.append((self.sinyz*self.sinzx*self.cosxy+self.cosyz*self.sinxy)*x+(-1*self.sinyz*self.sinzx*self.sinxy+self.cosyz*self.cosxy)*y-self.sinyz*self.coszx*z)
    self.zto.append((-1*self.cosyz*self.sinzx*self.cosxy+self.sinyz*self.sinxy)*x+(self.cosyz*self.sinzx*self.sinxy+self.sinyz*self.cosxy)*y+self.cosyz*self.coszx*z)

screen = 240/tan(fov/2)
exe = main()
FONTNAME = None
FONTSIZE = 30
string = "fps:0"
font = pygame.font.SysFont(FONTNAME, FONTSIZE)
timestamp = perf_counter()
count = 0
while True:
  count += 1
  root.fill((255,255,255))
  if count >= int(string.replace("fps:", "")):
    text = font.render(string, False, (0,0,0), (255, 255, 255))
    count = 0
  root.blit(text, (0,0))
  mouseX, mouseY = pygame.mouse.get_pos()
  zx = mouseX*3/4-180
  yz = -1*mouseY-180
  exe.__init__()
  for i in range(len(x)):
    exe.mov(x[i],y[i],z[i])
  exe.points[0] = [exe.xto[i]*screen/(exe.pers-exe.zto[i]) for i in range(len(x))]
  exe.points[1] = [exe.yto[i]*screen/(exe.pers-exe.zto[i]) for i in range(len(x))]
  for i in graphics:
    exe.calcdirection(i)
  exe.polygons = [[i, graphics[i][0], graphics[i][temp-1], graphics[i][temp], cos(exe.shader[i])*(1-reflection)+reflection, (exe.zto[graphics[i][0]]+exe.zto[graphics[i][temp-1]]+exe.zto[graphics[i][temp]])/3] for i in range(len(graphics)) for temp in range(2, len(graphics[i])) if exe.direction[i]<90]
  zsorted = exe.zsort()
  #graphic
  for i in zsorted:
    temp = exe.polygons[i]
    pygame.draw.polygon(
      root, rgb(color[temp[0]], temp[4]), #TODO shading
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
  string = f"fps:{int(1/(perf_counter()-timestamp))}"
  timestamp = perf_counter()