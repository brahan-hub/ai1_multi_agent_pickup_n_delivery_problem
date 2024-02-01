from abc import abstractmethod
from collections import deque
import copy
import sys
import heapq
import State
import Agents
from Node import Node

T_TIME_EVALUATION = 0.0001
        
class SearchAgent(Agents.AbstractAgent):
    def __init__(self, start_x, start_y, environment) -> None:
        super().__init__(start_x, start_y,environment)
        # start

    def heuristic_function(self, u_node):
        cur_rel_vertices = self.get_rel_vertices(u_node)
        important_vertices_distance_matrix = dict()
        important_vertices_distance_matrix = dict.fromkeys(list(cur_rel_vertices))
        for vertex in cur_rel_vertices:
            important_vertices_distance_matrix[vertex] = {}.fromkeys(list(cur_rel_vertices),0)
            self.min_distances(important_vertices_distance_matrix[vertex],vertex)
        ## build mst:
        return self.minimum_spanning_tree(important_vertices_distance_matrix,u_node.state_location)


    def get_rel_vertices(self, u_node):
        rel_ver = set()
        for package in u_node.packages:
            rel_ver.add(package.cur_location)
            rel_ver.add(package.dst_location)
        for packge in u_node.agent_packages:
            rel_ver.add(packge.dst_location)
        rel_ver.add(u_node.state_location)

        return rel_ver


    def min_distances(self, distance_dict,start_location):
        
        visited = set()
        queue = deque([(start_location, 0)])
        
        while queue:
            current_node, distance = queue.popleft()
            if current_node in distance_dict.keys():
                distance_dict[current_node] = distance
            visited.add(current_node)
            for neighbor in self.get_neighbors(current_node):
                if neighbor not in visited:
                    queue.append((neighbor, distance + 1))
        
        # return distances

    def minimum_spanning_tree(self, min_dist_graph, start_vertex):
        mst = dict()
        visited = set()
        min_edge_heap = [(0, start_vertex, start_vertex)]
        total_mst_distance = 0
        while min_edge_heap:
            cost, current_vertex, prev_vertex = heapq.heappop(min_edge_heap)
            if current_vertex not in visited:
                visited.add(current_vertex)
                total_mst_distance += cost
                mst[current_vertex] = prev_vertex 

                for neighbor, edge_cost in min_dist_graph[current_vertex].items():
                    if neighbor not in visited:
                        heapq.heappush(min_edge_heap, (edge_cost, neighbor, current_vertex))

        return total_mst_distance
    
    @abstractmethod
    def expand(self,u_state):
        pass
    
    def is_goal_location(self, node):
        if len(node.agent_packages) == 0 and len(node.packages) == 0:
            return True
        return False
            
    def search_optimal_path(self,limit=10000): # A* limit should be global constant
        open_set = []
        closed_set = {}
        counter = 0

        start_node = Node(self.cur_location, self.environment, self.packages)
        heapq.heappush(open_set, (start_node.f(), id(start_node), start_node))

        while open_set:
            _, _,current_node = heapq.heappop(open_set)

            if self.is_goal_location(current_node) or counter == limit:
                path = []
                while current_node:
                    path.append(current_node.state_location)
                    current_node = current_node.parent
                return limit, path[::-1]

            if current_node.state_location in closed_set and closed_set[current_node.state_location] >= g:
                    continue
                
            closed_set[current_node.state_location] = current_node.g

            for neighbor_location in self.get_neighbors(current_node.state_location):
                g = current_node.g + 1
                
                neighbor_node = Node(neighbor_location, self.environment,self.packages, current_node,g,0)
                
                neighbor_node.h = self.heuristic_function(neighbor_node)
                
                heapq.heappush(open_set, (neighbor_node.f(), id(neighbor_node), neighbor_node))

            counter += 1

        return limit, None    

