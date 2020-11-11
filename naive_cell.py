#! usr/bin/python3


# セルを表すクラス
# セル番号self.identifier
# セルが接続しているネットのリストself.net_list
# セルのサイズself.size
# セルがどのブロックにあるのかを示すself.which_block
# を持つ
class Cell:
    def __init__(self, identifier, size, net_list, which_block):
        self.__identifier = identifier
        self.__net_list = list(net_list)
        self.__size = size
        self.__which_block = which_block

    @property
    def identifier(self):
        return self.__identifier
        
    @property
    def net_list(self):
        return self.__net_list

    @property
    def size(self):
        return self.__size

    @property
    def which_block(self):
        return self.__which_block

    def switch_block(self, which_block):
        self.__which_block = which_block

        

