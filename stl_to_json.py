from stl import mesh
import json

d = mesh.Mesh.from_file("./stldata.stl")
p = d.vectors.reshape(-1,3).tolist()
g = d.vectors.tolist()
template={"points":[],"surface":[], "color":[],"screen":700}
for i in p:
    template["points"].append(str(tuple(i)))
for i in g:
    temp = []
    for j in i:
        temp.append(p.index(j))
    template["surface"].append(str(tuple(temp)))
template["color"] = ["(58,100,100)" for i in range(len(template["surface"]))]
template["screen"] = 700*50/max([i[0] for i in p])
with open("./stl.json", "w", encoding="utf-8") as f:
    json.dump(template, f, indent=2)