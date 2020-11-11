#! /usr/bin/python3


# セルを表すクラス
# 接続しているネットの集合net_set
# セルのゲインgain
# セルのサイズsize
# セルがどちらのブロックにあるのかを表すwhich_block
class Cell:
    def __init__(self, identifier, size, net_list, which_block):
        self.__identifier = identifier
        self.__net_list = list(net_list)
        self.__size = size
        self.__which_block = which_block
        self.__gain = 0

    @property
    def identifier(self):
        return self.__identifier
    
    @property
    def net_list(self):
        return self.__net_list

    @property
    def gain(self):
        return self.__gain
    @property
    def size(self):
        return self.__size

    @property
    def which_block(self):
        return self.__which_block

    # self.__gainを+valする
    def add_gain(self, val):
        self.__gain += val

    # self.__gainを変更する
    def set_gain(self, val):
        self.__gain = val


    # self.__which_blockを変更する
    def switch_block(self, which_block):
        self.__which_block = which_block

