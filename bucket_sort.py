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

