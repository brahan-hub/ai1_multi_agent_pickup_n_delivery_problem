import pickle
from collections import defaultdict
import numpy as np

import gymnasium as gym
from gymnasium import Env
from tqdm import tqdm

BLACKJACK_STATE_DIMS = (21, 11, 2)
BLACKJACK_FLAT_DIMS = 31 * 11 * 2
BLACKJACK_ACTIONS_DIMS = 2
BLACKJACK_ACE_DIMS = 2
MIN_CARDS_SUM = 4
BLACKJACK_STATE_DIMS = 32
BLACKJACK_DEALER_DIMS = 11

REWARDS_DICT = {29: -1.0, 30:0.0, 31: 1.0}

def simulate_transition_matrix(n_episodes=1000_000):
    prob_dict = defaultdict(lambda: {a: {} for a in range(2)}) 
    env: Env = gym.make('Blackjack-v1')
    #pa = env.P
    env.reset()
    resultsDict = {-1.0 : 33, 0.0: 34, 1.0:35}
    for _ in tqdm(range(n_episodes)):
        obs, _ = env.reset()
        done = False
        # play one episode
        while not done:
            action = env.action_space.sample()
            next_obs, reward, terminated, truncated, _ = env.step(action)
            act_dict = prob_dict[obs][action]
            # update if the environment is done and the current obs
            done = terminated or truncated
            
            if done:
                next_state = (resultsDict.get(reward), obs[1], obs[2])
            else:
                next_state = next_obs

            if next_state in act_dict.keys():
                act_dict[next_state] += 1
            else:
                act_dict[next_state] = 1

            obs = next_obs

    # convert occuring frequency to probabilities
    tr_matrix = np.zeros((BLACKJACK_ACTIONS_DIMS, BLACKJACK_DEALER_DIMS,BLACKJACK_STATE_DIMS - 3, BLACKJACK_STATE_DIMS)) 
    P = {}
    is_end_state = lambda a : False if(a <= 31) else True
    for start_state in prob_dict.keys():
        P[start_state] = {}
        for a in [0, 1]:
            trx_state_list = []
            end_states = prob_dict[start_state][a]
            start_loc = start_state[0] + start_state[2] * 10 -MIN_CARDS_SUM
            tot_trxs = sum(end_states.values())
            for end_state, val in end_states.items():
                if (is_end_state(end_state[0])):
                    end_loc = end_state[0]
                else:
                    end_loc = end_state[0] + end_state[2] * 10
                tr_matrix[a][start_state[1]][start_loc][end_loc -MIN_CARDS_SUM] = round(val / tot_trxs, ndigits=3)

    #policy_iteration(tr_matrix, 1, 0.005)
    print("probablity matrix for action 0", '\n')
    print_tr_matrix(tr_matrix, 0)
    print("probablity matrix for action 1", '\n')
    print_tr_matrix(tr_matrix, 1)

    with open('tr_matrix_3dm10m-test.pickle', 'wb') as f:
        pickle.dump(tr_matrix, f)
    return P

def print_tr_matrix(tr_matrix, action):
    count =0;
    pr = []
    for d in range(0, BLACKJACK_DEALER_DIMS):
        for i in range(0, BLACKJACK_STATE_DIMS - 3):
            for j in range(0, BLACKJACK_STATE_DIMS):
                pr.append(tr_matrix[action][d][i][j])
                count += tr_matrix[action][d][i][j]

            print(pr, " ", count)
            count = 0;
            pr = []
        print()
        print()


#def aprox_policy_eval(tr):
#    policy_matrix = np.ones((BLACKJACK_STATE_DIMS, BLACKJACK_ACTIONS_DIMS))/ BLACKJACK_ACTIONS_DIMS
#    vf_matrix = np.zeros(BLACKJACK_STATE_DIMS)
#    vf_matrix[28] = -1
#    vf_matrix[30] = 1
#    state_values = policy_evaluation(policy_matrix, 1, 0.05, vf_matrix, tr_matrix)
    


