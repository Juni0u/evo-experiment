import numpy as np, random as rd
from global_vars import MARKOV_MUTATION_PROB, MARKOV_MUTATION_INTERVAL

#TODO: Make a class of markov environment: it has functions that act on probabilities matrix of a specific type.

class MarkovChainEnvironment():
    def __init__(self, mutation_probability:float=MARKOV_MUTATION_PROB, mutation_interval:list=MARKOV_MUTATION_INTERVAL) -> None:
        """[mutation_probability] = Chance for a mutation to happen;
        [mutation_interval] = range of mutation changes"""
        self.mutation_prob = mutation_probability
        self.mutation_interval = mutation_interval

    def build_random_prob_matrix(self, dimension:int) -> np.ndarray:
        """Build a matrix of [dimension]x[dimension] with random values assigned
        """
        output = np.zeros((dimension,dimension))
        for i in range(0,dimension):
            for j in range(0,dimension):
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

    def mutate_matrix(self):
        """Mutation:
            - Mutation chance: 1 roll for each matrix
                - If yes, chose 1 row randomly and then 2 columns randomly
            - Mutation value:
                - Decrease a column by a value between MARKOV_MUTATION_INTERVAL
                - Increase the other column by the same value
            - Respect minimum of 0 and maximum of 1"""
        
        if random.random() <= self.mutation_prob:
            row = random.randint(0,len(self.states)-1)
            col1 = random.randint(0,len(self.states)-1)
            col2 = random.randint(0,len(self.states)-1)
            while col2==col1: col2 = random.randint(0,len(self.states)-1)

            value = random.uniform(self.mutation_interval[0],self.mutation_interval[1])
            if value >= self.probability_matrix[row,col1]: value = self.probability_matrix[row,col1] #type: ignore

            self.probability_matrix[row,col1] -= value #type: ignore
            self.probability_matrix[row,col2] += value #type: ignore

            if self.probability_matrix[row,col1] < 0: self.probability_matrix[row,col1] = 0 #type: ignore
            elif self.probability_matrix[row,col1] > 1: self.probability_matrix[row,col1] = 1 #type: ignore
            if self.probability_matrix[row,col2] < 0: self.probability_matrix[row,col2] = 0 #type: ignore
            elif self.probability_matrix[row,col2] > 1: self.probability_matrix[row,col2] = 1 #type: ignore
            self.check_matrix(self.probability_matrix)
    
class MarkovChainIndividual(MarkovChainEnvironment):
    def __init__(self, matrix:np.ndarray, mutation_probability: float = MARKOV_MUTATION_PROB, mutation_interval: list = MARKOV_MUTATION_INTERVAL) -> None:
        super().__init__(mutation_probability, mutation_interval)
        pass


def main():
    M = MarkovChainEnvironment()
    A = M.build_random_prob_matrix(3)
    
    M.normalize_matrix(A)
    
    

if __name__ == "__main__":
    main()
