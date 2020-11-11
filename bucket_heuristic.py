#! /usr/bin/python3

from enum import Enum

from bucket_cell import Cell
from network import Network
from block import Block
from bucket_sort import BucketSort

debug = False

# セルがどちらのブロックにあるのかを表す
# transitionsの方が良いか
class WhichBlock(Enum):
    A = 1
    B = 2


# 全てのフリーなセルのゲインの初期化を行う関数
# ネットごとに、
# 必要ならば、maxgainの更新を行う
def init_gain(init_cell_list, free_cell_set, bucket_sort, network, WhichBlock):

    # ゲインを初期化するセルのゲインを0にする
    # for cell in init_cell_list:
    for cell in network.cell_list:
        cell.set_gain(0)

    # バケツソートのmaxgainを-pmax - 1にする
    bucket_sort.maxgain = -bucket_sort.pmax - 1

    free_cell_set.clear()

    # バケツソートを空にする
    for bucket in bucket_sort.bucket_list:
        bucket.clear()



    # ネットが接続しているセルのゲインに与える影響を計算する
    for net_index in range(network.net_num):
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
            for cell in network.cell_connect_net_list(net_index):
                if a_num == 1 and b_num == 1:
                    cell.add_gain(1)
                elif a_num == 1:
                    if cell.which_block == WhichBlock.A:
                        cell.add_gain(1)
                    else:
                        cell.add_gain(-1)
                elif a_num == 0:
                    cell.add_gain(-1)
                elif b_num == 1:
                    if cell.which_block == WhichBlock.B:
                        cell.add_gain(1)
                    else:
                        cell.add_gain(-1)
                elif b_num == 0:
                    cell.add_gain(-1)

    # 初期化するゲインをバケツソートとfree_cell_setに加える
    for cell in init_cell_list:
        bucket_sort.add_cell(cell)
        free_cell_set.add(cell)


# セルのゲインを計算する関数
def calc_gain(cell, network):

    g = 0
    for net in cell.net_list:
        fn = 0
        tn = 0
        for neighbor_cell in network.cell_connect_net_list(net - 1):
            if neighbor_cell.which_block == cell.which_block:
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
def update_neighbor_gain(base_cell, network, free_cell_set, bucket_sort):

    # for base_net in base_cell.net_list:
        # neighbor_cell_list = []
        # for neighbor_cell in network.cell_connect_net_list(base_net - 1):
            # bucket_sort.remove(neighbor_cell)
            # neighbor_cell_list.append(neighbor_cell)


    for base_net in base_cell.net_list:
        for neighbor_cell in network.cell_connect_net_list(base_net - 1):
            if neighbor_cell in free_cell_set:
                bucket_sort.remove_cell(neighbor_cell)
                new_gain = calc_gain(neighbor_cell, network)
                neighbor_cell.set_gain(new_gain)
                bucket_sort.add_cell(neighbor_cell)


# バケツの中にセルが存在するゲインの中で、
# 引数として与えられたゲインの次に大きなゲインを返す
def search_next_gain(gain, bucket_sort):

    next_gain = gain - 1
    while next_gain > -bucket_sort.pmax - 1:
        if len(bucket_sort.bucket_list[bucket_sort.pmax + next_gain]) > 0:
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
def search_bestsize_cell(block_a, block_b, bucket_cell_list):

    best_size_a = block_a.best_size
    best_size_b = block_b.best_size
    bestcell = None
    dif_from_best = block_a.size + block_b.size


    for cell in bucket_cell_list:

        if debug:
            print("searching:{}".format(cell.identifier))

        # block_aのセル数がセル数の制約と等しいなら、block_aのセルは選ばない
        if block_a.min_cell_num_constraint == block_a.cell_num and cell.which_block == block_a.which_block:
            continue
        # block_bのセル数がセル数の制約と等しいなら、block_bのセルは選ばない
        if block_b.min_cell_num_constraint == block_b.cell_num and cell.which_block == block_b.which_block:
            continue
        # block_aのサイズが最小のサイズの制約以下なら、block_aのセルは選ばない
        if block_a.min_size_constraint >= block_a.size and cell.which_block == block_a.which_block:
            continue
        # block_bのサイズが最小のサイズの制約以下なら、block_bのセルは選ばない
        if block_b.min_size_constraint >= block_b.size and cell.which_block == block_b.which_block:
            continue

        if cell.which_block == block_a.which_block:
            after_block_size = block_a.size - cell.size
            if after_block_size < block_a.min_size_constraint:
                continue
            temp_dif = abs(block_a.best_size - after_block_size)
            if temp_dif < dif_from_best:
                bestcell = cell
        else:
            after_block_size = block_b.size - cell.size
            if after_block_size < block_b.min_size_constraint:
                continue
            temp_dif = abs(block_b.best_size - after_block_size)
            if temp_dif < dif_from_best:
                bestcell = cell

    return bestcell

    # 旧バージョン
    # for cell in bucket_cell_list:

      # if cell.which_block == block_a.which_block:
            # after_block_size = block_a.size - cell.size
            # if after_block_size >= block_a.min_size_constraint:
                # if dif_a > abs(best_size_a - after_block_size):
                    # best_size_cell_a = cell
                    # dif_a = abs(best_size_a - after_block_size)

        # else:
            # after_block_size = block_b.size - cell.size
            # if after_block_size >= block_b.min_size_constraint:
                # if dif_b > abs(best_size_b - after_block_size):
                    # best_size_cell_b = cell
                    # dif_b = abs(best_size_a - after_block_size)

    # return best_size_cell_a, dif_a, best_size_cell_b, dif_b



