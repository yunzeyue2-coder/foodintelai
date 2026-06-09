import json
f=open("/Users/mac/Desktop/虾哥/h5工作站/recipes-data.json")
d=json.load(f)
targets = ["铁板炒饭","锡纸花甲粉","柳州螺蛳粉","万能卤水","川式五香卤水","高汤熬制","鸭血粉丝汤","兰州拉面","潮汕卤水","湖州卤水"]
for item in d:
    for t in targets:
        if t in item["name"]:
            print(json.dumps(item, ensure_ascii=False))
            break
