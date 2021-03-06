import random

class RandomProblem:

    def __init__(self, max_cell_num, max_net_num, max_cell_size):

        self.cell_num = random.randrange(10, max_cell_num + 1)
        self.net_num = random.randrange(10, max_net_num + 1)
        print("cell_num = {}".format(self.cell_num))
        print("net_num = {}".format(self.net_num))
        self.net_connect_cell_lists = []
        self.cell_connect_net_lists = [[] for n in range(self.net_num)]

        for i in range(self.cell_num):
            net_set = set([])

            for n in range(random.randrange(1, self.net_num)):
                add_net = random.randrange(1, self.net_num)
                if not add_net in net_set:
                    net_set.add(add_net)
                    self.cell_connect_net_lists[add_net - 1].append(i + 1)
            self.net_connect_cell_lists.append(list(net_set))

        self.cell_size_list = [random.randrange(1, max_cell_size + 1) for i in range(self.cell_num)]

        lock_a_cell_num = random.randrange(self.cell_num // 3)
        lock_b_cell_num = random.randrange(self.cell_num // 3)
        self.lock_a_cell_set = set([])
        self.lock_b_cell_set = set([])
        for i in range(lock_a_cell_num):
            add_cell = random.randrange(1, self.cell_num)
            if not add_cell in self.lock_a_cell_set:
                self.lock_a_cell_set.add(add_cell)
        for i in range(lock_b_cell_num):
            add_cell = random.randrange(1, self.cell_num)
            if not add_cell in self.lock_a_cell_set and not add_cell in self.lock_b_cell_set:
                self.lock_b_cell_set.add(add_cell)

        self.block_size_ratio = 0.5
        self.block_a_min_cell_num_constraint = 0
        self.block_b_min_cell_num_constraint = 0

        # self.block_size_ratio = random.randrange(9) / 10
        # self.block_a_min_cell_num_constraint = random.randrange(self.cell_num // 10)
        # self.block_b_min_cell_num_constraint = random.randrange(self.cell_num // 10)


        print("これからファイル出力するよ")

        network_text = open("random_network.txt", "w", encoding = "utf-8")

        network_text.write("cell_num = {}\n".format(self.cell_num))
        network_text.write("net_num = {}\n".format(self.net_num))
        network_text.write("(cell, net)\n")
        for i in range(self.cell_num):
            for net in self.net_connect_cell_lists[i]:
                network_text.write("({}, {})\n".format(i + 1, net))
        network_text.write("cell_size\n")
        for i in range(self.cell_num):
            network_text.write("{}: {}\n".format(i + 1, self.cell_size_list[i]))
        network_text.write("lock_a_cell\n")
        for cell in self.lock_a_cell_set:
            network_text.write("{}\n".format(cell))

        network_text.write("lock_b_cell\n")
        for cell in self.lock_b_cell_set:
            network_text.write("{}\n".format(cell))

        network_text.write("block_size_ratio = {}\n".format(self.block_size_ratio))
        network_text.write("min_cell_num_a = {}\n".format(self.block_a_min_cell_num_constraint))
        network_text.write("min_cell_num_b = {}\n".format(self.block_b_min_cell_num_constraint))

        network_text.close()
        

        

        
        
