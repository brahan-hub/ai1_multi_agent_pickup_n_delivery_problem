import Environment
import Agents
import SearchAgents
import Package
import FileParser

def create_grid(max_x, max_y):
    grid = [
        [
            "." if x % 2 == 0 and y % 2 == 0 else
            "-" if x % 2 == 1 and y % 2 == 0 else
            "|" if x % 2 == 0 and y % 2 == 1 else
            " " 
            for x in range(2*max_x + 1)
        ]
        for y in range(2*max_y + 1)
    ]
    return grid

def populate_grid(grid, location, item):
    grid[2*location[1]][2*location[0]] = item
    
def populate_grid_edges(grid,cor1,cor2,item):
    grid[cor1[1]+cor2[1]][cor1[0]+cor2[0]] = item
    
def print_board(environment):
    grid = create_grid(environment.max_x,environment.max_y)
    for package in environment.packages:
        if environment.counter >= package.start_time:
            populate_grid(grid,package.cur_location,"P"+package.id)
            populate_grid(grid,package.dst_location,"D"+package.id)
            print(f"Package {package.id} cur location: {package.cur_location}, delivery location: {package.dst_location}, package deadline {package.deadline}")
    for agent in environment.agents:
        populate_grid(grid,agent.cur_location,agent.agent_letter())
        print(f"Agent {agent.agent_letter()} cur location: {agent.cur_location}")
    for blocked_edge in environment.blocked_edges:
        populate_grid_edges(grid,blocked_edge[0],blocked_edge[1],"#")
    for fragile_edge in environment.fragile_edges:
        populate_grid_edges(grid,fragile_edge[0],fragile_edge[1],"/")

        
    for row in reversed(grid):
        print(" ".join(row))
    print("blocked edges: ", environment.blocked_edges)
    print("fragile edges: ", environment.fragile_edges)
    print("time counter: ", environment.counter)
    

def start_game(env):

    for agent in env.agents:
        agent.handle_packages_and_deliveries()

    print_board(env)
    while not env.is_game_over():
        for agent in env.agents:
            agent.handle_packages_and_deliveries()
            print(agent.agent_letter() + " Turn")
            agent.take_action()
            env.counter = env.counter + 1
            env.update_max_game_time()
            print_board(env)
            print("env counter: "+ str(env.counter))
            print(agent.agent_letter()+  " Current Score: " + str(agent.score))
            
    print("Final ScoreBoard:")
    for agent in env.agents:
        agent.handle_packages_and_deliveries()
        print(agent.agent_letter()+  " Score: " + str(agent.score))
       
def main():
    file_path = "input.txt" 
    environment = FileParser.read_input_file(file_path)

    print("Initial Board:")
    environment.update_max_game_time()
    
    start_game(environment)
    


if __name__ == "__main__":
    main()

