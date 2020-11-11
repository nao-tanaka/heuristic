class Problem:

    def __init__(self, cell_num, net_num):
        self.cell_num = cell_num
        self.net_num = net_num
        self.net_connect_cell_lists = [[] for n in range(cell_num)]
        self.cell_connect_net_lists = [[] for n in range(net_num)]
        self.cell_size_list = []
        self.lock_a_cell_set = []
        self.lock_b_cell_set = []
        self.block_size_ratio = 0
        self.block_a_min_cell_num_constraint = 0
        self.block_b_min_cell_num_constraint = 0


    def add_connection(self, cell, net):

        self.cell_connect_net_set_list[cell].add(net)
        self.net_connect_cell_set_list[net].add(cell)
