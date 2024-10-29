import numpy, random
from global_vars import MARKOV_MUTATION_PROB, MARKOV_MUTATION_INTERVAL


class MarkovChain():
    def __init__(self,states_list:list[str],probability_matrix:list[float]=[0]) -> None:
        self.states = states_list
        self.mutation_prob = MARKOV_MUTATION_PROB
        self.mutation_interval = MARKOV_MUTATION_INTERVAL
        if (len(probability_matrix) == 1):
            self.probability_matrix = self.build_random_prob_matrix(dimension=len(self.states)) #type: ignore
        else:
            self.probability_matrix = probability_matrix

    def build_random_prob_matrix(self, dimension:int):
        output = numpy.zeros((dimension,dimension))
        for i in range(0,dimension):
            for j in range(0,dimension):
                output[i,j] = random.random()
            total = sum(output[i,:])
            for j in range(0,dimension):
                output[i,j] = output[i,j]/total
        self.check_matrix(output)
        return output
    
    def state_transition(self,current_state: str) -> str:
        c_state = self.states.index(current_state)
        chance = random.random()
        row_sum = 0
        #print(f"all states: {self.states}")
        for j in range(0,len(self.probability_matrix)):
            #print(f"j={j}, chance = {chance}, ts = {self.probability_matrix[c_state,j]+row_sum} \n {self.probability_matrix[c_state,:]}\n") #type: ignore
            if chance <= self.probability_matrix[c_state,j]+row_sum:  #type: ignore
                return self.states[j]
            else:
                row_sum += self.probability_matrix[c_state,j]        #type: ignore
        return self.states[-1]

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

    def check_matrix(self, matrix):
        for i in range(0,len(self.states)):
            sum = self.get_row_sum(i, matrix)
            if (sum < 0.9999) or (sum > 1.0001) :
                raise ValueError(f"The sum of row {i}, row of state {self.states[i]} is {sum}. It should be 1. \n {self.probability_matrix}")

    def get_row_sum(self, row:int, matrix) -> float:
        output = numpy.sum(matrix[row,:]) #type: ignore
        return output #type: ignore
    
# states = ["a","b","c"]
# A = MarkovChain(states)
# print(A.state_transition("a"))
