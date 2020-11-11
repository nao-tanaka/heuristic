#! /usr/bin/python3

from enum import Enum

from naive_cell import Cell
from network import Network
from block import Block


# どちらのブロックかを表す
# transitionsの方が良いか
class WhichBlock(Enum):
    A = 1
    B = 2
    

    
# 与えられたセルのゲインを計算する関数
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


# ベースセルを探す関数
# フリーな全てのセルから探す
# 最もゲインが高く、ブロックのサイズに良い影響を与えるものを選ぶ
def search_basecell(network, block_a, block_b, free_cell_set):

    
    basecell = None
    max_gain = -network.net_num
    dif_from_best = block_a.size + block_b.size
    
    for cell in free_cell_set:

        
        # print("searching cell.{}".format(cell.identifier))

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
        
        cell_gain = calc_gain(cell, network)
        if cell_gain > max_gain:
            if cell.which_block == block_a.which_block:
                after_block_size = block_a.size - cell.size
                if after_block_size < block_a.min_size_constraint:
                    continue
                temp_dif = abs(block_a.best_size - after_block_size)
                if temp_dif < dif_from_best:
                    basecell = cell
                    max_gain = cell_gain
            else:
                after_block_size = block_b.size - cell.size
                if after_block_size < block_b.min_size_constraint:
                    continue
                temp_dif = abs(block_b.best_size - after_block_size)
                if temp_dif < dif_from_best:
                    basecell = cell
                    max_gain = cell_gain
    if basecell is None:
        print("basecell not found")
                    
    return basecell, max_gain



# セルを動かす中で現れた最小のカットセットサイズを持つブロックとか返す
def partition(network, block_a, block_b, next_free_cell_set):

    free_cell_set = set(next_free_cell_set)
    # next_free_cell_set.clear()

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
    
    min_cutset_size_in_pass = network.net_num
    min_cutset_block_a_in_pass = None
    min_cutset_block_b_in_pass = None
    

    for cell in network.cell_list:
        print("id:{} block:{}".format(cell.identifier, cell.which_block))
    

    while True:
        # ベースセルを探す
        basecell, gain = search_basecell(network, block_a, block_b, free_cell_set)

        # あれば移動
        if basecell is not None:

            if basecell.which_block == WhichBlock.A:
                from_block = block_a
                to_block = block_b
            else:
                from_block = block_b
                to_block = block_a

            print("move")
            print("id:{}, gain:{}".format(basecell.identifier, gain))

            from_block.remove_cell(basecell)
            to_block.add_cell(basecell)
            # next_free_cell_set.add(basecell)
            free_cell_set.remove(basecell)
            basecell.switch_block(to_block.which_block)

            cutset_size -= gain

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

        # なければ終了
        else:
            return min_cutset_size_in_pass, min_cutset_block_a_in_pass, min_cutset_block_b_in_pass, next_free_cell_set


# 与えられた問題から、naive_heuristicのためのデータ構造を作る
def make_data_structure(problem):

    total_cell_size = 0
    max_free_cell_size = 0
    for i in range(problem.cell_num):
        size = problem.cell_size_list[i]
        total_cell_size += size
        if max_free_cell_size < size:
            if not i + 1 in problem.lock_a_cell_set and not i in problem.lock_b_cell_set:
                max_free_cell_size =size

    block_a = Block(total_cell_size, max_free_cell_size, problem.block_size_ratio, problem.block_a_min_cell_num_constraint, WhichBlock.A)
    block_b = Block(total_cell_size, max_free_cell_size, 1 - problem.block_size_ratio, problem.block_a_min_cell_num_constraint, WhichBlock.B)

    next_free_cell_set = set([])

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
                print("cell{} add block_b".format(cell_i + 1))
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
                
            next_free_cell_set.add(cell)

    # networkを作る
    network = Network(cell_list, cell_connect_net_lists)


    return network, block_a, block_b, next_free_cell_set
    
        
# 与えられたネットワークの、
# カットセットが最小となるような２つのブロックへの分割を見つける関数
def naive_heuristic(network, block_a, block_b, next_free_cell_set):

    min_cutset_size = network.net_num
    min_cutset_block_a = list(block_a.cell_set)
    min_cutset_block_b = list(block_b.cell_set)
    
    
    # min_cutsetが更新される限り続ける
    # されなければFalseに
    updated = True

    while updated:
        min_cutset_size_in_pass, min_cutset_block_a_in_pass, min_cutset_block_b_in_pass, next_free_cell_set = partition(network, block_a, block_b, next_free_cell_set)

        print("min_cutset_size_in_pass = {}".format(min_cutset_size_in_pass))
        print("/////////////////////////////////////////////////////")
        if min_cutset_size > min_cutset_size_in_pass:
            min_cutset_size = min_cutset_size_in_pass
            min_cutset_block_a = min_cutset_block_a_in_pass
            min_cutset_block_b = min_cutset_block_b_in_pass

        else:
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

    print("block_a_size = {}".format(min_cutset_block_a_size))
    print("max_const = {}".format(block_a.max_size_constraint))
    print("min_const = {}".format(block_a.min_size_constraint))

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

    random = False
    
    if random: 
        from make_random_problem import RandomProblem
        print("max_cell_num:")
        max_cell_num = int(input())
        print("max_net_num:")
        max_net_num = int(input())
        print("max_cell_size:")
        max_cell_size = int(input())
    
        problem = RandomProblem(max_cell_num, max_net_num, max_cell_size)
        from sample_problem import Problem

    else:
        from sample_problem import SampleProblem
        problem = SampleProblem()
    
    network, block_a, block_b, next_free_cell_set = make_data_structure(problem)

    naive_heuristic(network, block_a, block_b, next_free_cell_set)

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
    
          