def policy_evaluation(policy, gamma, theta, state_values, tr_matrix):
    """
    policy_evaluation: 		estimate state values based on the policy
    
    @param env:       		OpenAI Gym environment
    @param policy:    		policy matrix containing actions and their probability in each state
    @param gamma:     		discount factor
    @param theta: 			evaluation will stop once values for all states are less than theta
    @param state_values: 	initial state values

    @return:         		new state values of the given policy
    """
    delta = theta*2
    state_len = BLACKJACK_STATE_DIMS - 3
    dealer_len = BLACKJACK_DEALER_DIMS
    action_len = BLACKJACK_ACTIONS_DIMS
    while (delta > theta):
        delta = 0
        # for all state
        for d in range(dealer_len):
            for s in range(state_len):
            
                # we will get new state value
                new_s = 0
                # for all actions
                for a in range(action_len):
                    # get the current transitions list (U,D,L,R)
                    transitions_list = tr_matrix[a][d][s]
                    # for all transitions from currect state
                    for i in range(transitions_list.size):
                        new_s += policy[d,s,a] * transitions_list[i]*(gamma * state_values[d][i])
                        #transition_prob, next_state, reward, done = i
                        #new_s += policy[s,a]*transition_prob*(reward+gamma*state_values[next_state])
        
                delta = max(delta, np.abs(new_s - state_values[d][s])) 
                state_values[d][s] = new_s
    return state_values

def policy_improvement(tr_matrix, policy, state_values, gamma):
    """
    policy_improvement:  improve policy
    
    @param env:          OpenAI Gym environment
    @param policy:       policy matrix containing actions and their probability in each state
    @param gamma:        discount factor
    @param state_values: the evaluation will stop once values for all states are less than the threshold
    
    @return policy_stable: flag for if policy is stable
    @return policy:        improved policy
    """
    
    policy_stable = True
    state_len = BLACKJACK_STATE_DIMS - 3
    action_len = BLACKJACK_ACTIONS_DIMS
    dealer_len = BLACKJACK_DEALER_DIMS
    # for all states
    for d in range(dealer_len):
        for s in range(state_len):
            # actions from current state
            old_action = np.argmax(policy[d][s])
            temp_array = np.zeros((action_len))
            # for all actions from current state
            for a in range(action_len):
                transitions_list = tr_matrix[a][d][s]
                    # for all transitions from currect state
                for i in range(0, transitions_list.size):
                    temp_array[a] += transitions_list[i] * (gamma * state_values[d][i])

            policy[d,s] = np.zeros((action_len))
            policy[d,s, np.argmax(temp_array)] = 1.
            if old_action != np.argmax(policy[d][s]): 
                policy_stable = False
            
    return policy_stable, policy

def policy_iteration(tr_matrix, gamma, theta):
    # initial state values
    policy_matrix = np.ones((BLACKJACK_DEALER_DIMS, BLACKJACK_STATE_DIMS, BLACKJACK_ACTIONS_DIMS))/ BLACKJACK_ACTIONS_DIMS
    vf_matrix = np.zeros((BLACKJACK_DEALER_DIMS, BLACKJACK_STATE_DIMS))

    vf_matrix[:,29] = -1
    vf_matrix[:,31] = 1

    # create a random policy
    policy_stable = False
    
    while not policy_stable:
        # policy evaluation
        vf_matrix = policy_evaluation(policy_matrix, 1, 0.05, vf_matrix, tr_matrix)
        # policy improvement
        policy_stable, policy_matrix = policy_improvement(tr_matrix, policy_matrix, vf_matrix, gamma)

    print_policy(policy_matrix)
    return vf_matrix, policy_matrix



def print_policy(policy_matrix):
    action = lambda a : 0 if(a[0] == 1) else 1
    pr = []
    for j in range(BLACKJACK_STATE_DIMS):
        pr.append(j)
    print(pr, " ")
    pr = []

    for i in range(BLACKJACK_DEALER_DIMS):
        pr.append(i)
        for j in range(BLACKJACK_STATE_DIMS - 3):
            #print(action(policy_matrix[i][j]), ' ', , end =" "),
            pr.append(action(policy_matrix[i][j]))
            #pr.append(' ')
        print(pr, " ")
        #print()
        pr = []

         

if __name__ == '__main__':
    #with open('tr_matrix_3dm-test.pickle', 'rb') as f:
    ##with open('tr_matrix-test.pickle', 'rb') as f:
    #    tr_matrix = pickle.load(f)
    ##print("probablity matrix for action 0", '\n')
    ##print_tr_matrix(tr_matrix, 0)
    ##print("probablity matrix for action 1", '\n')
    ##print_tr_matrix(tr_matrix, 1)
    #policy_iteration(tr_matrix, 1, 0.005)
    simulate_transition_matrix(10000000)