# ベースセルを決める関数
# ベースセル
# うごかせるセルが無い場合、Noneを返す
def search_basecell(block_a, block_b, bucket_sort):

    search_gain = bucket_sort.maxgain

    while search_gain > -bucket_sort.pmax - 1:
        search_cell_list = bucket_sort.cell_list(search_gain)
        basecell = search_bestsize_cell(block_a, block_b, search_cell_list)

        if basecell is None:
            search_gain = search_next_gain(search_gain, bucket_sort)

        else:
            return basecell




# ネットワークのパーティションを行う関数
# パーティション中に現れたもっとも小さなカットセットの値とその時のブロックAとブロックBを返す
def partition(free_cell_set, init_cell_list, block_a, block_b, bucket_sort, network, WhichBlock):

    min_cutset_size_in_pass = network.net_num + 1
    min_cutset_block_a_in_pass = None
    min_cutset_block_b_in_pass = None

    # 初期パーティションにおけるcutsetの値を調べる
    # 両ブロックにセルを持つネットの数
    cutset_size = 0
    for net_index in range(network.net_num):
        cell_in_a = 0
        cell_in_b = 0
        for cell in network.cell_connect_net_list(net_index):
            if cell.which_block == block_a.which_block:
                cell_in_a += 1
            else:
                cell_in_b += 1
            if cell_in_a > 0 and cell_in_b > 0:
                cutset_size += 1
                break
    if debug:
        print("cutset_size:{}".format(cutset_size))

        print_init_cell = []
        for cell in init_cell_list:
            print_init_cell.append(cell.identifier)
        print("init_cell = {}".format(print_init_cell))

    # セルのゲインの初期化
    init_gain(init_cell_list, free_cell_set, bucket_sort, network, WhichBlock)

    # init_cell_setは空になる
    # init_cell_list.clear()

    if debug:
        for cell in network.cell_list:
            print("id:{} block:{} gain:{}".format(cell.identifier, cell.which_block, cell.gain))


    # ベースセルが見つからなくなるまでループ
    while True:
        # ベースセルの選択
        basecell = search_basecell(block_a, block_b, bucket_sort)

        if basecell is not None:

            if basecell.which_block == WhichBlock.A:
                from_block = block_a
                to_block = block_b
                next_block = WhichBlock.B
            else:
                from_block = block_b
                to_block = block_a
                next_block = WhichBlock.A

            # ベースセルを移動
            if debug:
                print("move_cell:{} gain = {}".format(basecell.identifier, basecell.gain))

            from_block.remove_cell(basecell)
            bucket_sort.remove_cell(basecell)
            to_block.add_cell(basecell)
            #init_cell_list.append(basecell)
            free_cell_set.remove(basecell)
            basecell.switch_block(next_block)

            # ベースセルの隣人のゲインを更新
            update_neighbor_gain(basecell, network, free_cell_set, bucket_sort)

            if debug:
                debug_cell_gain_list = []
                debug_cell_which_list = []
                for cell in network.cell_list:
                    debug_cell_gain_list.append(cell.gain)
                    if cell.which_block == block_a.which_block:
                        debug_cell_which_list.append("A")
                    else:
                        debug_cell_which_list.append("B")
                print(debug_cell_gain_list)
                print(debug_cell_which_list)




            # カットセットをベースセルのゲインだけ変化させる
            cutset_size -= basecell.gain

            if debug:
                print(cutset_size)

            if cutset_size < min_cutset_size_in_pass:

                # パーティションが、制約を満たしているかを調べる
                meet_constraint = True

                if block_a.cell_num < block_a.min_cell_num_constraint:
                    meet_constraint = False
                if block_b.cell_num < block_b.min_cell_num_constraint:
                    meet_constraint = False

                if block_a.size < block_a.min_size_constraint:
                    meet_constraint = False
                if block_b.size < block_b.min_size_constraint:
                    meet_constraint = False


                if meet_constraint:
                    min_cutset_size_in_pass = cutset_size
                    min_cutset_block_a_in_pass = list(block_a.cell_set)
                    min_cutset_block_b_in_pass = list(block_b.cell_set)

        else:
            return min_cutset_size_in_pass, min_cutset_block_a_in_pass, min_cutset_block_b_in_pass



