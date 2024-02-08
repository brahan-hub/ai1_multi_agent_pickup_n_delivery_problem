from Package import Package
import sys

class Environment:

    def __init__(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y
        self.blocked_edges = []
        self.fragile_edges = set()
        self.packages = set()
        #self.future_packages = set()
        self.agents = set()
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


    def get_packages(self, location, curr_time = None):
        if curr_time == None:
            curr_time = self.counter
        packages = set()
        for package in self.packages:
            if package.check_package_cur_location(location) and package.start_time <= curr_time:
                packages.add(package)
        return packages

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

    #def update_future_packages(self):
    #    for future_package in self.future_packages:
    #        if future_package.start_time <= self.counter:
    #            self.packages.add(future_package)
    #    self.future_packages.difference_update(self.packages)

    def break_fragile_edge(self, old_position, new_position):
        if (old_position, new_position) in self.fragile_edges:
            self.fragile_edges.remove((old_position, new_position))
            self.blocked_edges.append((old_position, new_position))

        if (new_position, old_position) in self.fragile_edges:
            self.fragile_edges.remove((new_position, old_position))
            self.blocked_edges.append((new_position, old_position))
