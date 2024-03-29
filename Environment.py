from Package import Package
import Agents
import sys

class Environment:

    def __init__(self, max_x, max_y):
        self.max_x, self.max_y= max_x,max_y
        self.fragile_edges,self.packages,self.agents = set(),set(),set()
        self.blocked_edges = []
        self.counter = 0
        self.closest_deadline = sys.maxsize
        self.bonus = False


    def update_max_game_time(self):
        temp_time = sys.maxsize
        for package in self.packages:
            if temp_time > package.deadline:
                temp_time = package.deadline
        if temp_time != sys.maxsize:
            self.closest_deadline = temp_time


    def is_game_over(self):
        return len(self.packages) == 0 or self.counter >= self.closest_deadline

    def bonus_saboteur_location(self):
        if self.bonus:
            for agent in self.agents:
                if isinstance(agent, Agents.SaboteurAgent):
                    return agent.cur_location
        return None

    def get_packages(self, location, curr_time = None):
        if curr_time == None:
            curr_time = self.counter
        packages = set()
        for package in self.packages:
            if package.check_package_cur_location(location) and package.start_time <= curr_time:
                packages.add(package)
        return packages

    def remove_package(self, package):
        self.packages.remove(package)
        # for agent in self.agents
        
    def check_if_has_package(self, position):
        for package in self.packages:
            if package.check_package_cur_location(position) and package.start_time <= self.counter:
                return True
        return False

    def check_if_has_delivery(self, position):
        for package in self.packages:
            if package.check_package_dst_location(position):
                return True
        return False

    def check_if_fragile_edge(self, old_position, new_position):
        # check if fragile edge was broken
        if not (old_position, new_position) in self.fragile_edges and not (new_position, old_position) in self.fragile_edges:
            return False
        return True

    def check_if_vertex_of_fragile(self, position):
        # check if fragile edge was broken
        for fragile_edge in self.fragile_edges:
            if position in fragile_edge:
                return True
        return False


    def break_fragile_edge(self, old_position, new_position):
        if (old_position, new_position) in self.fragile_edges:
            self.fragile_edges.remove((old_position, new_position))
            self.blocked_edges.append((old_position, new_position))

        if (new_position, old_position) in self.fragile_edges:
            self.fragile_edges.remove((new_position, old_position))
            self.blocked_edges.append((new_position, old_position))
    
    def is_valid_move(self,new_location):
        return all(agent.cur_location == new_location for agent in self.agents)


        # self.max_x, self.max_y= max_x,max_y
        # self.fragile_edges,self.packages,self.agents = set(),set(),set()
        # self.blocked_edges = []
        # self.counter = 0
        # self.closest_deadline = sys.maxsize
        # self.bonus = False