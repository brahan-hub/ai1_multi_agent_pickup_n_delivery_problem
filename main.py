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
            " "  # Empty space for intersections
            for x in range(2*max_x + 1)
        ]
        for y in range(2*max_y + 1)
    ]
    return grid

    
def print_board(environment):
    grid = create_grid(environment.max_x,environment.max_y)
    for package in environment.packages:
        if environment.counter >= package.start_time:
            grid[2*package.cur_location[1]][2*package.cur_location[0]] =  "P" + package.id ## place the packages where 0,0 is bottom left
            grid[2*package.dst_location[1]][2*package.dst_location[0]] = "D" + package.id## place the packages where 0,0 is bottom left
            print(f"Package {package.id} cur location: {package.cur_location}, delivery location: {package.dst_location}, package deadline {package.deadline}")
    for agent in environment.agents:
        grid[2*agent.cur_location[1]][2*agent.cur_location[0]] = agent.agent_letter() ## place the packages where 0,0 is bottom left
        print(f"Agent {agent.agent_letter()} cur location: {agent.cur_location}")

    for row in reversed(grid): ## print the grid where 0,0 is bottom left
        print(" ".join(row))
    # for edge in environment.blocked_edges:
        # if edge.point1[0] 
    print("blocked edges: ", environment.blocked_edges)
    print("fragile edges: ", environment.fragile_edges)
    print("time counter: ", environment.counter)
    
    print()

def start_game(env):
    while len(env.packages) > 0:
        print_board(env)
        for agent in env.agents:
            agent.take_action()
            env.counter = env.counter + 1

            # greedy agent keep getting stuck 
       
def main():
    file_path = "input.txt" 
    environment = FileParser.read_input_file(file_path)

    print("Initial Board:")
    start_game(environment)


if __name__ == "__main__":
    main()

## todo: fix the printing - last

## todo: game counter - each move by agent increase by 1
## todo: the score
## todo: game time
## todo: decide what happens if deadline have passed

## todo: check if agents work
## todo: agents time calc