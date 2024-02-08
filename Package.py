class Package:
    def __init__(self, id, start_x, start_y, deliver_x, deliver_y, start_time, deadline):
        self.id = id
        self.cur_location = (start_x,start_y)
        self.dst_location = (deliver_x,deliver_y)
        self.start_time = start_time
        self.deadline = deadline
        
    def check_package_cur_location(self, location):
        return location == self.cur_location

    
    def check_package_dst_location(self, location):
        return location == self.dst_location

    def update_package_location(self,new_location):
        self.cur_location = new_location



