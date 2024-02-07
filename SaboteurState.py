import Agents
class SaboteurState():
    def __init__(self, agent_loaction, env, prev_state = None):
        self.greedy_agent = Agents.SaboteurAgent((agent_loaction), env)
        self.broken_edges = set()

        
    def check_if_broken_edge(self, prev_state):
        for edge in self.environment.fragile_edges:
            if self.cur_location in edge:
                if prev_state.greedy_agent.cur_location == edge[len(edge) - edge.index(current) -1]:
                    self.broken_edge.append(edge)




