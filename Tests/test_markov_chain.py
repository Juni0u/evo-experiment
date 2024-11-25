import unittest
import numpy as np
from unittest.mock import patch
from markov_chain import MarkovChainEnvironment, Brain

#python -m unittest Tests.test_markov_chain
class TestMarkovChainEnvironment(unittest.TestCase):
    
    def test_build_random_prob_matrix(self):
        env = MarkovChainEnvironment(mutation_probability=1,mutation_interval=[0.05,0.95])
        n_states_list = [0,1,5,10,15,20,1000]
        matrix_list = []
        for n_state in n_states_list:
            matrix = env.build_random_prob_matrix(n_states=n_state)
            self.assertEqual(matrix.shape, (n_state,n_state))
            for row in matrix:
                self.assertAlmostEqual(np.sum(row), 1.0, delta=1e-3)
                
    def test_normalize_matrix(self):
        env = MarkovChainEnvironment(mutation_probability=1,mutation_interval=[0.05,0.95])
        matrix1 = np.array([[1,2,3],
                            [1,2,3],
                            [1,2,3]], dtype=float)
        matrix2 = np.array([[2,2,2],
                           [2,2,2],
                           [2,2,2]], dtype= float)
        norm_matrix1 = np.array([[0.1667,0.3333,0.5],
                                [0.1667,0.3333,0.5],
                                [0.1667,0.3333,0.5]])
        norm_matrix2 = np.array([[0.3333,0.3333,0.3333],
                                [0.3333,0.3333,0.3333],
                                [0.3333,0.3333,0.3333]])
        
        ans1 = env.normalize_matrix(matrix=matrix1)
        ans2 = env.normalize_matrix(matrix=matrix2)
        
        
        np.testing.assert_allclose(ans1,norm_matrix1,atol=1e-4)
        np.testing.assert_allclose(ans2,norm_matrix2,atol=1e-4)
        
    def test_mutate_probability_in_matrix(self):
        env = MarkovChainEnvironment(mutation_probability=1,mutation_interval=[0.05,0.95])
        matrix1 = np.array([        
            [0.2, 0.3, 0.5],
            [0.3, 0.4, 0.3],
            [0.4, 0.3, 0.3]])
        
        ans1 = np.array([
            [0.2, 0.3, 0.5],
            [0.2, 0.4, 0.4],
            [0.4, 0.3, 0.3]
            ])
        
        ans2 = np.array([
            [0.2, 0.05, 0.75],
            [0.3, 0.4, 0.3],
            [0.4, 0.3, 0.3]])
        
        with patch("random.random", return_value=0.5),\
             patch("random.randint", side_effect=[1,0,2]),\
             patch("random.uniform", return_value=0.1):
             mutated_matrix1 = env.mutate_probability_in_matrix(matrix1)
        
        np.testing.assert_allclose(mutated_matrix1,ans1, atol=1e-4)
        
        with patch("random.random", return_value=0.5),\
             patch("random.randint", side_effect=[0,1,2]),\
             patch("random.uniform", return_value=0.25):
             mutated_matrix2 = env.mutate_probability_in_matrix(matrix1)
             
        np.testing.assert_allclose(mutated_matrix2,ans2, atol=1e-4)

class TestBrain(unittest.TestCase):
    
    def test_brain_initialization(self):
        brain1 = Brain(mutation_probability=0.9,mutation_interval=[0.05,0.95],states=["idle","eat","reproduce"], transition_grid=0, transition_zones=2)
        brain2 = Brain(mutation_probability=0.9,mutation_interval=[0.05,0.95],states=["idle","eat","reproduce","move"], transition_grid=0, transition_zones=5)
        brain3 = Brain(mutation_probability=0.9,mutation_interval=[0.05,0.95],states=["idle","eat","reproduce","move","run"], transition_grid=0, transition_zones=15)

        np.testing.assert_allclose(brain1.transition_grid.shape,(2,3,3))
        np.testing.assert_allclose(brain2.transition_grid.shape,(5,4,4))
        np.testing.assert_allclose(brain3.transition_grid.shape,(15,5,5))

    def test_state_transitions(self):
        brain1 = Brain(mutation_probability=0.9,mutation_interval=[0.05,0.95],states=["idle","eat","reproduce"], transition_grid=0, transition_zones=2)
        brain3 = Brain(mutation_probability=0.9,mutation_interval=[0.05,0.95],states=["idle","eat","reproduce","move","run"], transition_grid=0, transition_zones=15)

        with patch("numpy.random.choice", return_value=1):
            brain1.state_transition()
            
        self.assertEqual(brain1.current_brain_state_index, 1)
        self.assertEqual(brain1.current_brain_state,"eat")
        
        with patch("numpy.random.choice", return_value=4):
            brain3.state_transition()
            
        self.assertEqual(brain3.current_brain_state_index, 4)
        self.assertEqual(brain3.current_brain_state,"run")       
        
if __name__ == "__main__":
    unittest.main()