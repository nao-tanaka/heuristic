#! usr/bin/python3

# ブロックを表すセル
# 二つ作られる
# ブロックに属するセルの集合cell_set
# ブロックに属するセルのサイズの和size
# 最も望ましいブロックのサイズbest_size
# ブロックの最小サイズの制約min_constraint
# ブロックの最大サイズの制約max_constraint
# ブロックに属する最小セル数の制約min_cell_num_constraint
class Block:

    def __init__(self, total_cell_size, max_free_cell_size, block_size_ratio, min_cell_num_constraint, which_block):
        self.cell_set = set([])
        self.size = 0
        self.__best_size = total_cell_size * block_size_ratio
        self.__min_size_constraint = self.best_size - max_free_cell_size
        self.__max_size_constraint = self.best_size + max_free_cell_size
        self.__min_cell_num_constraint = min_cell_num_constraint
        self.__which_block = which_block


    # ブロックにセルを追加する関数
    def add_cell(self, cell):
        self.cell_set.add(cell)
        self.size += cell.size

    # ブロックからセルを消去する関数
    def remove_cell(self, cell):
        self.cell_set.remove(cell)
        self.size -= cell.size

    @property
    def cell_num(self):
        return len(self.cell_set)

    @property
    def which_block(self):
        return self.__which_block

    @property
    def best_size(self):
        return self.__best_size

    @property
    def min_size_constraint(self):
        return self.__min_size_constraint

    @property
    def max_size_constraint(self):
        return self.__max_size_constraint

    @property
    def min_cell_num_constraint(self):
        return self.__min_cell_num_constraint

    @property
    def which_block(self):
        return self.__which_block