class GreedySearchAgent(SearchAgent): # one expand with different goal state
    def __init__(self, start_x, start_y, environment) -> None:
        super().__init__(start_x, start_y, environment)

    def take_action(self):
        if len(self.environment.packages) != 0:
            limit, path = self.search_optimal_path(1)
            if path is not None:
                self.environment.break_fragile_edge(self.cur_location, path[1])
                self.cur_location = path[1]
                self.handle_packages_and_deliveries()
                self.update_package_location()
        return None
  
  
    #def GreedySearch(self,limit=10000): # A* limit should be global constant
    #    open_set = []
    #    open_nodes = set()
    #    closed_set = {}

    #    start_node = Node(self.cur_location, self.environment, self.packages)
    #    heapq.heappush(open_set, (start_node.f(), id(start_node), start_node))
    #    open_nodes.add(self.cur_location)


    #    while open_set:
    #        _, _,current_node = heapq.heappop(open_set)
    #        open_nodes.remove(current_node.state_location)

    #        if self.is_goal_location(current_node) or limit<1:
    #            path = []
    #            while current_node:
    #                path.append(current_node.state_location)
    #                current_node = current_node.parent
    #            return path[::-1]
            
    #        if current_node.state_location in closed_set:
    #                continue
                
    #        closed_set[current_node.state_location] = current_node.h

    #        for neighbor_location in self.get_neighbors(current_node.state_location):

    #            if neighbor_location in open_nodes:
    #                continue
    #            g = current_node.g + 1
                
    #            neighbor_node = Node(neighbor_location, self.environment, self.packages, current_node,g,0)
                
    #            neighbor_node.h = self.heuristic_function(neighbor_node)
                
    #            heapq.heappush(open_set, (neighbor_node.h, id(neighbor_node), neighbor_node))
    #            open_nodes.add(neighbor_location)
    #    return None

    def agent_letter(self):
        return 'S'

class AStarSearchAgent(SearchAgent):
    def __init__(self, start_x, start_y, environment) -> None:
        super().__init__(start_x, start_y, environment)
           
    def take_action(self):
        if len(self.environment.packages) != 0:
            limit, path = self.search_optimal_path()
            print("A* search agent took: ", limit, " Expensiosn to reach goal, it took him: ", limit * T_TIME_EVALUATION, "To find path")
            if path is not None:
                self.environment.break_fragile_edge(self.cur_location, path[1])
                self.cur_location = path[1]
                self.handle_packages_and_deliveries()
                self.update_package_location()
                
    #def AStarSearch(self,limit=10000): # A* limit should be global constant
    #    open_set = []
    #    closed_set = {}
    #    counter = 0

    #    start_node = Node(self.cur_location, self.environment, self.packages)
    #    heapq.heappush(open_set, (start_node.f(), id(start_node), start_node))

    #    while open_set:
    #        _, _,current_node = heapq.heappop(open_set)

    #        if self.is_goal_location(current_node) or counter == limit:
    #            path = []
    #            while current_node:
    #                path.append(current_node.state_location)
    #                current_node = current_node.parent
    #            return limit, path[::-1]

    #        if current_node.state_location in closed_set and closed_set[current_node.state_location] >= g:
    #                continue
                
    #        closed_set[current_node.state_location] = current_node.g

    #        for neighbor_location in self.get_neighbors(current_node.state_location):
    #            g = current_node.g + 1
                
    #            neighbor_node = Node(neighbor_location, self.environment,self.packages, current_node,g,0)
                
    #            neighbor_node.h = self.heuristic_function(neighbor_node)
                
    #            heapq.heappush(open_set, (neighbor_node.f(), id(neighbor_node), neighbor_node))

    #        counter += 1

    #    return None

    def agent_letter(self):
        return 'A'

        
class RealTimeAStarSearchAgent(AStarSearchAgent):
    def __init__(self, start_x, start_y, environment) -> None:
        super().__init__(start_x, start_y, environment)
        self.L = 10


    def take_action(self):
        if len(self.environment.packages) != 0:
            limit, path = self.search_optimal_path(self.L)
            print("Real time A* search agent took: ", limit * T_TIME_EVALUATION, "To find path")
            self.environment.counter += limit * T_TIME_EVALUATION
            if path is not None:
                self.environment.break_fragile_edge(self.cur_location, path[1])
                self.cur_location = path[1]
                self.handle_packages_and_deliveries()
                self.update_package_location()

    def agent_letter(self):
        return 'R'


### greedy search agent not working 
### need to add evaluation 
### need to check that packages are showing 



