from stl import mesh
import json, os, sys
def main(file):
    d = mesh.Mesh.from_file(file)
    p = d.vectors.reshape(-1,3).tolist()
    g = d.vectors.tolist()
    template={"points":[],"surface":[], "color":[],"screen":700}
    for i in p:
        template["points"].append(str(tuple(i)))
    indexer = {tuple(value): index for index, value in enumerate(p)}
    for i in g:
        temp = []
        for j in i:
            temp.append(indexer[tuple(j)])
        template["surface"].append(str(tuple(temp)))
    template["color"] = ["(58,100,100)" for i in template["surface"]]
    template["screen"] = int(700*50/max([i[0] for i in p]))
    return template

if __name__ == '__main__':
    file = input("enter the file path(.stl)")
    if os.path.splitext(file)[1].lower() != ".stl":
        print("stl file only!")
        sys.exit()
    data = main(file)
    with open(f"{os.path.splitext(os.path.basename(file))[0]}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)