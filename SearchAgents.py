from abc import abstractmethod
from collections import deque
import copy
import sys
import heapq
import State
import Agents
from Node import Node, Package_state

T_TIME_EVALUATION = 0.0001


##### _________________________ ABSTRACT SEARCH AGENT _________________________ #####

class SearchAgent(Agents.AbstractAgent):
    def __init__(self, start_x, start_y, environment) -> None:
        super().__init__(start_x, start_y,environment)

    @abstractmethod
    def expand(self,u_state):
        pass
    
    def heuristic_function(self, u_node):
        cur_rel_vertices = u_node.get_rel_vertices()
        important_vertices_distance_matrix = dict()
        important_vertices_distance_matrix = dict.fromkeys(list(cur_rel_vertices))
        for vertex in cur_rel_vertices:
            important_vertices_distance_matrix[vertex] = {}.fromkeys(list(cur_rel_vertices),0)
            self.min_distances(important_vertices_distance_matrix[vertex],vertex)
        ## build mst:
        return self.minimum_spanning_tree(important_vertices_distance_matrix,u_node.state_location)



    def min_distances(self, distance_dict,start_location):
        counter = len(distance_dict)
        visited = set()
        queue = deque([(start_location, 0)])
        
        while queue and counter > 0:
            current_node, distance = queue.popleft()
            
            if current_node in visited:
                continue

            if current_node in distance_dict.keys():
                distance_dict[current_node] = distance
                counter -= 1
                
            visited.add(current_node)
            
            for neighbor in self.get_neighbors(current_node):
                if neighbor not in visited:
                    queue.append((neighbor, distance + 1))


    def minimum_spanning_tree(self, min_dist_graph, start_vertex):
        mst = dict()
        visited = set()
        total_mst_distance = 0
        min_edge_heap = [(0, start_vertex, start_vertex)]
        
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
    
    
    #def is_goal_location(self, node):
    #    if len(node.agent_packages) == 0 and len(node.packages) == 0:
    #    return 
    #        return True
    #    return False

    def get_neighbors_with_bonus(self, current_node):
        neighbors = self.get_neighbors(current_node.state_location)

        removed_neighbors = set()
        for neighbor in neighbors:
            for edge in current_node.fragile_broken_edges:
                if current_node.state_location in edge and neighbor in edge:
                        removed_neighbors.add(neighbor)
        neighbors.difference_update(removed_neighbors)
        return neighbors


    # add set of fragile, that the sabuter can break on it's way
            
    def search_optimal_path(self, limit=10000): # A* limit should be global constant
        open_set = []
        closed_set = {}
        counter = 0
        #check if needs to 
        start_node = Node(self.cur_location, self.environment,self.packages, None ,0,0)
        heapq.heappush(open_set, (start_node.f(), id(start_node), start_node))

        while open_set and counter < limit:
            _, _,current_node = heapq.heappop(open_set)

            if current_node.is_goal_state():
                path = []
                while current_node:
                    path.append(current_node.state_location)
                    current_node = current_node.parent
                return counter, path[::-1]
            if current_node.state_location in closed_set:
                if current_node.compare_node(closed_set[current_node.state_location]) and closed_set[current_node.state_location].f() <= current_node.f():
                    continue
               
            closed_set[current_node.state_location] = current_node



            for neighbor_location in self.get_neighbors_with_bonus(current_node):
                g = current_node.g + 1

                neighbor_node = Node(neighbor_location, self.environment,self.packages, current_node,g,0)

                neighbor_node.h = self.heuristic_function(neighbor_node)
                
                heapq.heappush(open_set, (neighbor_node.f(), id(neighbor_node), neighbor_node))

            counter += 1

        return counter, None    

##### ____________________________________________________________________ #####

##### _________________________ASTAR SEARCH AGENT_________________________ #####

class GreedySearchAgent(SearchAgent):
     # one expand with different goal state
     
    def __init__(self, start_x, start_y, environment) -> None:
        super().__init__(start_x, start_y, environment)
    
    def agent_letter(self):
        return 'S'
    
    def take_action(self):
        if len(self.environment.packages) != 0:
            limit, path = self.search_optimal_path(1)
            
            if path is not None:
                self.environment.break_fragile_edge(self.cur_location, path[1])
                self.cur_location = path[1]
                self.handle_packages_and_deliveries()
                
        return None


##### ____________________________________________________________________ #####

##### _________________________ASTAR SEARCH AGENT_________________________ #####

class AStarSearchAgent(SearchAgent):
    
    def __init__(self, start_x, start_y, environment) -> None:
        super().__init__(start_x, start_y, environment)
    
    def agent_letter(self):
        return 'A'
           
    def take_action(self):
        if len(self.environment.packages) != 0:
            limit, path = self.search_optimal_path()
            print("A* search agent took: ", limit, " Expensiosn to reach goal, it took him: ", limit * T_TIME_EVALUATION, "To find path")
            if path is not None:
                self.environment.break_fragile_edge(self.cur_location, path[1])
                self.cur_location = path[1]
                self.handle_packages_and_deliveries()
                #self.update_package_location()                


##### ____________________________________________________________________ #####

##### _________________________ REAL TIME A STAR _________________________ #####

class RealTimeAStarSearchAgent(AStarSearchAgent):
    def __init__(self, start_x, start_y, environment) -> None:
        super().__init__(start_x, start_y, environment)
        self.L = 10

    def agent_letter(self):
        return 'R'

    def take_action(self):
        if len(self.environment.packages) != 0:
            limit, path = self.search_optimal_path(self.L)
            print("Real time A* search agent took: ", limit * T_TIME_EVALUATION, "To find path")
            self.environment.counter += limit * T_TIME_EVALUATION
            
            if path is not None:
                self.environment.break_fragile_edge(self.cur_location, path[1])
                self.cur_location = path[1]
                self.handle_packages_and_deliveries()
                #self.update_package_location()



