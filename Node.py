from copy import deepcopy,copy
from enum import Enum 
import Agents

class Package_state(Enum):
    NOT_SHOWN = 1
    NOT_TAKEN = 2
    TAKEN = 3
    DELIVERED = 4


class Node:
    def __init__(self, state_location, env, agent_packages, parent=None, g=0, h=0):
        self.state_location = state_location
        self.parent = parent
        self.packages = dict()
        self.g = g  # cost from start node to current node
        self.h = h  # heuristic cost from current node to goal node

        #bonus state 
        self.saboteur_location = None
        self.fragile_broken_edges = set()
        self.is_bonus = env.bonus

        self.is_valid_node = self.update_packages_and_deliveries(env, agent_packages)
        self.break_fragile_edges(env)
        if env.bonus:
            self.bonus_saboteur_next_step(env)

    def f(self):
        return self.g + self.h

    def __eq__(self, __other: object) -> bool:
        if self.state_location == __other.state_location:
            if len(self.fragile_broken_edges.difference(__other.fragile_broken_edges)) == 0:
                if self.packages == __other.packages:
                    return True
        return False

    def is_goal_state(self):
        for package,package_state in self.packages.items():
            if package_state!=Package_state.DELIVERED:
                return False
        return True
    

    def f_eval_function(node):
        return node.g + node.h

    def h_eval_function(node):
        return node.h
    
        
    def update_packages_and_deliveries(self, env, agent_packages):

        if self.parent is not None: ## update packages from parent state
            # self.update_package_state_from_parent(env)
            for package, package_state in self.parent.packages.items(): 
                    can_del_on_time = self.can_deliver_on_time(package, package_state, self.g + env.counter) 
                    if package_state != Package_state.DELIVERED and not can_del_on_time: #check if package can still be delivered 
                        return False
                    if package_state == Package_state.NOT_SHOWN and package.start_time <= self.g + env.counter:
                        self.packages[package] = Package_state.NOT_TAKEN
                    else:
                        self.packages[package] = self.parent.packages[package]

            for package in env.get_packages(self.state_location, env.counter + self.g):
                package_state = self.packages[package]
                if package_state != Package_state.DELIVERED and package_state != Package_state.TAKEN:
                    self.packages[package] = Package_state.TAKEN

            for package,package_state in self.packages.items():
                if package_state ==  Package_state.TAKEN and self.state_location == package.dst_location :
                    self.packages[package] = Package_state.DELIVERED        
        else: # new state
            for package in env.packages:
                if package.start_time <= env.counter:
                    self.packages[package] = Package_state.NOT_TAKEN 
                else:
                    self.packages[package] = Package_state.NOT_SHOWN

            for package in agent_packages:
                self.packages[package] = Package_state.TAKEN
                
        return True

    def break_fragile_edges(self, env):
        # if self.parent is not None:
        if self.parent is None:
            return
        
        self.fragile_broken_edges = copy(self.parent.fragile_broken_edges)
        
        for edge in env.fragile_edges.difference(self.fragile_broken_edges): #check if agent broke fragile edge 
            if self.state_location in edge:
                if self.parent.state_location == edge[len(edge) - edge.index(self.state_location) -1]:
                    self.fragile_broken_edges.add(edge)


    def calculate_distance(self, package):
        manhattan_distance = lambda a, b: sum(abs(val1-val2) for val1, val2 in zip(a,b))
        m_dist_state_pack = manhattan_distance(self.state_location, package.cur_location)
        m_dist_pack_dst = manhattan_distance(package.cur_location, package.dst_location)
        m_dist_state_dst = manhattan_distance(self.state_location, package.dst_location)
        total_m_dist = m_dist_state_pack +m_dist_pack_dst
        return total_m_dist,m_dist_state_dst
    
    def can_deliver_on_time(self, package, package_state, time):
        
        if package.deadline < time:
            return False
        
        total_m_dist, m_dist_state_dst = self.calculate_distance(package)
        
        if package_state == Package_state.NOT_TAKEN and (total_m_dist > package.deadline - time):
            return False
        elif package_state == Package_state.TAKEN and (m_dist_state_dst > package.deadline - time):
            return False
        
        return True

          
    def get_rel_vertices(self):
        rel_ver = set()
        
        for package, package_state in self.packages.items():
            if package_state == Package_state.NOT_TAKEN or  package_state == Package_state.NOT_SHOWN:
                rel_ver.add(package.cur_location)
                rel_ver.add(package.dst_location)
            if package_state == Package_state.TAKEN:
                rel_ver.add(package.dst_location)


        rel_ver.add(self.state_location)

        return rel_ver


    def bonus_saboteur_next_step(self, env):
        if self.parent is None:
            self.saboteur_location = env.bonus_saboteur_location()
        else:
            greedy_agent = Agents.SaboteurBonusAgent(self.parent.saboteur_location[0], self.parent.saboteur_location[1], env, self.fragile_broken_edges)
            next_greedy_step = greedy_agent.get_next_action()
            if next_greedy_step != self.state_location and next_greedy_step != self.parent.saboteur_location:
                self.saboteur_location = next_greedy_step

                for edge in env.fragile_edges.difference(self.fragile_broken_edges):
                    if self.saboteur_location in edge:
                        if self.parent.saboteur_location == edge[len(edge) - edge.index(self.saboteur_location) -1]:
                            self.fragile_broken_edges.add(edge)

            else:
                self.saboteur_location = env.bonus_saboteur_location()
 