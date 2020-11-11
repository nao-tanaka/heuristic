# バケツソートを作る関数
def make_bucket(block_a, block_b, cell_list, free_cell_list):

    # ゲインの取りうる値pmaxを求める
    # pmaxは初期に自由なセルの属するネットの数の最大値
    pmax = 0
    for n in free_cell_list:
        if len(cell_list[n]) > pmax:
            pmax == len(cell_list[n])

    # バケツリストをブロックA、Bに一つづつ作る
    # バケツリストの要素は-pmax~pmax
    bucket_a = [[] for n in range(2 * pmax + 1)]
    bucket_b = [[] for n in range(2 * pmax + 1)]

    return bucket_a, bucket_b, pmax


# セルのゲインを初期化する関数
def init_gain(free_cell_list, cell_list, net_list, bucket_a, bucket_b, block_a, block_b):

    # それぞれのバケツリストの、セルが存在する最も値の大きなバケツを指す
    maxgain_a = 0
    maxgain_b = 0
    # free_cell_listのすべてのセルに対して
    for c in free_cell_list:
        g = 0

        # セルcの属するネットがクリティカルかどうかを判定し、ゲインを増減させる
        # fnはネットnに属し、cの現在のブロックにいるセルの数
        # tnはネットnに属し、cと反対のブロックにいるセルの数
        if c in block_a:
            from_block = block_a
            from_bucket = bucket_a
            from_maxgain = maxgain_a
        else:
            from_block = block_b
            from_bucket = bucket_b
            from_maxgain = maxgain_b

        for n in cell_list[c]:
            fn = 0
            tn = 0
            for nc in net_list[n]:
                if nc in from_block:
                    fn += 1
                else:
                    tn += 1
                if fn > 1 && tn > 1:
                    break

            if fn == 1:
                g += 1
            elif tn == 0:
                g -= 1
            # bucket[0]はゲイン-pmax、[2pmax]がpmax、[(len(bucket) - 1) / 2]が0
        from_bucket[(len(from_bucket) - 1) / 2 + g].append(c)
        if from_maxgain < (len(from_bucket) - 1) / 2 + g:
            from_maxgain = (len(from_bucket) - 1) / 2 + g

    return maxgain_a, maxgain_b


# セルのゲインを計算する関数
# 名前はupdate_gainのほうが良いか？
def calc_gain(base_cell, cell_list, net_list, block_a, block_b, free_cell_list):

    # 移動前にクリティカルなネット、移動後にクリティカルなネットを調べる
    # 見つかったなら、そのネットに属するセルのゲインを更新する
    # cell_list[base_cell]より、ベースセルの属するネットを参照
    if base_cell in block_a:
        from_block = block_a
        to_block   = block_b
    else:
        from_block = block_b
        to_block   = block_a

    for n in cell_list[base_cell]:

        # ffはネットnに属し、cの現在のブロックにいるフリーのセルの数
        # ftはネットnに属し、cと反対のブロックにいるフリーのセルの数
        # lfはネットnに属し、cの現在のブロックにいるロックされているセルの数
        # ltはネットnに属し、cと反対のブロックにいるロックされているセルの数
        ffn = 0
        ftn = 0
        lfn = 0
        ltn = 0

        # net_list[n]より、ネットnに属するセルを見る
        for nc in net_list[n]:
            if nc in free_cell_list:
                if nc in from_block:
                    lfn += 1
                else:
                    ltn += 1
            else:
                if nc in from_block:
                    ffn += 1
                else:
                    ftn += 1

            if ltn > 1 && lfn > 0:
                break

            elif ftn > 1 && ffn > 2:
                break

        else:
            if ltn == 0:
                if ftn == 0:
                    for c in net_list[n]:
                        if not c in free_cell_list:

















# 入力として与えられたネットから、cell配列、net配列を作る
# class Input
# return セル数C, ネット数N, cell_list, net_list




# ブロックAとBに含まれるセル数の比r(0<r<1)を入力してもらう
# Aに固定するセル、Bに固定するセルを入力
# lock_a = []、lock_b = []


# 初期パーテイションの作成（A:Aに固定されたものと自由なセル全て、B:Bに固定されたもの）
A = [n for n in range(c)]
B = list(lock_b)

# free_cell_listは固定されていないセルのリスト


# ここからパーテイションの１パス

# class Partition
# 入力は A, B, free_cell_list
# return A, B, free_cell_list
def partition(block_a, block_b, frr_cell_list):

  # バケツリストの作成

  # 入力は A, B, free_cell_list
  # return bucket_list_A, bucket_list_B, maxgain_A, maxgain_B


    # 以下フリーなセルがなくなるまでループ

    # ベースセル(移動させるセル)を決める
    # maxgain_Aとmaxgain_Bを用いる
    # r +- ??% (??%は要考察)を満たしていないときは、rに近づくものを選ぶ
    # r +- ??% 以内ならば、r +- ??% から外れてしまうセルは選ばない


    # ベースセルをもう一方のブロックに移動させる
    # ベースセルをバケツリストから取り出し、free_cell_listに入れる
    # ベースセルと隣人(ネットで繋がっている)セルの、利得の再計算を行う
    # maxgainの変動がないか調べる
    # ベースセルの利得が正ならば、今までのカットセットの最小値と現在のカットセットの値を比べ、
