from copy import deepcopy

class Node:
    def __init__(self, state_location, env, agent_packages, parent=None, g=0, h=0):
        self.state_location = state_location
        self.parent = parent
        self.packages,  self.agent_packages = set(), set()
        self.delivered_packages = set()
        
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
        # add - check packages time - 
        # if still not showing - don't take 
        # if deadline passed - don't take 
        # show all packages all time 

        #maybe return when package didn't deliverd on time
        if self.parent is not None: 
            for package in self.parent.packages:
                #check if package can still be delivered 
                if package.deadline < self.g + env.counter:
                    return False
                self.packages.add(package)
                

            for package in self.parent.agent_packages:
                if package.deadline < self.g + env.counter:
                    return False
                self.agent_packages.add(package)


            for package in self.parent.delivered_packages:
                self.delivered_packages.add(package)
            
            #self.packages = deepcopy(prev_state.packages)
            #self.agent_packages = deepcopy(prev_state.agent_packages)

            for package in env.get_packages(self.state_location, env.counter + self.g):
                if package not in self.delivered_packages and package not in self.agent_packages:
                    self.agent_packages.add(package)
                    self.packages.remove(package)

            #packge_delivered = set()
            for package in self.agent_packages:
                if self.state_location == package.dst_location:
                    self.delivered_packages.add(package)
            self.agent_packages.difference_update(self.delivered_packages)
        else:
            for package in env.packages:
                self.packages.add(package)            
            #self.packages = deepcopy(env.packages)

            for package in agent_packages:
                self.agent_packages.add(package)
                self.packages.remove(package)
        return True

    def break_fragile_edges(self, env):
        if self.parent is not None:

            #copy the broken fragile edges
            self.fragile_broken_edges = deepcopy(self.parent.fragile_broken_edges)

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


        