# 与えられたネットワークを使い、データ構造を作る関数
def make_data_structure(problem):

    # problemには、cell_num、net_num
    # cell_connect_net_lists、net_connect_cell_lists, cell_size_list
    # lock_a_cell_set, lock_b_cell_set
    # block_size_ratio(0 < block_size_ratio < 1)
    # block_a_min_cell_num_constraint
    # block_b_min_cell_num_constraint
    # がある

    # セルのサイズの和total_cell_size
    # 初期にフリーなセルのサイズの最大値max_free_cell_sizeを調べる
    total_cell_size = 0
    max_free_cell_size = 0
    for i in range(problem.cell_num):
        size = problem.cell_size_list[i]
        total_cell_size += size
        if max_free_cell_size < size:
            if not i + 1 in problem.lock_a_cell_set and not i in problem.lock_b_cell_set:
                max_free_cell_size = size

    # block_aとblock_bを作る
    block_a = Block(total_cell_size, max_free_cell_size, problem.block_size_ratio, problem.block_a_min_cell_num_constraint, WhichBlock.A)
    block_b = Block(total_cell_size, max_free_cell_size, 1 - problem.block_size_ratio, problem.block_a_min_cell_num_constraint, WhichBlock.B)


    # パスの最初にゲインを更新するセルの集合init_cell_list
    # フリーなセルの集合free_cell_set
    init_cell_list = []
    free_cell_set = set([])


    # 初期パーテイションの作成（A:Aに固定されたものと自由なセル全て、B:Bに固定されたもの）
    # cell_listの作成
    cell_list = []
    cell_connect_net_lists = [[] for n in range(problem.net_num)]
    for cell_i in range(problem.cell_num):
        size = problem.cell_size_list[cell_i]
        net_list = problem.net_connect_cell_lists[cell_i]

        if cell_i + 1 in problem.lock_a_cell_set:
            cell = Cell(cell_i + 1, size, net_list, WhichBlock.A)
            cell_list.append(cell)
            for net_index in net_list:
                cell_connect_net_lists[net_index - 1].append(cell)
            block_a.add_cell(cell)
        elif cell_i + 1 in problem.lock_b_cell_set:
            cell = Cell(cell_i + 1, size, net_list, WhichBlock.B)
            cell_list.append(cell)
            for net_index in net_list:
                cell_connect_net_lists[net_index - 1].append(cell)
            block_b.add_cell(cell)
        else:
            if block_b.cell_num < block_b.min_cell_num_constraint:
                cell = Cell(cell_i + 1, size, net_list, WhichBlock.B)
                cell_list.append(cell)
                for net_index in net_list:
                    cell_connect_net_lists[net_index - 1].append(cell)
                block_b.add_cell(cell)
            else:
                cell = Cell(cell_i + 1, size, net_list, WhichBlock.A)
                cell_list.append(cell)
                for net_index in net_list:
                    cell_connect_net_lists[net_index - 1].append(cell)
                block_a.add_cell(cell)

            init_cell_list.append(cell)

    # networkを作る
    network = Network(cell_list, cell_connect_net_lists)


    # pmaxをnetworkから取得
    # pmaxは、セルが属するnet数の最大値
    pmax = 0
    for cell in network.cell_list:
        if len(cell.net_list) > pmax:
            pmax = len(cell.net_list)


    # バケツリストの作成
    bucket_sort = BucketSort(pmax)

    return network, block_a, block_b, bucket_sort, free_cell_set, init_cell_list



