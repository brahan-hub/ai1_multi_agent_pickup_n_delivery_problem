from Environment import Environment
import Agents
import SearchAgents
from Package import Package



def read_input_file(file_path):
    environment = None
    packages = []
    agents = []

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith("#X"):
                _, max_x = line.split()
                max_x = int(max_x)
            elif line.startswith("#Y"):
                _, max_y = line.split()
                max_y = int(max_y)
                environment = Environment(max_x, max_y)
            elif line.startswith("#P"):
                print(line)
                _S, start_x, start_y,start_time, _D, deliver_x, deliver_y, deadline = line.split()
                print(start_x, start_y,start_time, deliver_x, deliver_y, deadline)
                package_id = str(len(environment.packages))
                package = Package(package_id,int(start_x), int(start_y), int(deliver_x), int(deliver_y), int(start_time), int(deadline))
                environment.future_packages.add(package)
            elif line.startswith("#B"):
                _, x1, y1, x2, y2 = line.split()
                blocked_edge = ((int(x1), int(y1)), (int(x2), int(y2)))
                environment.blocked_edges.append(blocked_edge)
            elif line.startswith("#F"):
                _, x1, y1, x2, y2 = line.split()
                fragile_edge = ((int(x1), int(y1)), (int(x2), int(y2)))
                environment.fragile_edges.append(fragile_edge)
            #elif line.startswith("#G"):
            #     _, start_x, start_y = line.split()
            #     agent = Agents.GreedyAgent(int(start_x), int(start_y),environment)
            #     environment.agents.add(agent)
            ##elif line.startswith("#H"):
            ##     _, start_x, start_y = line.split()
            ##     human_agent = Agents.Human_Agent(int(start_x), int(start_y), environment)
            ##     environment.agents.add(human_agent)
            #elif line.startswith("#I"):
            #     _, start_x, start_y = line.split()
            #     interfering_agent = Agents.Saboteur_Agent(int(start_x), int(start_y), environment)
            #     environment.agents.add(interfering_agent)
            elif line.startswith("#A"):
                 _, start_x, start_y = line.split()
                 search_agent = SearchAgents.AStarSearchAgent(int(start_x), int(start_y), environment)
                 environment.agents.add(search_agent)
            elif line.startswith("#S"):
                 _, start_x, start_y = line.split()
                 search_agent = SearchAgents.GreedySearchAgent(int(start_x), int(start_y), environment)
                 environment.agents.add(search_agent)
            elif line.startswith("#R"):
                 _, start_x, start_y = line.split()
                 search_agent = SearchAgents.RealTimeAStarSearchAgent(int(start_x), int(start_y), environment)
                 environment.agents.add(search_agent)


    return environment
