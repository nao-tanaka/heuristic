from enum import Enum

# セルがどちらのブロックにあるのかを表す
# transitionsの方が良いか
class WhichBlock(Enum):
    A = 1
    B = 2


# セルを表すクラス
# 接続しているネットの集合net_set
# セルのゲインgain
# セルのサイズsize
# セルがどちらのブロックにあるのかを表すwhich_block
class Cell:
    def __init__(self, size, net_list, which_block):
        self.__net_list = list(net_list)
        self.__size = size
        self.__which_block = which_block
        self.__gain = 0


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


# ネットワークを表すクラス
# cell_listは、i番目の要素が、セルiを持つ
# net_connect_cell_listsは、i番目の要素が、ネットiに接続しているセルのリストを持つ
class Network:

    def __init__(self, cell_list, cell_connect_net_lists):
        self.__cell_list = list(cell_list)
        self.__cell_connect_net_lists  = list(cell_connect_net_lists)


    @property
    def cell_num(self):
        return len(cell_list)

    @property
    def net_num(self):
        return len(net_list)

    @property
    def cell_list(self):
        for cell in self.__cell_list:
            yield cell

    def cell(self, cell_index):
        return self.__cell_list[index]

    def cell_connect_net_list(self, net_index):
        for cell in self.__net_connect_cell_lists[index]:
            yield cell




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
        self.best_size = total_cell_size * block_size_ratio
        self.min_size_constraint = self.best_size - max_free_cell_size
        self.max_size_constraint = self.best_size + max_free_cell_size
        self.min_cell_num_constraint = cell_num_constraint
        self.__which_block = which_block

    @property
    def which_block(self):
        return self.__which_block

    # ブロックにセルを追加する関数
    def add_cell(self, cell):
        self.block.add(cell)
        self.size += cell.size

    # ブロックからセルを消去する関数
    def remove_cell(self, cell):
        self.block.remove(cell)
        self.size -= cell.size

    @property
    def cell_num(self):
        return len(self.cell_set)


# ブロックについての情報のクラス
# ブロック内のセルのゲインのバケツリスト(self.bucket_list)
# ブロック内の最も大きなゲインを持ったセルのゲインの値(self.maxgain)を持つ
class BucketSort:

    def __init__(self, pmax):
        self.bucket_list = [set([]) for n in range(2 * pmax + 1)]
        self.maxgain = -pmax - 1
        self.__pmax = pmax

    @property
    def pmax(self):
        return self.__pmax

    # 渡されたセルを、そのセルのゲインに対応したself.bucketの要素内のリストに加える
    # ゲインgに対応したself.bucketの要素は,pmax + 1 + g番目
    # セルのゲインがself.maxgainよりも大きければ、self.maxgainを更新
    def add_cell(self, cell):
        self.__bucket(cell.gain).add(cell)
        if self.maxgain < cell.gain:
            self.maxgain = cell.gain


    # 渡されたセルをバケツリストから取り出す関数
    # 取り出すセルのゲインがmaxgainと同じかつ、
    # そのセルの入っているバケツに他のセルがいないのなら、ゲインの更新を行う
    def remove_cell(self, cell):
        self.__bucket(cell.gain).remove(cell)

        if cell.gain == self.maxgain:
            while self.maxgain > -self.pmax - 1:
                if len(self.__bucket(self.maxgain)) > 0:
                    break
                else:
                    self.maxgain -= 1

    # gainの値を持つセルのリストを返す
    def cell_list(self, gain):
        for cell in self.__bucket(gain):
            yield cell

    def __bucket(self, gain):
        return self.bucket_list[self.pmax + gain]




# 全てのフリーなセルのゲインの初期化を行う関数
# ネットごとに、
# 必要ならば、maxgainの更新を行う
def init_gain(init_cell_list, free_cell_set, bucket_sort, network, WhichBlock):

    for cell in init_cell_list:
        cell.gain = 0

    bucket_sort.maxgain = -bucket_sort.pmax - 1

    for bucket in bucket_sort.bucket_list:
        bucket.clear()


    for net_index in network.net_num:
        a_num = 0
        b_num = 0
        for cell in network.cell_connect_net_list(net_index):
            if cell.which_block == WhichBlock.A:
                a_num += 1
            else:
                b_num += 1

            if a_num > 1 and b_num > 1:
                break
        else:
            if a_num == 1:
                for cell in init_cell_list:
                    if cell.which_block == WhichBlock.A:
                        cell.add_gain(1)
                    else:
                        cell.add_gain(-1)

    for cell in init_cell_list:
        bucket_sort.add_cell(cell)
        free_cell_set.add(cell)


# セルのゲインを計算する関数
def calc_gain(cell, from_block, network, WhichBlock):

    g = 0
    for net in cell.net_list:
        fn = 0
        tn = 0
        for neighbor_cell in network.cell_connect_net_list(net):
            if neighbor_cell.which_block == from_block.which_block:
                fn += 1
            else:
                tn += 1
            if fn > 1 and tn > 1:
                break

        if fn == 1:
            g += 1
        elif tn == 0:
            g -= 1

    return g


