import numpy as np, random as rd
from config import Parameters

#TODO: Make a class of markov environment: it has functions that act on probabilities matrix of a specific type.

class MarkovChainEnvironment():
    def __init__(self, mutation_probability: float, mutation_interval: list) -> None:
        """[mutation_probability] = Chance for a mutation to happen;
        [mutation_interval] = range of mutation changes"""

        self.parameter = Parameters()
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
    
    def normalize_matrix(self, matrix: np.ndarray) -> np.ndarray:
        """Given a [matrix], returns a normalized version where sum of the values in each row is 1"""
        normalized_matrix = matrix.copy().astype(float)
        for i in range(normalized_matrix.shape[0]):
            row_sum = np.sum(normalized_matrix[i,:])
            normalized_matrix[i,:] = matrix[i,:]/row_sum
        return normalized_matrix

    def mutate_probability_in_matrix(self, mut_matrix: np.ndarray) -> np.ndarray:
        """Mutation:
            - Mutation chance: 1 roll for each matrix
                - If yes, chose 1 row randomly and then 2 columns randomly
            - Mutation value:
                - Decrease a column by a value between MARKOV_MUTATION_INTERVAL
                - Increase the other column by the same value
            - Respect minimum of 0 and maximum of 1"""
        matrix = mut_matrix.copy().astype(float)
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
    
class Brain(MarkovChainEnvironment):
    def __init__(self, mutation_probability: float, mutation_interval: list, states:list, transition_grid = 0, transition_zones:int=1) -> None:
        super().__init__(mutation_probability, mutation_interval)
        """transition_grid: The group of probability matrix of all 'transition_zones' -> 0 = Random probability Matrix based on n_states
        states: list of states names
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

        self.current_brain_zone = 0
        self.current_brain_state = self.states[0]
        self.current_brain_state_index = self.states.index(self.current_brain_state)
        
    def state_transition(self) -> None:
        """Transitions state based com self.current_brain_state"""
        current_state_row = self.transition_grid[self.current_brain_zone,self.current_brain_state_index,:]
        self.current_brain_state_index = np.random.choice(a=len(current_state_row),p=current_state_row)
        self.current_brain_state = self.states[self.current_brain_state_index]

    def mutate(self,transition_zone:int=9999) -> None:
        if transition_zone == 9999: transition_zone = rd.randint(0,self.transition_zones-1)
        self.transition_grid[transition_zone,:,:] = self.mutate_probability_in_matrix(self.transition_grid[transition_zone,:,:])

def main():
    # b=np.zeros((3,2,2))
    # A=Brain(1,[0.05,0.25],states=["idle","move","run"],transition_zones=2)
    # print(A.transition_grid)
    # print("MUTATION")
    # for i in range(A.transition_grid.shape[0]):
    #     #print(i)
    #     A.mutate(i)
    # print(A.transition_grid)
    env = MarkovChainEnvironment(mutation_probability=1,mutation_interval=[0.05,0.95])
    matrix1 = np.array([[1,2,3],
                        [1,2,3],
                        [1,2,3]])
    matrix2 = np.array([[2,2,2],
                        [2,2,2],
                        [2,2,2]])
    
    ans1 = env.normalize_matrix(matrix=matrix1)
    ans2 = env.normalize_matrix(matrix=matrix2)
    print(ans1)

if __name__ == "__main__":
    main()

