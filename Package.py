class Package:
    def __init__(self, id, start_x, start_y, deliver_x, deliver_y, start_time, deadline):
        self.id = id
        self.cur_location = (start_x,start_y)
        self.dst_location = (deliver_x,deliver_y)
        self.start_time = start_time
        self.deadline = deadline
        
    ## add function to check if a given location is holding a package or a delivery location for the package

    def check_package_cur_location(self, location):
        if location == self.cur_location:
            return True
        return False
    
    def check_package_dst_location(self, location):
        if location == self.dst_location:
            return True
        return False



