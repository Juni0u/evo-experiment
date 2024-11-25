from environment import Environment

res = (5,5)
grid = {}

env = Environment()
env.create_new_region(0,0,int(res[0]/2),int(res[1]/2), 15)
env.create_new_region(int(res[0]/2),0,int(res[0]/2),int(res[1]/2), 5)

for y in range(res[1]):
    for x in range(res[0]):
        grid[(x,y)] = { "plants": [],
            "fruits": [],
            "creatures": []
        }
    
        for region in env.regions:
            if x >=region.x and x<region.x+region.w:              
                if y>=region.y and y<region.y+region.h:
                    grid[(x,y)]["env"] = region
                    break


# for key, items in grid.items():
#     print(key,items)

import uuid

a=f"plant_{uuid.uuid4()}"
print(a)