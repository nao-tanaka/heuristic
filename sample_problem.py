#! /usr/bin/python3

class SampleProblem:

    def __init__(self):
        self.cell_num = 10
        self.net_num = 20
        self.net_connect_cell_lists = [[1, 2, 3, 4], [1, 5, 6, 7], [2, 5, 8, 9], [3, 6, 8, 10], [4, 7, 9, 10], [11, 12, 13, 14], [11, 15, 16, 17], [12, 15, 18, 19], [13, 16, 18, 20], [14, 17, 19, 20]]
        self.cell_connect_net_lists = [[1, 2], [1, 3], [1, 4], [1, 5], [2, 3], [2, 4], [2, 5], [3, 4] ,[3, 5] ,[4, 5] ,[6, 7] ,[6, 8] ,[6, 9] ,[6, 10] ,[7, 8] ,[7, 9] ,[7, 10] ,[8, 9] ,[8, 10] ,[9, 10]]
        self.cell_size_list = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.lock_a_cell_set = []
        self.lock_b_cell_set = []
        self.block_size_ratio = 0.5
        self.block_a_min_cell_num_constraint = 3
        self.block_b_min_cell_num_constraint = 3
