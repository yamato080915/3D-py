import os, json, sys
from stl import mesh

def json_to_scr(file):
    with open(file, "r", encoding="utf-8") as f:
        d = json.load(f)
    x = [eval(i)[0] for i in d["points"]]
    y = [eval(i)[1] for i in d["points"]]
    z = [eval(i)[2] for i in d["points"]]
    g = [f'{str([i+1 for i in list(eval(d["surface"][i]))])[:-1]}{d["color"][i]}]' for i in range(len(d["surface"]))]
    data = "{"+f"{x},{y},{z}"+"}{"+str(g)[1:-1]+"};"+str(d["screen"])
    return data.replace(" ","").replace("'","").replace('"','')

def stl_to_scr(file):
    d = mesh.Mesh.from_file(file)
    p = d.vectors.reshape(-1,3).tolist()
    g = d.vectors.tolist()
    x = [i[0]*50 for i in p]
    y = [i[1]*50 for i in p]
    z = [i[2]*50 for i in p]
    graphics = []
    indexer = {tuple(value): index for index, value in enumerate(p)}
    for i in g:
        temp = []
        for j in i:
            temp.append(indexer[tuple(j)]+1)
        graphics.append(temp)
    data = "{" + str(graphics)[1:-1].replace("]","(58,100,100)]") + "}"
    screen = int(700*50/max(x))
    data="{" +f"{x},{y},{z}" + "}" + data +f";{screen}"
    return data
file = input("enter the file path(.stl or .json)")
ext = os.path.splitext(file)
if ext[1] == ".stl":
    d = stl_to_scr(file)
elif ext[1] == ".json":
    d = json_to_scr(file)
else:
    print("unsupported file type!")
    sys.exit()
with open(f"{ext[0]}.txt", "w", encoding="utf-8") as f:
    f.write(d)
print(f"saved as {ext[0]}.txt")