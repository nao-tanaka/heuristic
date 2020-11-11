# �o�P�c�\�[�g�����֐�
def make_bucket(block_a, block_b, cell_list, free_cell_list):

    # �Q�C���̎�肤��lpmax�����߂�
    # pmax�͏����Ɏ��R�ȃZ���̑�����l�b�g�̐��̍ő�l
    pmax = 0
    for n in free_cell_list:
        if len(cell_list[n]) > pmax:
            pmax = len(cell_list[n])

    # �o�P�c���X�g���u���b�NA�AB�Ɉ�Â��
    # �o�P�c���X�g�̗v�f��-pmax~pmax
    bucket_a = [[] for n in range(2 * pmax + 1)]
    bucket_b = [[] for n in range(2 * pmax + 1)]

    return bucket_a, bucket_b, pmax


# �Z���̃Q�C��������������֐�
def init_gain(free_cell_list, cell_list, net_list, bucket_a, bucket_b, block_a, block_b):

    # ���ꂼ��̃o�P�c���X�g�́A�Z�������݂���ł��l�̑傫�ȃo�P�c���w��
    maxgain_a = 0
    maxgain_b = 0
    # free_cell_list�̂��ׂẴZ���ɑ΂���
    for c in free_cell_list:
        g = 0

        # �Z��c�̑�����l�b�g���N���e�B�J�����ǂ����𔻒肵�A�Q�C���𑝌�������
        # fn�̓l�b�gn�ɑ����Ac�̌��݂̃u���b�N�ɂ���Z���̐�
        # tn�̓l�b�gn�ɑ����Ac�Ɣ��΂̃u���b�N�ɂ���Z���̐�
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

            # bucket[0]�̓Q�C��-pmax�A[2pmax]��pmax�A[(len(bucket) - 1) / 2]��0
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

# �Z���̃Q�C�����v�Z����֐�
# �x�[�X�Z���Ɠ����l�b�g�ɑ�����Z���ɂ��āA�x�[�X�Z���̈ړ���̃Q�C�����v�Z���X�V����
# �x�[�X�Z�����ړ�������Ɏ��s
# ���O��update_gain�̂ق����ǂ����H
def calc_gain(base_cell, cell_list, net_list, block_a, block_b, bucket_a, bucket_b, free_cell_list):

    # net_list[base_cell] ����A�x�[�X�Z����������l�b�g�ɂ���
    for net in cell_list[base_cell]:

        # net_list[n] ����A�l�b�gn�ɑ�����Z���ɂ���
        # �l�b�gn�ɑ�����Z���́A�x�[�X�Z���̗אl(neighbor)�ƌĂсA�ȉ�n_cell�Ƃ���
        for n_cell in net_list[n]:
            g == 0

            # n_cell��������u���b�N�ŏꍇ��������
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


# �x�[�X�Z����I�Ԋ֐�

def select_basecell():

    # �܂��Apartition���v�����ꂽ�T�C�Y��𖞂����Ă��邩�ŏꍇ����������
    # rW - smax <= |A| <= rW + smax
    # �����ŁAr�͓��͂��ꂽ��
    # |A|,|B|�̓u���b�NA,B���ꂼ��ɑ�����Z���̃T�C�Y�̘a
    # W = |A| + |B|
    # smax �͏����Ƀt���[�ł���ő�̃Z���̃T�C�Y

    if


# ���͂Ƃ��ė^����ꂽ�l�b�g����Acell�z��Anet�z������
# class Input
# return �Z����C, �l�b�g��N, cell_list, net_list
def make_





# class Partition
# ���͂� A, B, free_cell_list
# return A, B, free_cell_list
def partition(block_a, block_b, frr_cell_list):
p
  # �o�P�c���X�g�̍쐬

  # ���͂� A, B, free_cell_list
  # return bucket_list_A, bucket_list_B, maxgain_A, maxgain_B


    # �ȉ��t���[�ȃZ�����Ȃ��Ȃ�܂Ń��[�v

    # �x�[�X�Z��(�ړ�������Z��)�����߂�
    # maxgain_A��maxgain_B��p����
    # r +- ??% (??%�͗v�l�@)�𖞂����Ă��Ȃ��Ƃ��́Ar�ɋ߂Â����̂�I��
    # r +- ??% �ȓ��Ȃ�΁Ar +- ??% ����O��Ă��܂��Z���͑I�΂Ȃ�


    # �x�[�X�Z������������̃u���b�N�Ɉړ�������
    # �x�[�X�Z�����o�P�c���X�g������o���Afree_cell_list�ɓ����
    # �x�[�X�Z���Ɨאl(�l�b�g�Ōq�����Ă���)�Z���́A�����̍Čv�Z���s��
    # maxgain�̕ϓ����Ȃ������ׂ�
    # �x�[�X�Z���̗��������Ȃ�΁A���܂ł̃J�b�g�Z�b�g�̍ŏ��l�ƌ��݂̃J�b�g�Z�b�g�̒l���ׁA


def partition():

    # ����ǂݍ��݁A�l�b�g���\������
    read():
    # return �Z����C, �l�b�g��N, cell_list, net_list

    # �u���b�NA��B�Ɋ܂܂��Z�����̔�r(0<r<1)����͂��Ă��炤
    # A�ɌŒ肷��Z���AB�ɌŒ肷��Z�������
    # lock_a = []�Alock_b = []


    # �����p�[�e�C�V�����̍쐬�iA:A�ɌŒ肳�ꂽ���̂Ǝ��R�ȃZ���S�āAB:B�ɌŒ肳�ꂽ���́j
    # free_cell_list�͌Œ肳��Ă��Ȃ��Z���̃��X�g
    A = [n for n in range(c)]
    B = list(lock_b)
    free_cell_list = []


    # �o�P�c���X�g�̍쐬
    bucket_a, bucket_b, pmax = make_bucket()


    # �Z���̃Q�C���̏�����
    maxgain_a, maxgain_b = init_gain()


    # �x�[�X�Z���̑I��
