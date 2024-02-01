from abc import abstractmethod
from collections import deque
import copy
import sys
import heapq
import State
import Agents
import Node

        
class SearchAgent(Agents.AbstractAgent):
    def __init__(self, start_x, start_y, environment) -> None:
        super().__init__(start_x, start_y,environment)
        # start

    def hioristic_function(self, u_node):
        cur_rel_vertices = u_node.packages | u_node.deliveries
        cur_rel_vertices.add(u_node.state_location)
        important_vertices_distance_matrix = dict()
        important_vertices_distance_matrix = dict.fromkeys(list(cur_rel_vertices),{}.fromkeys(list(cur_rel_vertices),0))
        for vertex in cur_rel_vertices:
            self.min_distances(important_vertices_distance_matrix[vertex],vertex)
        ## build mst:
        return self.minimum_spanning_tree(important_vertices_distance_matrix,u_node.state_location)


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
        if len(node.agent_packages) == 0 and len(node.packages) == 0 and len(node.deliveries)==0:
            return True
        return False
            
        

class GreedySearchAgent(SearchAgent): # one expand with different goal state
    def __init__(self, start_x, start_y, environment) -> None:
        super().__init__(start_x, start_y, environment)
        
    def expand(self):
        min_huristic = sys.maxsize
        next_vertex_to_go = self.cur_location

        curr_state = Node.Node(self.cur_location, self.environment.packages, self.packages,0,0)
        for neighbor in self.get_neighbors(self.cur_location):
            # self.state
            curr_h = self.hioristic_function(Node(neighbor, self.environment.packages, self.packages, curr_state, 1))
            if (curr_h < min_huristic):
                min_huristic = curr_h
                next_vertex_to_go = neighbor 
        return next_vertex_to_go

    def expand2(self): # GREEDY
        open_set = []
        closed_set = set()  # set of nodes already eval

        start_node = Node(self.cur_location, self.environment.packages, self.packages)
        heapq.heappush(open_set, (start_node.f(), id(start_node), start_node))

        while open_set:
            _, _,current_node = heapq.heappop(open_set)  #
            open_set.clear()
            
            if self.is_goal_location(current_node):
                path = []
                while current_node:
                    path.append(current_node.state)
                    current_node = current_node.parent
                return path[::-1] # returing reversed path
                
            closed_set.add((current_node.state))
            
            for neighbor_location in self.get_neighbors(current_node.state_location):

                if neighbor_location in closed_set:
                    continue
  
                neighbor_node = Node(neighbor_location, self.environment.packages,self.packages, current_node,0,0)
                neighbor_node.h = self.heuristic(neighbor_node)
                
                heapq.heappush(open_set, (neighbor_node.h, id(neighbor_node), neighbor_node))

        return None
  
  


    def take_action(self):
        """
        Plan the path for the agent using Dijkstra's algorithm.
        """
        if len(self.environment.packages) != 0:
            next_Vertex = self.expand() ## strategy
            if next_Vertex != self.cur_location:
                self.environment.break_fragile_edge(self.cur_location, next_Vertex)
                self.cur_location = next_Vertex
                self.handle_packages_and_deliveries()
                self.update_package_location()

    def agent_letter(self):
        return 'S'

class AStarSearchAgent(SearchAgent):
    def __init__(self, start_x, start_y, environment) -> None:
        super().__init__(start_x, start_y, environment)
           
        
    def expand2(self,limit=10000): # A* limit should be global constant
        open_set = []
        closed_set = {}

        start_node = Node(self.cur_location, self.environment.packages, self.packages)
        heapq.heappush(open_set, (start_node.f(), id(start_node), start_node))

        while open_set:
            _, _,current_node = heapq.heappop(open_set)

            if self.is_goal_location(current_node) or limit<1:
                path = []
                while current_node:
                    path.append(current_node.state)
                    current_node = current_node.parent
                return path[::-1]
            
            if current_node.state_location in closed_set and closed_set[current_node.state_location] >= g:
                    continue
                
            closed_set[current_node.state_location] = current_node.g

            for neighbor_location in self.get_neighbors(current_node.state_location):
                g = current_node.g + 1
                
                neighbor_node = Node(neighbor_location, self.environment.packages,self.packages, current_node,g,0)
                
                neighbor_node.h = self.heuristic(neighbor_node)
                
                heapq.heappush(open_set, (neighbor_node.f(), id(neighbor_node), neighbor_node))
            limit -=1

        return None



        
class RealTimeAStarSearchAgent(AStarSearchAgent):
    def __init__(self, start_x, start_y, environment) -> None:
        super().__init__(start_x, start_y, environment)
        
    def expand2(self,limit=10): # realA* limit is user determined constant
            open_set = []
            closed_set = {}

            start_node = Node(self.cur_location, self.environment.packages, self.packages)
            heapq.heappush(open_set, (start_node.f(), id(start_node), start_node))

            while open_set:
                _, _,current_node = heapq.heappop(open_set)

                if self.is_goal_location(current_node) or limit<1:
                    path = []
                    while current_node:
                        path.append(current_node.state)
                        current_node = current_node.parent
                    return path[::-1]
                    
                if current_node.state_location in closed_set and closed_set[current_node.state_location] >= g:
                        continue
                    
                closed_set[current_node.state_location] = current_node.g

                for neighbor_location in self.get_neighbors(current_node.state_location):
                    g = current_node.g + 1
                    
                    neighbor_node = Node(neighbor_location, self.environment.packages,self.packages, current_node,g,0)
                    
                    neighbor_node.h = self.heuristic(neighbor_node)
                    
                    heapq.heappush(open_set, (neighbor_node.f(), id(neighbor_node), neighbor_node))
                    
                limit-=1

            return None
### find the minimal distance between every 2 vertices in the grid but save only the distance between the important vertices
### build an mst from the relevant vertices - 
### repeat for each expand? check
### the total weight of the mst is the huristic -> h --> here the greedy end
### the time is g
### sort by f=g+h, expand the state with the minimal f value --> for the A*


## need to re define:
## who hold state
## who hold environment 
## does the agent hold state or the state hold current agent?
## 



