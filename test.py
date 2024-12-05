ai = 1
af = 10
res = {}
ven = {}

for i in range(ai,af+1):
    res[i] = []
    ven[i] = []
    for j in range(ai, af+1):
        if i%j==0:
            ven[i].append(j)
        if j%i==0:
            res[i].append(j)
            
class VenomResistence():
    def __init__(self,venom,resistence) -> None:
        if not isinstance(venom,list):
            self.venom = [venom]
        else: self.venom = venom   
        if not isinstance(resistence,list):
            self.resistence = [resistence]
        else: self.resistence = resistence
        
    def __str__(self) -> str:
        if not self.venom: self.venom = list()
        if not self.resistence: self.resistence = list()
        output = f"Venom: {self.venom}\n"
        output += f"Resistence: {self.resistence}\n"
        output += f"Immunities: {self.getImmunity()} (more, more metabolism)\n"
        output += f"Antidotes2OwnVenom: {self.getAntidotes2OwnVenom()} (less, more metabolism)\n"
        output += f"Metabolism: {self.getMetabolism()}"
        return output
        
    def getImmunity(self):
        immunity = set()
        for venom in self.venom:
            immunity.add(venom)
        for resistence in self.resistence:
            immunity.update(res[resistence])
        return immunity
    
    def getAntidotes2OwnVenom(self):
        antidotes = set()
        for venom in self.venom:
            antidotes.update(ven[venom])
        return antidotes
    
    def getMetabolism(self):
        metabolism = 1
        max_food_from_environment = 15
        if not self.resistence: metabolism_from_res=0
        else: metabolism_from_res = (max_food_from_environment) * (len(self.getImmunity())/af)
        if not self.venom: metabolism_from_venom=0
        else: metabolism_from_venom = (max_food_from_environment) * (1 - len(self.getAntidotes2OwnVenom())/af)
        
        
        print(f"met from venom: {metabolism_from_venom}, from res: {metabolism_from_res}")        
        metabolism += metabolism_from_res+metabolism_from_venom
        return metabolism
        
a = VenomResistence(venom=[10,8,3,2],resistence=[3])
b = VenomResistence(venom=2,resistence=3)
c = VenomResistence(venom=1,resistence=5)


print(f"{a}\n\n{b}\n\n{c}\n")  
print(f"Venom: {ven}")
print(f"Res: {res}")