# 与えられたネットワークの、
# カットセットが最小となるような２つのブロックへの分割を見つける関数
def bucket_heuristic(network, block_a, block_b, bucket_sort, free_cell_set, init_cell_list):

    min_cutset_size = network.net_num
    min_cutset_block_a = list(block_a.cell_set)
    min_cutset_block_b = list(block_b.cell_set)


    # min_cutset_sizeが更新されたかを表す変数
    # updatedがFalseになると終了する
    updated = True

    while updated:

        roop_num = 1

        # ここからパーティションのパス
        # 1パスは動かせるセルがなくなるまで続く
        min_cutset_size_in_pass, min_cutset_block_a_in_pass, min_cutset_block_b_in_pass  = partition(free_cell_set, init_cell_list, block_a, block_b, bucket_sort, network, WhichBlock)


        # ここまでがパーティションの1パス
        # min_cutset_sizeとmin_cutset_size_in_passを比較して、
        # 同じならばループを抜けてsmallest_cutset, ブロックA,ブロックBを返して終了
        if debug:
            print("//////////////////////////////////////////////")
        if min_cutset_size > min_cutset_size_in_pass:
            min_cutset_size = min_cutset_size_in_pass
            min_cutset_block_a = min_cutset_block_a_in_pass
            min_cutset_block_b = min_cutset_block_b_in_pass

        else:
            updated = False
        roop_num += 1
        if roop_num == 4:
            updated = False


    # min_cutsetの時のパーティションが、制約を満たしているかを調べる
    meet_constraint = True

    block_a_cell_list = []
    for cell in min_cutset_block_a:
        block_a_cell_list.append(cell.identifier)
    print("block_a = {}".format(block_a_cell_list))
    print(min_cutset_size)
    if len(min_cutset_block_a) < block_a.min_cell_num_constraint:
        meet_constraint = False
    if len(min_cutset_block_b) < block_b.min_cell_num_constraint:
        meet_constraint = False

    min_cutset_block_a_size = 0
    for cell in min_cutset_block_a:
        min_cutset_block_a_size += cell.size

    if min_cutset_block_a_size > block_a.max_size_constraint:
        meet_constraint = False
    if min_cutset_block_a_size < block_a.min_size_constraint:
        meet_constraint = False

    if meet_constraint:
        return min_cutset_size, min_cutset_block_a, min_cutset_block_b
    else:
        print("制約を満たせませんでした")





if __name__ == "__main__":

    import sys

    # Trueならランダムなネットワークを作る

    random = True

    if random:
        from make_random_problem import RandomProblem
        print("max_cell_num:")
        max_cell_num = int(input())
        print("max_net_num:")
        max_net_num = int(input())
        print("max_cell_size:")
        max_cell_size = int(input())

        problem = RandomProblem(max_cell_num, max_net_num, max_cell_size)

    else:
        from sample_problem import SampleProblem
        problem = SampleProblem()


    network, block_a, block_b, bucket_sort, free_cell_set, init_cell_list = make_data_structure(problem)

    bucket_heuristic(network, block_a, block_b, bucket_sort, free_cell_set, init_cell_list)



    if random:
        print("cell_num:{} net_num{}".format(problem.cell_num, problem.net_num))

        print("net_connect_cell_lists")
        print(problem.net_connect_cell_lists)
        print("problem.cell_connect_net_lists")
        print(problem.cell_connect_net_lists)
        print("cell_size_list")
        print(problem.cell_size_list)
        print("lock_a_cell_set")
        print(problem.lock_a_cell_set)
        print("lock_b_cell_set")
        print(problem.lock_b_cell_set)
        print("block_size_ratio: {}".format(problem.block_size_ratio))
        print("block_a_min_cell_num: {}".format(problem.block_a_min_cell_num_constraint))
        print("block_b_min_cell_num: {}".format(problem.block_b_min_cell_num_constraint))
