from plants import Plant, Fruit
#from creature import Creature
import typing
from environment import Environment, Region
import uuid, pickle, random as rd
GRID_ELEMENTS = ("fruit","plant","creature") 

class Grid():
    def __init__(self,x_size:int, y_size:int) -> None:
        self.id = f"simulation-{uuid.uuid4()}"
        self.x_size = x_size
        self.y_size = y_size
        self.grid = self.build_grid()

        self.plants_occupy = set()
        self.fruits_occupy = set()
        self.creatures_occupy = set()
        self.environment = Environment()

    def build_grid(self):
        # grid = {}
        grid: list[list[dict[str, typing.Any]]] = [
            [
                {
                    "env": set(),
                } for _ in range(self.x_size)
            ] for _ in range(self.y_size)
        ]
        # for y in range(self.y_size):
        #     for x in range(self.x_size):
        #         grid[(x,y)] = {
        #             "env": set(),
        #             "neighbors": set(),
        #         }
                
        #         grid[(x,y)]["neighbors"] = set(self.get_neighbors(x,y))

        # grid[0][0]["neighbors"] = {(0,1),(1,0),(1,1)}
        # grid[(0,self.y_size-1)]["neighbors"] = {(0,self.y_size-2),(1,self.y_size-2),(1,self.y_size-1)}
        # grid[(self.x_size-1),0]["neighbors"] = {(self.x_size-2,0),(self.x_size-2,1),(self.x_size-1,1)}
        # grid[(self.x_size-1,self.y_size-1)]["neighbors"] = {(self.x_size-1,self.y_size-2),(self.x_size-2,self.y_size-2),(self.x_size-2,self.y_size-1)}
        return grid

    def get_neighbors(self,x,y):
        neighbors = []
        if x == 0 and y != self.y_size-1:
            for ix in range(0, 2):
                for iy in range(-1, 2):
                    if not (ix == 0 and iy == 0):
                        neighbors.append((x + ix, y + iy))
        elif y == 0 and x != self.x_size-1:
            for ix in range(-1, 2):
                for iy in range(0, 2):
                    if not (ix == 0 and iy == 0):
                        neighbors.append((x + ix, y + iy))
        else:
            for ix in range(-1, 2):
                for iy in range(-1, 2):
                    if not (ix == 0 and iy == 0):
                        neighbors.append((x + ix, y + iy))
        return neighbors 
    
    def add_rectangle_region(self, x:int, y:int, w:int, h:int, given_energy: float):
        new_region = self.environment.create_new_region(x,y,w,h,given_energy)
        for y in range(self.y_size):
            for x in range(self.x_size):
                if x >=new_region.x and x<=new_region.x+new_region.w:              
                    if y>=new_region.y and y<=new_region.y+new_region.h:
                        self.grid[x][y]["env"].add(new_region)

    def add_plant(self, x:int, y:int, gene:list=[0]):
        if "plant" not in self.grid[x][y]:
            new_plant = Plant(x,y,gene)
            self.grid[x][y]["plant"] = new_plant
            self.plants_occupy.add((x,y))
            return new_plant.id

    def add_fruit(self, x:int, y:int, gene:list=[0]):
        if "fruit" not in self.grid[x][y]:
            new_fruit = Fruit(x,y,gene)
            self.grid[x][y]["fruit"] = new_fruit
            self.fruits_occupy.add((x,y))
            return new_fruit.id

    def remove_plant(self, x, y):
        del self.grid[x][y]["plant"]
        self.plants_occupy.discard((x,y))

    def remove_fruit(self, x, y):
        del self.grid[x][y]["fruit"]
        self.fruits_occupy.discard((x,y))

    def save_grid_state(self, address,step):
        with open(f"{address}/[{step}]-{self.id}", "wb") as file:
            pickle.dump(self,file)
        

if __name__ == "__main__":
    A = Grid(5,5)
    A.add_rectangle_region(0,0,2,2,15)
    A.add_rectangle_region(0,0,2,2,10)
    # aid = A.add_plant(1,1)
    # A.add_plant(1,1)
    # A.add_plant(1,2)
    # A.add_plant(3,3)
    # A.add_fruit(1,2,[0,1,1])
    # A.add_fruit(2,2,[0,1,1])
 
    # for key, items in A.grid.items():
    #     print(key)
    #     for key2, items2 in A.grid[key].items():
    #         print(key2,items2)

    # if A.grid[(2,3)]["env"]:
    #     print(A.grid[(2,3)]["env"])
    #     pick_env =rd.choice(list(A.grid[(2,3)]["env"])) 
    #     print(pick_env.food_available)
    # else:
    #     print(20)
    # print(A.grid[(1,1)])
    # print(A.plants_occupy)
    # A.remove_plant(1,1,aid)
    # print(A.grid[(1,1)])
    # print(A.plants_occupy)
    
    

    # for key, items in A.grid.items():
    #     for key2, items2 in A.grid[key]["plant"].items():
    #         if key==(1,1): data2remov = (key[0],key[1],key2)
    
    # #assim que remove um item
    # A.remove_plant(data2remov[0],data2remov[1],data2remov[2])
    # print(A.grid[(1,1)]["plant"])



    # #Assim que vamos embaralhar a ordem
    # A_lista = list(A.grid.keys())
    # rd.shuffle(A_lista)
    # print(A_lista)

    # for position in A_lista:
    #     print(f"{position} Cor do pixel: {A.grid[position]['color']}")
    #     for tipo, valores in A.grid[position].items():
    #         if valores:
    #             if "plant" in tipo:
    #                 for id, objeto in A.grid[position][tipo].items():
    #                     print(f"[PLANTA] posicao: {position}, id:{id}, obj: {objeto}")
    #             elif "fruit" in tipo:
    #                 for id, objeto in A.grid[position][tipo].items():
    #                     print(f"[FRUITS] posicao: {position}, id:{id}, obj: {objeto}")