from copy import deepcopy,copy
from enum import Enum 

class Package_state(Enum):
    NOT_SHOWN = 1
    NOT_TAKEN = 2
    TAKEN = 3
    DELIVERED = 4

#Package_State = Enum(NOT_SHOWN = 1
#                     NOT_TAKEN = 2
#                     TAKEN = 3
#                     DELIVERED = 4)

class Node:
    def __init__(self, state_location, env, agent_packages, parent=None, g=0, h=0):
        self.state_location = state_location
        self.parent = parent
        #self.packages,  self.agent_packages = set(), set()
        #self.delivered_packages = set()
        self.packages = dict()
        self.g = g  # cost from start node to current node
        self.h = h  # heuristic cost from current node to goal node

        #bonus state 
        self.fragile_broken_edges = set()

        self.is_valid_node = self.update_packages_and_deliveries(env, agent_packages)
        self.break_fragile_edges(env)

    def f(self):
        return self.g + self.h

    # not sure maybe a way to do it better ? 
    # maybe save one matrix for packages taken, and one for the rest ? 
    def update_packages_and_deliveries(self, env, agent_packages):
        #is_ok = True
    #        NOT_SHOWN = 1
    #NOT_TAKEN = 2
    #TAKEN = 3
    #DELIVERED = 4

        #maybe return when package didn't deliverd on time
        if self.parent is not None: ## update packages from parent state

            for package, package_state in self.parent.packages.items(): 
                #check if package can still be delivered 
                if package.deadline < self.g + env.counter:
                    return False
                if package_state == Package_state.NOT_SHOWN and package.start_time <= self.g + env.counter:
                    self.packages[package] = Package_state.NOT_TAKEN
                self.packages[package] = self.parent.packages[package]

            for package in env.get_packages(self.state_location, env.counter + self.g):
                package_state = self.packages[package]
                if package_state != Package_state.DELIVERED and package_state != Package_state.TAKEN:
                    self.packages[package] = Package_state.TAKEN

            #packge_delivered = set()
            #for package in self.agent_packages:
            for package,package_state in self.packages.items():
                if package_state ==  Package_state.TAKEN and self.state_location == package.dst_location :
    #self.delivered_packages.add(package)
                    self.packages[package] = Package_state.DELIVERED
            #self.agent_packages.difference_update(self.delivered_packages)
        else: # new state
            for package in env.packages:
                if package.start_time <= env.counter:
                    self.packages[package] = Package_state.NOT_TAKEN 
                else:
                    self.packages[package] = Package_state.NOT_SHOWN
        #self.packages = deepcopy(env.packages)

            for package in agent_packages:
                self.packages[package] = Package_state.TAKEN 
        return True

    def break_fragile_edges(self, env):
        if self.parent is not None:

            #copy the broken fragile edges
            self.fragile_broken_edges = copy(self.parent.fragile_broken_edges)
            
            # check if the greedy agent broke any fragile edge 
            for edge in env.fragile_edges.difference(self.fragile_broken_edges):
                #check if agent broke fragile edge 
                if self.state_location in edge:
                    if self.parent.state_location == edge[len(edge) - edge.index(self.state_location) -1]:
                        self.fragile_broken_edges.add(edge)

    def get_rel_ver_num(self):
        count = 0

        count += len(self.packages) * 2
        count += len(self.agent_packages)
        count += 1

        return count

    def __eq__(self, __other: object) -> bool:
        if self.state_location == __other.state_location:
            if len(self.fragile_broken_edges.difference(__other.fragile_broken_edges)) == 0:
                if self.packages == __other.packages:
                    return True
        return False

    
    def get_rel_vertices(self):
        rel_ver = set()
        
        for package, package_state in self.packages.items():
            if package_state == Package_state.NOT_TAKEN or  package_state == Package_state.NOT_SHOWN:
                rel_ver.add(package.cur_location)
                rel_ver.add(package.dst_location)

        rel_ver.add(self.state_location)

        return rel_ver

    def is_goal_state(self):
        for package,package_state in self.packages.items():
            if package_state!=Package_state.DELIVERED:
                return False
        return True
    

    def f_eval_function(node):
        return node.g + node.h

    def h_eval_function(node):
        return node.h       