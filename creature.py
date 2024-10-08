import pygame, math, random, uuid
from global_vars import FOOD_STANDARD_COLOR, RESOLUTION, MUTATION_RATE

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

    def update(self,year,FoodList,AgentList,seed):
        if self.born_in-year==0: self.birth()
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
            self.reproduce(year, AgentList,index)
            self.state="idle"
        return FoodList, AgentList

    def draw(self,canvas) -> None:
        try: pygame.draw.rect(canvas,(255,255,255),self.vision_rect)
        except AttributeError:
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
        
        AgentList.remove(self)
        index = self.rect.collidelist(AgentList)
        if (index != -1) and (self.stamina > self.reprodution_thresold/2) and (AgentList[index].stamina > AgentList[index].reprodution_thresold/2):
            self.state = "reproducing"
            self.move(direction=[])#TODO: os agentes tao ficando presos no estado de reproducing ai ficam assim ate morrer
            AgentList.append(self)
            return index
        
        AgentList.append(self)
        self.state="searching"
        return None
    
    def reproduce(self,year,AgentList,index):
        print(f"{year},reproducing")
    #     self.stamina -= self.reprodution_thresold/2
    #     AgentList[index].stamina -= AgentList[index].reprodution_thresold/2
    #     self.crossover(age=year,partner=AgentList[index],AgentList=AgentList)

    # def mutate(self,chromosome):
    #     if random.random() <= MUTATION_RATE:
    #         chromosome = list(chromosome)
    #         index = random.randint(1,len(chromosome)-1)
    #         if chromosome[index]=="0": chromosome[index]="1"
    #         else: chromosome[index]="0"
    #         chromosome = "".join(chromosome)
    #     return chromosome

    # def crossover(self,age,partner,AgentList):
    #     cut = random.randint(1,len(self.chromosome)-2)
    #     child1 = ""
    #     child2 = ""
    #     for i in range(0,cut,1):
    #         child1 += self.chromosome[i]
    #         child2 += partner.chromosome[i]
    #     for i in range(cut,len(self.chromosome),1):
    #         child1 += partner.chromosome[i]
    #         child2 += self.chromosome[i]

    #     child1 = self.mutate(child1)
    #     child2 = self.mutate(child2)

    #     AgentList.append(Creature(id=uuid.uuid4(),x=random.randint(self.x-1,self.x+1),y=random.randint(self.y-1,self.y+1),color=(255,0,0),born_in=age,chromosome=child1))
    #     AgentList.append(Creature(id=uuid.uuid4(),x=random.randint(self.x-1,self.x+1),y=random.randint(self.y-1,self.y+1),color=(255,0,0),born_in=age,chromosome=child2))
    #     return AgentList
        
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