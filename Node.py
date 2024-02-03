from copy import deepcopy

class Node:
    def __init__(self, state_location, env, agent_packages, parent=None, g=0, h=0):
        self.state_location = state_location
        self.parent = parent
        self.packages,  self.agent_packages = set(), set()
        self.delivered_packages = set()
        
        self.g = g  # cost from start node to current node
        self.h = h  # heuristic cost from current node to goal node

        self.update_packages_and_deliveries(parent, env, agent_packages)

    def f(self):
        return self.g + self.h

    # not sure maybe a way to do it better ? 
    # maybe save one matrix for packages taken, and one for the rest ? 
    def update_packages_and_deliveries(self, prev_state, env, agent_packages):
        if prev_state is not None: 
            for package in prev_state.packages:
                self.packages.add(package)

            for package in prev_state.agent_packages:
                self.agent_packages.add(package)


            for package in prev_state.delivered_packages:
                self.delivered_packages.add(package)
            
            #self.packages = deepcopy(prev_state.packages)
            #self.agent_packages = deepcopy(prev_state.agent_packages)

            for package in env.get_packages(self.state_location):
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