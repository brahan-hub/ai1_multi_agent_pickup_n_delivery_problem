import heapq
import Environment
import Package
# import Coordinate
from abc import ABC, abstractmethod

##### _________________________ ABSTRACT AGENT _________________________ #####
# NUM_OF_AGENTS = 0

class AbstractAgent:
    # n_agents = 0
    def __init__(self, start_x, start_y,environment):
        self.cur_location = (start_x,start_y)
        self.score = 0
        self.packages = set()
        self.environment = environment
        # self.n_agents +=1
        # NUM_OF_AGENTS +=1
        # self.id = AbstractAgent.n_agents

        
    # def set_id(self):
        
    @abstractmethod
    def agent_letter(self):
        pass
    
    @abstractmethod
    def is_goal_location(self,current): ## current == package coordinate
        pass
    
    @abstractmethod
    def take_action(self):
        pass
    
    
    def get_neighbors(self, position):
        x, y = position
        optinal_neighbors = set(((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)))
        neighbors = []
        for neighbor in optinal_neighbors:
            if self.check_if_valid_location(position, neighbor):
                neighbors.append(neighbor)

        return neighbors


    def check_if_valid_location(self, old_position, new_position):
        if 0 <= new_position[0] <= self.environment.max_x and 0 <= new_position[1] <= self.environment.max_y:

            if not (old_position, new_position) in self.environment.blocked_edges and not (new_position, old_position) in self.environment.blocked_edges:

                if  self.cur_location is old_position:
                    for agent in self.environment.agents:
                        if agent != self and agent.cur_location == new_position:
                            return False
            else:
                return False
            return True
        return False


    def handle_packages_and_deliveries(self):
        if self.environment.check_if_has_package(self.cur_location):
            packages = self.environment.get_packages(self.cur_location)
            for package in packages:
                package.cur_location = self.cur_location
                self.packages.add(package)

        packages_to_remove = list()

        for package in self.packages:
            if package.check_package_dst_location(self.cur_location):
                # need to check deadline
                print(f"package {package.id} had been deliveried at time: {package.deadline}" )
                self.score+=1
                packages_to_remove.append(package)
                

        for package in packages_to_remove:
            self.packages.remove(package)
            self.environment.packages.remove(package)


    def update_package_location(self):
        for package in self.packages:
            package.cur_location = self.cur_location
        
        
##### _______________________________________________________________ #####

##### _________________________ BASIC AGENT _________________________ #####

class Agent(AbstractAgent):
    
    def __init__(self, start_x, start_y,environment):
        super().__init__(start_x, start_y,environment)
        self.broken_bridges = list()

    
    def agent_letter(self):
        return 'A'
    
    
    def dijkstra(self):

        queue = [(0,self.cur_location, [])]
        visited = set()

        while queue:
            cost,current, path = heapq.heappop(queue)

            if current in visited:
                continue

            visited.add(current)
            path = path + [current]


            if self.is_goal_location(current): # one liner check if we are in package src or dst position
                return path

            neighbors = self.get_neighbors(current)
            for neighbor in neighbors:
                if neighbor not in visited: #and neighbor not in self.obstacles:
                    heapq.heappush(queue, (cost + 1,neighbor, path))

        return None  # No path found



##### _______________________________________________________________ #####
        
##### _________________________ HUMAN AGENT _________________________ #####

class HumanAgent(Agent):
    
    def __init__(self, start_x, start_y,environment):
        super().__init__(start_x, start_y,environment)


    def agent_letter(self):
        return 'H'


    def take_action(self):
        print("Enter action:")
        action = input()
        curr_pos = self.cur_location
        if action == 'u':
            if self.check_if_valid_location((self.cur_location[0], self.cur_location[1]), (self.cur_location[0], self.cur_location[1]+1)):
                self.cur_location = (self.cur_location[0], self.cur_location[1]+1)
        elif action == 'l':
            if self.check_if_valid_location((self.cur_location[0], self.cur_location[1]), (self.cur_location[0]-1, self.cur_location[1])):
                self.cur_location = (self.cur_location[0]-1, self.cur_location[1])
        elif action == 'd':
            if self.check_if_valid_location((self.cur_location[0], self.cur_location[1]), (self.cur_location[0], self.cur_location[1]-1)):
                self.cur_location = (self.cur_location[0], self.cur_location[1]-1)
        elif action == 'r':
            if self.check_if_valid_location((self.cur_location[0], self.cur_location[1]), (self.cur_location[0]+1, self.cur_location[1])):
                self.cur_location = (self.cur_location[0]+1, self.cur_location[1])
        elif action == 'n':
            self.cur_location = (self.cur_location[0], self.cur_location[1])
        else:
            raise ValueError(f"Unknown action: {action}")

        self.handle_packages_and_deliveries()
        self.update_package_location()
        self.environment.break_fragile_edge(curr_pos, self.cur_location)
    # check if location has package / delivery and do something about it
    # in the general area 


##### _______________________________________________________________ #####

##### _________________________ GREEDY AGENT _________________________ #####

class GreedyAgent(Agent):
    
    def __init__(self, start_x, start_y,environment):
        super().__init__(start_x, start_y,environment)


    def agent_letter(self):
        return 'G'
    
    
    def take_action(self):
        if len(self.environment.packages) != 0:
            path = self.dijkstra() ## strategy
            if len(path) > 1:
                self.environment.break_fragile_edge(self.cur_location, path[1])
                self.cur_location = path[1]
                self.handle_packages_and_deliveries()
                self.update_package_location()
    
                
    def is_goal_location(self, current): ## current == package coordinate
        if len(self.packages) == 0  and self.environment.check_if_has_package(current):
            return True
        elif len(self.packages) > 0 and self.environment.check_if_has_delivery(current):
            return True
        return False


##### _______________________________________________________________ #####

##### _________________________ SABOTEUR AGENT _________________________ #####

class SaboteurAgent(Agent):
    
    def __init__(self, start_x, start_y,environment):
        super().__init__(start_x, start_y,environment)
        self.other_coordinate = None

    
    def agent_letter(self):
        return 'I'
       
    def is_goal_location(self, current ): ## current == package coordinate
        #if not self.environment.fragile_edges.isEmpty(): ## add this check in the agent movement function
        for edge in self.environment.fragile_edges:
            if current in edge:
                self.other_coordinate = edge[len(edge) - edge.index(current) -1]
                return True
        return False
    
    def take_action(self):
        """
        Plan the path for the agent using Dijkstra's algorithm.
        """
        if len(self.environment.fragile_edges) == 0: ## add this check in the agent movement function
            return
        path = self.dijkstra() ## strategy
        if path:
            if len(path) == 1:
                
                self.environment.break_fragile_edge(self.cur_location, self.other_coordinate)
                self.cur_location = self.other_coordinate
            else:
                self.cur_location = path[1]  # not arrived to edge

    
