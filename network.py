#! /usr/bin/python3


# ネットワークを表すクラス
# cell_listは、i番目の要素が、セルiを持つ
# net_connect_cell_listsは、i番目の要素が、ネットiに接続しているセルのリストを持つ
class Network:

    def __init__(self, cell_list, cell_connect_net_lists):
        self.__cell_list = list(cell_list)
        self.__cell_connect_net_lists  = list(cell_connect_net_lists)


    @property
    def cell_num(self):
        return len(self.__cell_list)

    @property
    def net_num(self):
        return len(self.__cell_connect_net_lists)

    @property
    def cell_list(self):
        for cell in self.__cell_list:
            yield cell

    def cell(self, cell_index):
        return self.__cell_list[cell_index]

    def cell_connect_net_list(self, net_index):
        for cell in self.__cell_connect_net_lists[net_index]:
            yield cell

