class Edge:
    def __init__(self, src_x,src_y,dst_x,dst_y):
        # self.src_pnt = src_cor
        # self.dst_pnt = dst_cor
        self.edge_coordinates = set((src_x,src_y),(dst_x,dst_y))

        
        