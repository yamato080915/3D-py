import pygame, math, sys, json, colorsys, threading
from pygame.locals import *
from tkinter import filedialog
import stl_to_json as stl
import numpy as np
from ast import literal_eval
from time import perf_counter

pygame.init()
root = pygame.display.set_mode((480,360))

def fileselect(f):
  global data, x, y, z, graphics, color, scr, points
  data = ""
  if ".stl" in f.lower():
    data = stl.main(f)
  elif ".json" in f.lower():
    with open(f, "r", encoding="utf-8") as f:
      data = json.load(f)
  if data != "":
    points = np.array([list(literal_eval(i)) for i in data["points"]])
    graphics = [literal_eval(i) for i in data["surface"]]
    color= [literal_eval(i) for i in data["color"]]
    scr=data["screen"]

f = ""
def update():
  global f
  f = filedialog.askopenfilename(title="Select 3d data", filetypes=[("supported files", ".json .stl"), ("json files", ".json"), ("stl files", ".stl .STL"), ("all files", "*.*")])
def thread():
  th = threading.Thread(target=update, daemon=True)
  th.start()
  while th.is_alive():
    root.fill((255,255,255))
    pygame.display.update()
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      if f!="":break
thread()
fileselect(f)

if data == "":sys.exit()

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
lightv = np.array((-100,200,400))
size = 1
def rgb(hsv, shade):
  h = hsv[0]/100
  s = hsv[1]/100
  v = hsv[2]*shade/100
  return tuple([x*255 for x in list(colorsys.hsv_to_rgb(h,s,v))])

class main:
  def __init__(self):
    self.pers = screen*500/scr
    self.cam = np.array([0,0,self.pers])
    self.pointto = []
    self.points = []
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
    temp = [i[5] for i in self.polygons]
    temp2 = sorted(temp)
    for i in temp2:
      for j in [k for k, x in enumerate(temp) if x == i]:
        if not j in result:
          result.append(j)
    return result
  def calcdirection_np(self, g):
    g0 = self.pointto[g[0]]
    g1 = self.pointto[g[1]]
    g_1 = self.pointto[g[-1]]
    g1_g0 = g1-g0
    g_1_g0 = g_1-g0
    normal_vec = np.cross(g1_g0,g_1_g0)
    cam_g0 = self.cam-g0
    direction = acos(np.dot(normal_vec, cam_g0)/(np.linalg.norm(normal_vec)*np.linalg.norm(cam_g0)))
    gravity = np.array([0.0,0.0,0.0])
    for i in g:
      gravity += self.pointto[i]
    gravity /= len(g)
    light_gravity = lightv-gravity
    shader = acos(np.dot(normal_vec, light_gravity)/(np.linalg.norm(normal_vec)*np.linalg.norm(light_gravity)))
    if shader > 90:shader = 90
    self.direction.append(direction)
    self.shader.append(shader)
  def mov_np(self,point):
    rotpoint = np.dot(rot, point)
    self.pointto.append(rotpoint)

screen = 240/tan(fov/2)
exe = main()
fps = 120
limit = 240
latency = 0
font = pygame.font.SysFont(None, 20)
WireBackface = 2
clock = pygame.time.Clock()
while True:
  timestamp = perf_counter()
  root.fill((255,255,255))
  key_pressed = pygame.key.get_pressed()
  if key_pressed[pygame.K_LCTRL] and key_pressed[pygame.K_o]:
    thread()
    fileselect(f)
  fps = clock.get_fps()
  mouseX, mouseY = pygame.mouse.get_pos()
  if mouseX*3/4-180 != zx or -1*mouseY-180 != yz:
    zx = mouseX*3/4-180
    yz = mouseY-180
    exe.__init__()
    rotx = np.array([[1,0,0],[0,exe.cosyz, -exe.sinyz],[0, exe.sinyz, exe.cosyz]])
    roty = np.array([[exe.coszx, 0, exe.sinzx],[0,1,0], [-exe.sinzx, 0, exe.coszx]])
    rotz = np.array([[exe.cosxy, -exe.sinxy, 0],[exe.sinxy, exe.cosxy, 0],[0,0,1]])
    rot = np.dot(rotx,roty,rotz)
    for i in range(len(points)):
      exe.mov_np(points[i])
    exe.points = np.array([[exe.pointto[i][0]*screen/(exe.pers-exe.pointto[i][2]),exe.pointto[i][1]*screen/(exe.pers-exe.pointto[i][2])] for i in range(len(points))])
    for i in graphics:
      exe.calcdirection_np(i)
    exe.polygons = [[i, graphics[i][0], graphics[i][temp-1], graphics[i][temp], cos(exe.shader[i])*(0.95-reflection)+reflection, (exe.pointto[graphics[i][0]][2]+exe.pointto[graphics[i][temp-1]][2]+exe.pointto[graphics[i][temp]][2])/3, exe.direction[i] < 90] for i in range(len(graphics)) for temp in range(2, len(graphics[i])) if exe.direction[i]<90 or (pygame.mouse.get_pressed()[0] and WireBackface)]
    zsorted = exe.zsort()
  mousepressed = pygame.mouse.get_pressed()
  for i in zsorted:
    temp = exe.polygons[i]
    pygame.draw.polygon(
      root, rgb(color[temp[0]], temp[4]), 
      [
        (size*exe.points[temp[1]][0]+240,-size*exe.points[temp[1]][1]+180),
        (size*exe.points[temp[2]][0]+240,-size*exe.points[temp[2]][1]+180),
        (size*exe.points[temp[3]][0]+240,-size*exe.points[temp[3]][1]+180)
      ],
      mousepressed[0]*(temp[6] * (2 + WireBackface) + WireBackface)
    )
  if fps != 0.0:
    text = font.render(f"fps:{round(fps, 1)}   render latency:{round(1000*latency, 1)}ms", True, (0,0,0), (255, 255, 255))
    root.blit(text, (0,0))
  latency = perf_counter()-timestamp
  pygame.display.update()
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
    if key_pressed[pygame.K_LCTRL] and event.type == pygame.MOUSEWHEEL:
      size += event.y*0.05
      if size <= 0:
        size = 0.05
  clock.tick(limit)
  