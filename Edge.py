class Edge:
    def __init__(self, src_x,src_y,dst_x,dst_y):
        # self.src_pnt = src_cor
        # self.dst_pnt = dst_cor
        self.edge_coordinates = set((src_x,src_y),(dst_x,dst_y))
        self.direction = self.check_direction()
        
    # def check_direction(self):
    #     src_pos = self.edge_coordinates[0]
    #     if self.edge


def check_direction(src_x,src_y,dst_x,dst_y):
    if src_x - dst_x
        