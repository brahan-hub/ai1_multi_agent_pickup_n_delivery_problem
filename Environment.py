from Package import Package

class Environment:

    def __init__(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y
        self.blocked_edges = []
        self.fragile_edges = []
        self.packages = []
        self.agents = set()
        self.counter = 0


    def get_package(self, location):
        for package in self.packages:
            if package.check_package_cur_location(location):
                return package
        return None

    def check_if_has_package(self, position):
        for package in self.packages:
            if package.check_package_cur_location(position):
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
