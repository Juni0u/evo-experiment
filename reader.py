import pickle

class SimulationReader():
    def __init__(self, pickle_file) -> None:
        self.pickle_file = pickle_file
        with open (self.pickle_file, "rb") as f:
            self.simulation_grid = pickle.load(f)

if __name__ == "__main__":
    file = "/home/nonato/GitRepositories/evo-experiment/Evo-experiment-Results/Experiment 2024-11-27_10-28-21/simulation-83cf111a-c07a-4246-9deb-e126a90b6e78"
    A = SimulationReader(pickle_file=file)
    
    # for i,grid in enumerate(A.simulation_grid.all_grid_steps):
    #     for x in range(A.simulation_grid.x_size):
    #         for y in range(A.simulation_grid.y_size):
    #             if ("plant" in grid[x][y]) and (x>50):
    #                 print(x,y)
    #                 print(i, grid[x][y]["plant"].id)
    #                 print()