""" 			  		 			 	 	 		 		 	  		   	  			  	
Template for implementing QLearner  (c) 2015 Tucker Balch 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
Copyright 2018, Georgia Institute of Technology (Georgia Tech) 			  		 			 	 	 		 		 	  		   	  			  	
Atlanta, Georgia 30332 			  		 			 	 	 		 		 	  		   	  			  	
All Rights Reserved 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
Template code for CS 4646/7646 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
Georgia Tech asserts copyright ownership of this template and all derivative 			  		 			 	 	 		 		 	  		   	  			  	
works, including solutions to the projects assigned in this course. Students 			  		 			 	 	 		 		 	  		   	  			  	
and other users of this template code are advised not to share it with others 			  		 			 	 	 		 		 	  		   	  			  	
or to make it available on publicly viewable websites including repositories 			  		 			 	 	 		 		 	  		   	  			  	
such as github and gitlab.  This copyright statement should not be removed 			  		 			 	 	 		 		 	  		   	  			  	
or edited. 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
We do grant permission to share solutions privately with non-students such 			  		 			 	 	 		 		 	  		   	  			  	
as potential employers. However, sharing with other current or future 			  		 			 	 	 		 		 	  		   	  			  	
students of CS 7646 is prohibited and subject to being investigated as a 			  		 			 	 	 		 		 	  		   	  			  	
GT honor code violation. 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
-----do not edit anything above this line--- 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
Student Name: Martin Mathew (replace with your name)
GT User ID: mmathew32 (replace with your User ID)
GT ID: 903241329 (replace with your GT ID)
"""

import numpy as np
import random as rand

from numpy import random


def author():
    return "mmathew32"


class QLearner(object):

    def author(self):
        return "mmathew32"

    def __init__(self, \
                 num_states=100, \
                 num_actions=4, \
                 alpha=0.2, \
                 gamma=0.9, \
                 rar=0.5, \
                 radr=0.99, \
                 dyna=0, \
                 verbose=False):

        self.verbose = verbose
        self.num_actions = num_actions
        self.s = 0
        self.a = 0
        self.alpha = alpha
        self.gamma = gamma
        self.rar = rar
        self.radr = radr
        self.num_states = num_states
        self.dyna = dyna
        self.exp_tuple = {}
        # self.ttc = np.full((num_states, num_actions, num_states), 0.0000001)
        # self.reward = np.full((num_states, num_actions), 0.0)
        self.q = np.zeros((num_states, num_actions),dtype=float)

    def querysetstate(self, s,training=False):
        """ 			  		 			 	 	 		 		 	  		   	  			  	
        @summary: Update the state without updating the Q-table 			  		 			 	 	 		 		 	  		   	  			  	
        @param s: The new state 			  		 			 	 	 		 		 	  		   	  			  	
        @returns: The selected action 			  		 			 	 	 		 		 	  		   	  			  	
        """
        self.s = s
        if training:
            action = rand.randint(0, self.num_actions - 1)
        else:
            res = np.where(self.q[s] == np.amax(self.q[s]))[0]
            action = res[0]
        if self.verbose: print ("s =", s, "a =", action)
        self.a = action
        return action

    def query(self, s_prime, r):
        """ 			  		 			 	 	 		 		 	  		   	  			  	
        @summary: Update the Q table and return an action 			  		 			 	 	 		 		 	  		   	  			  	
        @param s_prime: The new state 			  		 			 	 	 		 		 	  		   	  			  	
        @param r: The ne state 			  		 			 	 	 		 		 	  		   	  			  	
        @returns: The selected action 			  		 			 	 	 		 		 	  		   	  			  	
        """
        self.q[self.s][self.a] = (1.0 - self.alpha) * self.q[self.s][self.a] + self.alpha * (
                    r + self.gamma * np.amax(self.q[s_prime]))
        self.rar *= self.radr
        r_act = np.random.rand()
        if r_act < self.rar:
            action = rand.randint(0, self.num_actions - 1)
        else:
            res = np.where(self.q[s_prime] == np.amax(self.q[s_prime]))[0]
            action = res[0]
        if self.verbose: print ("s =", s_prime, "a =", action, "r =", r)
        if self.dyna > 0:
            kee = "{}:{}".format(self.s, self.a)
            if kee in self.exp_tuple:
                r_s_prime_tup = self.exp_tuple.get(kee)
                r_s_prime_tup.append((r,s_prime))
                self.exp_tuple.update({kee: r_s_prime_tup})
            else:
                self.exp_tuple.update({kee: [(r, s_prime)]})
            self.experience_replay(self.dyna,self.exp_tuple)

        self.a = action
        self.s = s_prime
        return action

    def experience_replay(self, dyna, exp_tuples_list):
        keys = np.random.choice(list(exp_tuples_list.keys()), dyna)
        for key in keys:
            try:
                state_action = key.split(":")
                state_action_list = exp_tuples_list[key]
                index = random.randint(0,len(state_action_list))
                value = state_action_list[index]
                self.q[int(state_action[0])][int(state_action[1])] = (1.0 - self.alpha) * self.q[int(state_action[0])][int(state_action[1])] + self.alpha * (
                    value[0] + self.gamma * np.amax(self.q[value[1]]))
            except:
                print ("Error")








if __name__ == "__main__":
    print ("Remember Q from Star Trek? Well, this isn't him")
