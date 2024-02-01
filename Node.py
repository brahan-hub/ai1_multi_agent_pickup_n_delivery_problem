class Node:
    def __init__(self, state_location, env_packages, agent_packages, parent=None, g=0, h=0):
        self.state_location = state_location
        self.parent = parent
        self.packages, self.deliveries = set(), set()
        self.agent_packages = agent_packages
        self.g = g  # cost from start node to current node
        self.h = h  # heuristic cost from current node to goal node

        self.update_packages_and_deliveries(parent, env_packages)

    def f(self):
        return self.g + self.h

    # not sure maybe a way to do it better ? 
    # maybe save one matrix for packages taken, and one for the rest ? 
    def update_packages_and_deliveries(self, prev_state, env_packages):
        if prev_state is not None: 
            self.packages = prev_state.packages
            self.deliveries = prev_state.deliveries

            if self.state_location in self.packages:
                self.packages.remove(self.state_location)
                self.agent_packages.add(self.state_location)

            if self.state_location in self.deliveries and len(self.agent_packages) > 0:
                packages_delivered = []
                for package in self.agent_packages:
                    if self.state_location == package.dst_location:
                        self.deliveries.remove(self.state_location)
                        packages_delivered.add(package)
                if len(packages_delivered) > 0:
                    self.agent_packages.remove(packages_delivered)
        else:
            for package in env_packages:
                self.packages.add(package.cur_location)
                self.deliveries.add(package.dst_location)

            if len(self.agent_packages) > 0:
                self.packages.remove(self.agent_packages)