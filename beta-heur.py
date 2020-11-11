# バケツソートを作る関数
def make_bucket(block_a, block_b, cell_list, free_cell_list):

    # ゲインの取りうる値pmaxを求める
    # pmaxは初期に自由なセルの属するネットの数の最大値
    pmax = 0
    for n in free_cell_list:
        if len(cell_list[n]) > pmax:
            pmax = len(cell_list[n])

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
            bucket_a[(len(bucket_a) - 1) / 2 + g].append(c)
            if maxgain_a < (len(bucket_a) - 1) / 2 + g:
                maxgain_a = (len(bucket_a) - 1) / 2 + g

        if c in block_b:
            for n in cell_list[c]:
                fn = 0
                tn = 0
                for nc in net_list[n]:
                    if nc in block_b:
                        fn += 1
                    else:
                        tn += 1
                    if fn > 1 && tn > 1:
                        break

                if fn == 1:
                    g += 1
                elif tn == 0:
                    g -= 1
            bucket_b[(len(bucket_b) - 1) / 2 + g].append(c)
            if maxgain_b < (len(bucket_a) - 1) / 2 + g:
                maxgain_b = (len(bucket_b) - 1) / 2 + g
    return maxgain_a, maxgain_b

# セルのゲインを計算する関数
# ベースセルと同じネットに属するセルについて、ベースセルの移動後のゲインを計算し更新する
# ベースセルを移動した後に実行
# 名前はupdate_gainのほうが良いか？
def calc_gain(base_cell, cell_list, net_list, block_a, block_b, bucket_a, bucket_b, free_cell_list):

    # net_list[base_cell] から、ベースセルが属するネットについて
    for net in cell_list[base_cell]:

        # net_list[n] から、ネットnに属するセルについて
        # ネットnに属するセルは、ベースセルの隣人(neighbor)と呼び、以下n_cellとする
        for n_cell in net_list[n]:
            g == 0

            # n_cellが属するブロックで場合分けする
            if n_cell in block_a:
                for n_net in cell_list[n_cell]:
                    fn = 0
                    tn = 0
                    for n_n_cell in net_list[n_net]:
                        if n_n_cell in block_a:
                            fn += 1
                        else:
                            tn += 1
                        if fn > 1 && tn > 1:
                            break
                    if fn == 1:
                        g += 1
                    elif tn == 0:
                        g -= 1

                for bucket in bucket_a:
                    if n_cell in bucket:
                        bucket.remove[n_cell]
                        bucket_a[(len(bucket_a) - 1) / 2 + g].append(n_cell)
                        if maxgain_a < (len(bucket_a) - 1) / 2 + g:
                            maxgain_a = (len(bucket_a) - 1) / 2 + g


            if n_cell in block_b:
                for n_net in cell_list[n_cell]:
                    fn = 0
                    tn = 0
                    for n_n_cell in net_list[n_net]:
                        if n_n_cell in block_b:
                            fn += 1
                        else:
                            tn += 1
                        if fn > 1 && tn > 1:
                            break
                    if fn == 1:
                        g += 1
                    elif tn == 0:
                        g -= 1

                for bucket in bucket_b:
                    if n_cell in bucket:
                        bucket.remove[n_cell]
                        bucket_b[(len(bucket_b) - 1) / 2 + g].append(n_cell)
                        if maxgain_b < (len(bucket_b) - 1) / 2 + g:
                            maxgain_b = (len(bucket_b) - 1) / 2 + g


# ベースセルを選ぶ関数

def select_basecell():

    # まず、partitionが要求されたサイズ比を満たしているかで場合分けをする
    # rW - smax <= |A| <= rW + smax
    # ここで、rは入力された比
    # |A|,|B|はブロックA,Bそれぞれに属するセルのサイズの和
    # W = |A| + |B|
    # smax は初期にフリーである最大のセルのサイズ

    if


# 入力として与えられたネットから、cell配列、net配列を作る
# class Input
# return セル数C, ネット数N, cell_list, net_list
def make_





# class Partition
# 入力は A, B, free_cell_list
# return A, B, free_cell_list
def partition(block_a, block_b, frr_cell_list):
p
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


def partition():

    # 問題を読み込み、ネットを構成する
    read():
    # return セル数C, ネット数N, cell_list, net_list

    # ブロックAとBに含まれるセル数の比r(0<r<1)を入力してもらう
    # Aに固定するセル、Bに固定するセルを入力
    # lock_a = []、lock_b = []


    # 初期パーテイションの作成（A:Aに固定されたものと自由なセル全て、B:Bに固定されたもの）
    # free_cell_listは固定されていないセルのリスト
    A = [n for n in range(c)]
    B = list(lock_b)
    free_cell_list = []


    # バケツリストの作成
    bucket_a, bucket_b, pmax = make_bucket()


    # セルのゲインの初期化
    maxgain_a, maxgain_b = init_gain()


    # ベースセルの選択
