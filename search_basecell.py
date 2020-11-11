def classify_cell(cell_list):
    cell_in_a = []
    cell_in_b = []
    
    for cell in cell_list:
        if cell.which_block == WhichBlock.A:
            cell_in_a.append(cell)
        else:
            cell_in_b.append(cell)

    return cell_in_a, cell_in_b

def search_bestsize_cell(find_block, cell_list, total_cell_size):
    best_size = find_block.best_size
    dif_from_best = total_cell_size
    
    best_size_cell = None

    for cell in cell_list:
        after_block_size = find_block.size - cell.size
        if after_block_size > find_block.min_size_constraint:
            if dif_from_best > abs(best_size - after_block_size):
                best_size_cell = cell
                dif_from_best = abs(best_size - after_block_size)

    return best_size_cell, dif_from_best
    
    


def search_bestsize_each_block(block_a, block_b, bucket_cell_list):

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


def search_basecell(block_a, block_b, bucket_sort):

    search_gain = bucket_sort.maxgain
    
    while search_gain > -bucket_sort.pmax - 1:
        search_cell_list = bucket_sort.cell_list(search_gain)
        best_cell_a, dif_a, best_cell_b, dif_b = search_bestsize_cell(block_a, block_b, search_cell_list)

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
    







def search_bestcell(block_a, block_b, bucket_cell_set):

    # 無限大がないので、ベストなバランスとの差を表すdif_from_bestは
    # この関数が呼ばれたときの、find_blockのサイズとベストなサイズとの差とする
    before_block_size = find_block.size
    best_size = find_block.best_size
    min_constraint = find_block.min_constraint
    max_constraint = find_block.max_constraint

    best_size_cell = None
    dif_from_best = abs(best_size - before_block_size)

    for cell in bucket_cell_set:
        after_block_size = before_block_size - cell.size
        if after_block_size > min_constraint:
            temp_dif_from_best = abs(best_size - after_block_size)
            if temp_dif_from_best < dif_from_best:
                best_size_cell = cell
                dif_from_best = temp_dif_from_best

    return best_size_cell, dif_from_best


def search_basecell(block_a, block_b, bucket_a, bucket_b):

    searchgain_a = bucket_a.maxgain
    searchgain_b = bucket_b.maxgain
    pmax = bucket_a.pmax

    basecell = None

    if block_a.cell_num <= block_a.min_cell_num_constraints:
        while searchgain_b > -pmax - 1:
            search_cell_set = bucket_b[pmax + searchgain_b]
            basecell, dif_from_best = search_bestcell(block_b, search_cell_set)
            if basecell is None:
                searchgain_b = bucket_b.search_next_gain(searchgain_b)
            else:
                return basecell

    elif block_b.cell_num <= block_b.min_cell_num_constraints:
        while searchgain_a > -pmax - 1:
            search_cell_set = bucket_a[pmax + searchgain_a]
            basecell, dif_from_best = search_bestcell(block_a, search_cell_set)
            if basecell is None:
                searchgain_a = bucket_a.search_next_gain(searchgain_a)
            else:
                return basecell

    else:
        # temp_maxgain_a == -pmax - 1 かつ、temp_maxgain_b == -pmax - 1 の時、
        # うごかせるセルはもうないため終了する
        while searchgain_a > -pmax - 1 or searchgain_b > -pmax - 1:
            # AとBのsearchgainによって分岐する
            # Aのsearchgainが大きいとき
            if searchgain_a > searchgain_b:
                search_cell_set = bucket_a[pmax + searchgain_a]
                basecell, dif_from_best = search_bestcell(block_a, search_cell_set)

                # basecell == Noneの時、
                # そのバケツ内にベースセルに適したセルはなかった
                # temp_maxgainを小さくして最初に戻る
                if basecell is None:
                    # temp_maxgain をバケツ内に存在する次に大きいゲインにする
                    searchgain_a = bucket_a.search_next_gain(searchgain_a)
                else:
                    return basecell

            # Bのsearchgainが大きいとき
            elif searchgain_b > searchgain_a:
                search_cell_set = bucket_b[pmax + searchgain_b]
                basecell, dif_from_best = search_bestcell(block_b, search_cell_set)

                # basecell == Noneの時、
                # そのバケツ内にベースセルに適したセルはなかった
                # searchgainを小さくして最初に戻る
                if basecell is None:
                    # temp_maxgain をバケツ内に存在する次に大きいゲインにする
                    searchgain_b = bucket_b.search_next_gain(searchgain_b)

                else:
                    return basecell

        # searchgain_a == searchgain_b の時、
        # それぞれのバケツの中で最もいいセルを選び、
        # 返ってきたdif_from_bestを比較してベースセルを決める
        else:
            search_cell_set_a = bucket_a[searchgain_a + pmax]
            bestcell_a, dif_from_best_a = search_bestcell(block_a, search_cell_set_a)

            search_cell_set_b = bucket_b[searchgain_b + pmax]
            bestcell_b, dif_from_best_b = search_bestcell(block_b, search_cell_set_b)


            # ここで四つに分岐する
            # まずbestcell_aがNoneであるかで分岐
            if bestcell_a is not None:

                # 次にbestcell_bがNoneであるかで分岐
                if bestcell_b is not None:
                    # bestcell_a,bestcell_bがともにNoneでないので、
                    # dif_from_bestを比較して小さい方のbestcellを返す
                    if dif_from_best_a <= dif_from_best_b:
                        basecell = bestcell_a
                        return basecell

                    else:
                        basecell = bestcell_b
                        return basecell

                else:
                    basecell = bestcell_a
                    return basecell

            else:
                # 次にbestcell_bがNoneであるかで分岐
                if bestcell_b is not None:
                    basecell = bestcell_b
                    return basecell

                else:
                    searchgain_a = bucket_a.search_next_gain(searchgain_a)
                    searchgain_b = bucket_b.search_next_gain(searchgain_b)



    # うごかせるセルが存在しなかった時
    # basecellは定義した時点から値が変わっていないので、Noneである
    return basecell
