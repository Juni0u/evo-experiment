from plants import Plant, Fruit
from environment import Environment, Region
import uuid, random as rd

class Grid():
    def __init__(self,x_size:int, y_size:int) -> None:
        self.x_size = x_size
        self.y_size = y_size
        self.grid = self.build_initial_grid(x_size, y_size)
        self.environment = Environment()

    def build_initial_grid(self, x_size, y_size):
        grid = {}
        
        for y in range(y_size):
            for x in range(x_size):
                grid[(x,y)] = {
                    "plants": {},
                    "fruits": {},
                    "creatures": {},
                    "env": {},
                }
        return grid
    
    def add_rectangle_region(self, x:int, y:int, w:int, h:int, given_energy: float):
        new_region = self.environment.create_new_region(x,y,w,h,given_energy)
        for y in range(self.y_size):
            for x in range(self.x_size):
                if x >=new_region.x and x<=new_region.x+new_region.w:              
                    if y>=new_region.y and y<=new_region.y+new_region.h:
                        self.grid[(x,y)]["env"][new_region.id] = new_region

    def update_grid(self, pygame_events="maybe later"):
        grid_list = list(self.grid.keys())
        rd.shuffle(grid_list)

        for position in grid_list:
            for type, values in self.grid[position].items():
                if values: 
                    if "fruits" in type:
                        for id, fruit in self.grid[position][type].items():
                            self.grid[position][type][id].update()
                    if "plants" in type:
                        for id, plant in self.grid[position][type].item():
                            self.grid[position][type][id].update()
        return grid_list

    def draw_grid(self, shuffled_list:list, pygame_canvas): 
        #maybe itd be better to have this function READ a file that has all grid states for all steps of simulation and print it
        #maybe i just initialize pygame here if i want to draw stuff
        for position in shuffled_list:
            for type, values in self.grid[position].items():
                if "fruits" in type:
                    for id, fruit in self.grid[position][type].items():
                        self.grid[position][type][id].drawn(pygame_canvas)
                if "plants" in type:
                    for id, plant in self.grid[position][type].item():
                        self.grid[position][type][id].drawn(pygame_canvas)

    def add_plant(self, x:int, y:int, gene:list=[0]):
        new_plant = Plant(x,y,gene)
        if not self.grid[(x,y)]["plants"]: 
            self.grid[(x,y)]["plants"][new_plant.id] = new_plant

    def add_fruit(self, x:int, y:int, gene:list=[0]):
        new_fruit = Fruit(x,y,gene)
        if not self.grid[(x,y)]["fruits"]:
            self.grid[(x,y)]["fruits"][new_fruit.id] = new_fruit

    def remove_plant(self, x, y, id):
        del self.grid[(x,y)]["plants"][id]

    def remove_fruit(self, x, y, id):
        del self.grid[(x,y)]["fruits"][id]

if __name__ == "__main__":
    A = Grid(4,4)
    A.add_rectangle_region(0,0,2,2,15)
    A.add_rectangle_region(2,2,2,2,15)
    A.add_plant(1,1)
    A.add_plant(1,1)

    A.add_plant(1,1)
    # A.add_plant(1,2)
    # A.add_plant(3,3)
    A.add_fruit(1,2,[0,1,1])
    A.add_fruit(2,2,[0,1,1])
    print(A.grid[(1,1)]["plants"])

    # for key, items in A.grid.items():
    #     for key2, items2 in A.grid[key]["plants"].items():
    #         if key==(1,1): data2remov = (key[0],key[1],key2)
    
    # #assim que remove um item
    # A.remove_plant(data2remov[0],data2remov[1],data2remov[2])
    # print(A.grid[(1,1)]["plants"])

    # for key, items in A.grid.items():
    #     print(key)
    #     for key2, items2 in A.grid[key].items():
    #         print(key2,items2)

    # #Assim que vamos embaralhar a ordem
    # A_lista = list(A.grid.keys())
    # rd.shuffle(A_lista)
    # print(A_lista)

    # for position in A_lista:
    #     print(f"{position} Cor do pixel: {A.grid[position]['color']}")
    #     for tipo, valores in A.grid[position].items():
    #         if valores:
    #             if "plants" in tipo:
    #                 for id, objeto in A.grid[position][tipo].items():
    #                     print(f"[PLANTA] posicao: {position}, id:{id}, obj: {objeto}")
    #             elif "fruits" in tipo:
    #                 for id, objeto in A.grid[position][tipo].items():
    #                     print(f"[FRUITS] posicao: {position}, id:{id}, obj: {objeto}")