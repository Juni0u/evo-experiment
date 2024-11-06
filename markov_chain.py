import numpy as np, random as rd
from global_vars import MARKOV_MUTATION_PROB, MARKOV_MUTATION_INTERVAL, MARKOV_ZONE_MUTATION_PROB, MARKOV_ZONE_MUTATION_INTERVAL

#TODO: Make a class of markov environment: it has functions that act on probabilities matrix of a specific type.

class MarkovChainEnvironment():
    def __init__(self, mutation_probability: float = MARKOV_MUTATION_PROB, mutation_interval: list = MARKOV_MUTATION_INTERVAL) -> None:
        """[mutation_probability] = Chance for a mutation to happen;
        [mutation_interval] = range of mutation changes"""

        self.mutation_prob = mutation_probability
        self.mutation_interval = mutation_interval

    def build_random_prob_matrix(self, n_states:int) -> np.ndarray:
        """Build a matrix of [n_states]x[n_states] with random values assigned
        """
        output = np.zeros((n_states,n_states))
        for i in range(0,n_states):
            for j in range(0,n_states):
                output[i,j] = rd.random()
            sum = np.sum(output[i,:])
            output[i,:] = (output[i,:]/sum)
        return output
    
    def state_transition(self, row: np.ndarray) -> int:
        """Given the returns the [index] of the next state based on a given [row] of probabilities"""
        return np.random.choice(a=len(row),p=row)
    
    def normalize_matrix(self, matrix: np.ndarray) -> np.ndarray:
        """Given a [matrix], returns a normalized version where sum of the values in each row is 1"""
        for i in range(matrix.shape[0]):
            sum = np.sum(matrix[i,:])
            matrix[i,:] = (matrix[i,:]/sum)
        return matrix

    def mutate_probability_in_matrix(self, matrix: np.ndarray) -> np.ndarray:
        """Mutation:
            - Mutation chance: 1 roll for each matrix
                - If yes, chose 1 row randomly and then 2 columns randomly
            - Mutation value:
                - Decrease a column by a value between MARKOV_MUTATION_INTERVAL
                - Increase the other column by the same value
            - Respect minimum of 0 and maximum of 1"""
        
        n_states = matrix.shape[0]
        if rd.random() <= self.mutation_prob:
            row = rd.randint(0,n_states-1)
            col1 = rd.randint(0,n_states-1)
            col2 = rd.randint(0,n_states-1)
            while col2==col1: col2 = rd.randint(0,n_states-1)

            value = rd.uniform(self.mutation_interval[0],self.mutation_interval[1])
            if value >= matrix[row,col1]: value = matrix[row,col1] #type: ignore

            matrix[row,col1] -= value #type: ignore
            matrix[row,col2] += value #type: ignore

            if matrix[row,col1] < 0: matrix[row,col1] = 0   #type: ignore
            elif matrix[row,col1] > 1: matrix[row,col1] = 1 #type: ignore
            if matrix[row,col2] < 0: matrix[row,col2] = 0   #type: ignore
            elif matrix[row,col2] > 1: matrix[row,col2] = 1 #type: ignore
            self.normalize_matrix(matrix)
        return matrix
    
class MarkovChainIndividual(MarkovChainEnvironment):
    def __init__(self,  transition_grid = 0, states:list=[0], transition_zones:int=1, mutation_probability: float = MARKOV_MUTATION_PROB, mutation_interval: list = MARKOV_MUTATION_INTERVAL) -> None:
        super().__init__(mutation_probability, mutation_interval)
        """transition_grid: The group of probability matrix of all 'transition_zones' -> 0 = Random probability Matrix based on n_states
        n_states: Number of existing states
        transition_zones: Each zone has a probability matrix associated with.
        mutation_probability: Chance of mutation
        mutation_interval: Mutation change"""

        if (not isinstance(transition_grid,np.ndarray) and (transition_grid!=0)): raise ValueError("Matrix must be an numpy.ndarray or 0 (if wanted to generate a random one)")
        self.states = states
        if isinstance(transition_grid,int): #Create a random Matrix
            if len(states) < 2: raise ValueError("Need number of states bigger than 1 to generate a random transition grid.")
            self.n_states = len(self.states)
            self.transition_zones = transition_zones
            self.transition_grid = np.zeros((self.transition_zones,self.n_states,self.n_states))
            for i in range(transition_zones):
                self.transition_grid[i,:,:] = self.build_random_prob_matrix(self.n_states)
        else:
            self.n_states = transition_grid.shape[1]
            self.transition_zones = transition_grid.shape[0]
            self.transition_grid = transition_grid                     


        self.current_transition_grid = 0
        self.current_state = self.states[0]
        self.current_state_index = self.states.index(self.current_state)
        
    def change_state(self) -> None:
        self.current_state_index = self.state_transition(self.transition_grid[self.current_transition_grid,self.current_state_index,:])
        self.current_state = self.states[self.current_state_index]

    def mutate(self,transition_zone:int=9999) -> None:
        if transition_zone == 9999: transition_zone = rd.randint(0,self.transition_zones-1)
        self.mutate_probability_in_matrix(self.transition_grid[transition_zone,:,:])


def main():
    b=np.zeros((3,2,2))
    A=MarkovChainIndividual(transition_grid=0,states=["idle","move","run"],transition_zones=2)

if __name__ == "__main__":
    main()