# ベースセルの隣人のゲインを更新する関数
# ベースセルが属するネットをbase_netとし、
# base_netに属するすべてのフリーなセルに対して計算を行う
def update_naighbor_gain(base_cell, free_cell_set, bucket_sort, WhichBlock):

    for base_net in base_cell.net_list:
        for neighbor_cell in net_list[base_net]:
            if neighbor_cell in free_cell_set:

                if neighbor_cell.which_block == WhichBlock.A:
                    bucket_a.remove_cell(neighbor_cell)
                    new_gain = calc_gain(neighbor_cell, block_a, network, WhichBlock)
                    neighbor_cell.set_gain(new_gain)
                    bucket_a.add_cell(neighbor_cell)

                else:
                    bucket_b.remove_cell(neighbor_cell)
                    new_gain = calc_gain(neighbor_cell, block_b, network, WhichBlock)
                    neighbor_cell.set_gain(new_gain)
                    bucket_.add_cell(neighbor_cell)



# バケツの中にセルが存在するゲインの中で、
# 引数として与えられたゲインの次に大きなゲインを返す
def search_next_gain(self, gain, bucket_sort):

    next_gain = gain - 1
    while next_gain > -bucket_sort.pmax - 1:
        if len(bucket_sort.cell_list(next_gain)) > 0:
            break
        else:
            next_gain -= 1

    return next_gain


# 渡されたバケツの中で最も望ましいサイズのセルを返す関数
# 最も望ましいセルは、
# 移動後に、rw - smax <= |A| <= rW + smax を満たすセルの中で、
# rW - |A|の絶対値が最も小さいセルである。
# rW - smax <= |A| <= rW + smax を満たすセルが与えられたバケツ内にないなら、
# best_size_cellはNoneを返す
def search_bestsize_cell(block_a, block_b, bucket_cell_list, WhichBlock):

    best_size_a = block_a.best_size
    best_size_b = block_b.best_size
    total_cell_size = block_a.size + block_b.size
    dif_a = total_cell_size
    dif_b = total_cell_size

    for cell in bucket_cell_list:
        if cell.which_block == WhichBlock.A:
            after_block_size = block_a.size - cell.size
            if after_block_size > block_a.min_size_constraint:
                if dif_a > abs(best_size_a - after_block_size):
                    best_size_cell_a = cell
                    dif_a = abs(best_size_a - after_block_size)

        else:
            after_block_size = block_b.size - cell.size
            if after_block_size > block_b.min_size_constraint:
                if dif_b > abs(best_size_b - after_block_size):
                    best_size_cell_b = cell
                    dif_b = abs(best_size_a - after_block_size)

    return best_size_cell_a, dif_a, best_size_cell_b, dif_b


# ベースセルを決める関数
# ベースセル
# うごかせるセルが無い場合、Noneを返す
def search_basecell(block_a, block_b, bucket_sort, WhichBlock):

    search_gain = bucket_sort.maxgain

    while search_gain > -bucket_sort.pmax - 1:
        search_cell_list = bucket_sort.cell_list(search_gain)
        best_cell_a, dif_a, best_cell_b, dif_b = search_bestsize_cell(block_a, block_b, search_cell_list, WhichBlock)

        if block_a.min_cell_num_constraint == block_a.cell_num:
            if best_cell_b == None:
                search_gain = search_next_gain(search_gain, bucket_sort)
            else:
                return best_cell_b
        elif block_b.min_cell_num_constraint == block_b.cell_num:
            if best_cell_a == None:
                search_gain = search_next_gain(search_gain, bucket_sort)
            else:
                return best_cell_a

        if best_cell_a == None:
            if best_cell_b is None:
                search_gain = search_next_gain(search_gain, bucket_sort)
            else:
                return best_cell_b

        elif best_cell_b == None:
            return best_cell_a

        else:
            if dif_a <= dif_b:
                return best_cell_a

            else:
                return best_cell_b


    return None



# ネットワークのパーティションを行う関数
# パーティション中に現れたもっとも小さなカットセットの値とその時のブロックAとブロックBを返す
def partition(cutset, free_cell_set, init_cell_list, block_a, block_b, bucket_a, bucket_b, network, WhichBlock):

    min_cutset_size_in_pass = network.net_num + 1


    # セルのゲインの初期化
    init_gain(init_cell_list, free_cell_set, bucket_sort, network, WhichBlock)

    # init_cell_setは空になる
    init_cell_list.clear()


    # ベースセルが見つからなくなるまでループ
    while True:
        # ベースセルの選択
        basecell = search_basecell(block_a, block_b, bucket_sort, WhichBlock)

        if basecell is not None:

            if basecell.which_block == WhichBlock.A:
                from_block = block_a
                to_block = block_b
            else:
                from_block = block_b
                to_block = block_a

            # ベースセルを移動
            from_block.remove_cell(basecell)
            bucket_sort.remove_cell(basecell)
            to_block.add_cell(basecell)
            init_cell_list.append(basecell)
            free_cell_set.remove(basecell)
            cell.switch_block(to_block.which_block)

            # ベースセルの隣人のゲインを更新
            update_neighbor_gain(basecell, network, free_cell_set, block_a, block_b, bucket_sort)


            # カットセットをベースセルのゲインだけ変化させる
            cutset -= basecell.gain

            # そのパス中最も小さいcutsetの値を持つ
            if cutset_size < min_cutset_size_in_pass:
                min_cutset_size_in_pass = cutset
                min_cutset_block_a_in_pass = set(block_a.cell_set)
                min_cutset_block_b_in_pass = set(block_b.cell_set)

        else:
            return min_cutset_size_in_pass, min_cutset_block_a_in_pass, min_cutset_block_b_in_pass
