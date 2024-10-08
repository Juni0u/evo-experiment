import pygame, math, random
from global_vars import FOOD_STANDARD_COLOR, RESOLUTION

class Creature():
    def __init__(self,id,x:int,y:int,color:tuple,born_in:int,chromosome:str):
        """Gene:
        [0,0,0,0,0|0,0,0,0|0,0,0,0|0,0,0,0]
        |0-------4|5-----8|9----12|13---16|
        | max_sta | spd   |vis_rad|rpd_thr|"""
        self.id = id
        self.x = x
        self.y = y
        self.color = color
        self.age = 0
        self.born_in = born_in
        self.stamina = 0
        self.vision_radius=1
        self.rect = pygame.Rect(x,y,1,1)
        self.chromosome = chromosome
        
        self.state="idle"
        self.hunt_target= [999,999]
        if len(chromosome) != 17: raise ValueError("Chromosome does not have the right size.")

    def birth(self) -> None:
        self.max_stamina = int(self.chromosome[0:5],2)
        self.max_steps = int(self.chromosome[5:9],2)-1/1000
        self.vision_radius = int(self.chromosome[9:13],2)        
        self.reprodution_thresold = int(self.chromosome[13:16],2)
        
        self.stamina = self.max_stamina
        self.vision_rect = pygame.Rect(self.x-self.vision_radius,self.y-self.vision_radius,2*self.vision_radius,2*self.vision_radius)

    def update(self,FoodList,AgentList,seed):
        if self.age==0: self.birth()
        self.age += 1
        self.stamina -= 0.05
        
        if self.stamina <= 0:
            AgentList.remove(self)
            return FoodList, AgentList
        
        index = self.collision(FoodList,AgentList)        
        if self.state=="eating":
            self.eat(FoodList,index)
            self.state = "idle"
            self.hunt_target=0
        elif self.state=="hunting":
            self.hunt()
            self.state="idle"
        elif self.state=="searching":
            self.search()
            self.state="idle"         
        elif self.state=="reproducing":
            self.reproduce(AgentList,index)
            self.state="idle"
        return FoodList, AgentList

    def draw(self,canvas) -> None:
        try: pygame.draw.rect(canvas,(255,255,255),self.vision_rect)
        except AttributeError:
            print(self.age)
            print(self.chromosome)
            print(self.vision_radius)
            
        canvas.set_at((int(self.x),int(self.y)), self.color)  

    def collision(self,FoodList,AgentList):
        index = self.rect.collidelist(FoodList)
        if index != -1: 
            self.state = "eating"
            return index
        
        index = self.vision_rect.collidelist(FoodList)
        if index != -1:
            self.state = "hunting"
            self.hunt_target = FoodList[index]
            return index    
        
        index = self.rect.collidelist(AgentList)
        if (index != 1) and (self.stamina > self.reprodution_thresold/2) and (AgentList[index].stamina > AgentList[index].reprodution_thresold/2):
            self.state = "reproducing"
            return index
        
        self.state="searching"
        return None
    
    def reproduce(self,AgentList, index):
        self.stamina -= self.reprodution_thresold/2
        AgentList[index].stamina -= AgentList[index].reprodution_thresold/2
        
       
    def eat(self, FoodList, index):    
        self.stamina += FoodList[index].energy
        del FoodList[index]

    def hunt(self):
        direction, steps = self.direction_with_point(target=[self.hunt_target.x,self.hunt_target.y])
        if steps > self.max_steps: steps = self.max_steps
        self.move(direction,steps)
        
    def search(self):
        self.move([random.randint(-1,1),random.randint(-1,1)],self.max_steps)    
        
    def direction_with_point(self,target:list):
        """Returns an unitary vector [x,y] that points to the target [x,y]"""
        vector = [target[0]-self.x, target[1]-self.y]
        lenght = math.sqrt(vector[0]**2 + vector[1]**2)
        if lenght!=0:
            direction = [vector[0]/lenght, vector[1]/lenght]
        else:
            direction = [0,0]
        return direction, lenght

    def move(self,direction: list, steps:float) -> None:
        if steps > self.max_steps: steps = self.max_steps
        if self.stamina > 1:
            self.x += direction[0] * steps
            self.y += direction[1] * steps
            self.rect.topleft = (self.x,self.y)
            self.vision_rect.topleft = (self.x-self.vision_radius,self.y-self.vision_radius)
            self.env_limits()
            self.stamina -= 1
            
    def env_limits(self) -> None:
        if self.x > RESOLUTION[0]:
            self.x = RESOLUTION[0]-1
        elif self.x < 0:
            self.x = 0
            
        if self.y > RESOLUTION[1]:
            self.y = RESOLUTION[1]-1
        elif self.y < 0:
            self.y = 0