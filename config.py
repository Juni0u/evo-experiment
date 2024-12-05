import json

class Parameters:
    def __init__(self, json_file="Parameters/general_parameters.json") -> None:
        self.parameter_file = json_file
        self.load_config()

    def load_config(self):
        with open(self.parameter_file, "r") as file:
            data = json.load(file)
        self.resolution = data["RESOLUTION"]
        self.screen_size = data["SCREEN_SIZE"]
        self.sun_energy = data["SUN_ENERGY"]
        self.experiment_folder=data["EXPERIMENT_FOLDER"]
        self.max_simulation_steps=data["MAX_SIMULATION_STEPS"]
        self.plant = PlantParameters()
        self.creature = CreatureParameters()

    def __str__(self) -> str:
        output = ""
        for key,value in vars(self).items():
            output += f"{key}={value}\n"
        return output
    
class PlantParameters:
    def __init__(self, json_file="Parameters/plants_parameters.json") -> None:
        self.parameter_file = json_file
        self.load_config()

    def load_config(self):
        with open(self.parameter_file, "r") as file:
            data = json.load(file)
        self.food_standard_color = data["FOOD_STANDARD_COLOR"]
        self.food_sprout_chance = data["FOOD_SPROUT_CHANCE"]
        self.age_max_death_prob = data["AGE_MAX_DEATH_PROB"]
        self.max_death_prob = data["MAX_DEATH_PROB"]
        self.spawn_radius = data["SPAWN_RADIUS"]
        self.base_color=data["BASE_COLOR"]
        # self.max_health_divisions=data["MAX_HEALTH_DIVISIONS"]
        self.colors=data["COLORS"]
        self.states = data["STATES"]
        self.standard_energy_capacity = data["STANDARD_ENERGY_CAPACITY"]
        self.standard_metabolism = data["STANDARD_METABOLISM"]
        self.standard_food_spawn_energy_thresold = data["STANDARD_FOOD_SPAWN_ENERGY_THRESOLD"]
        self.mutation_prob=data["MUTATION_PROB"]
        self.mutation_interval=data["MUTATION_INTERVAL"]
        self.brain_size_interval=data["BRAIN_SIZE_INTERVAL"]

    def __str__(self) -> str:
        output = ""
        for key,value in vars(self).items():
            output += f"{key}={value}\n"
        return output
    
class CreatureParameters:
    def __init__(self, json_file="Parameters/creature_parameters.json") -> None:
        self.parameter_file = json_file
        self.load_config()

    def load_config(self):
        with open(self.parameter_file, "r") as file:
            data = json.load(file)
        self.color = data["STANDARD_COLOR"]
        self.states = data["STATES"]
        self.standard_energy_capacity = data["STANDARD_ENERGY_CAPACITY"]
        self.standard_metabolism = data["STANDARD_METABOLISM"]
        self.standard_reproduction_thresold = data["REPRODUCTION_THRESOLD"]
        self.mutation_prob = data["MUTATION_PROB"]
        

    def __str__(self) -> str:
        output = ""
        for key,value in vars(self).items():
            output += f"{key}={value}\n"
        return output
    
def main():
    A = Parameters()
    print(A)

if __name__ == "__main__":
    main()
