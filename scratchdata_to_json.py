import os, json
files = os.listdir("./scratchdata/")
def strindex(text, word):
    positions = []
    current = 0
    while True:
        index = str(text).find(word, current)
        if index == -1:
            break
        positions.append(index)
        current = index+1
    return positions
def main(filename, d):
    template={"points":[],"surface":[], "color":[],"screen":700}
    if not ";" in d:return
    if d[0:2]!="{[":return
    index1 = strindex(d, "[")
    index2 = strindex(d, "]")
    x = eval(d[index1[0]:index2[0]+1])
    y = eval(d[index1[1]:index2[1]+1])
    z = eval(d[index1[2]:index2[2]+1])
    if len(x)!=len(y) or len(x)!=len(z) or len(index1)!=len(index2):return
    template["points"] = [str(tuple((x[i],y[i],z[i]))) for i in range(len(x))]
    for i in range(3,len(index1)):
        temp = d[index1[i]:index2[i]+1]
        if "(" in temp:
            color = temp[temp.index("("):temp.index(")")+1]
            template["surface"].append(str(tuple([x-1 for x in eval(temp.replace(color, ""))])))
            template["color"].append(color)
        else:
            template["surface"].append(str(tuple([x-1 for x in eval(temp)])))
            template["color"].append("(58,100,100)")
    template["screen"] = int(d[d.index(";")+1:])
    with open(f"./data/" + filename.replace(".txt",".json"), "w", encoding="utf-8") as f:
        json.dump(template, f, indent=2)
for i in files:
    with open(f"./scratchdata/{i}", "r", encoding="utf-8") as f:
        data = f.read()
        main(i,data)