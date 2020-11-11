#! /usr/bin/python3


if __name__ == "__main__":

    import sys
    import time



    random = False
    read_network = True

    if random:
        from make_random_problem import RandomProblem
        #from sample_problem import Problem

        print("max_cell_num(10以上):")
        while True:
            max_cell_num = int(input())
            if max_cell_num >= 10:
                break
            else:
                print("もう一度入力してください")
        print("max_net_num:")
        max_net_num = int(input())
        print("max_cell_size:")
        max_cell_size = int(input())

        problem = RandomProblem(max_cell_num, max_net_num, max_cell_size)

        print("make_problem_end")

    elif read_network:

        n = len(sys.argv)
        if n == 1:
            fin = sys.stdin
        elif n == 2:
            fin = open(sys.argv[1], "rt")
        else:
            print("引数間違い")
            exit(1)

        from network_reader import NetworkReader

        network_reader = NetworkReader()
        problem = network_reader.read(fin)
        

    else:

        from sample_problem import SampleProblem
        #from sample_problem import Problem

        problem = SampleProblem()

    naive_stime = time.process_time()

    from naive_heuristic import naive_heuristic, make_data_structure

    network, block_a, block_b, next_free_cell_set = make_data_structure(problem)

    naive_answer = naive_heuristic(network, block_a, block_b, next_free_cell_set)

    naive_etime = time.process_time()

    bucket_stime = time.process_time()

    from bucket_heuristic import bucket_heuristic, make_data_structure

    network, block_a, block_b, bucket_sort, free_cell_set, init_cell_list = make_data_structure(problem)
    
    bucket_answer = bucket_heuristic(network, block_a, block_b, bucket_sort, free_cell_set, init_cell_list)

    bucket_etime = time.process_time()


    debug = False
    if debug:
        print("cell_num:{} net_num{}".format(problem.cell_num, problem.net_num))

        print("net_connect_cell_lists")
        print(problem.net_connect_cell_lists)
        print("problem.cell_connect_net_lists")
        print(problem.cell_connect_net_lists)
        print("lock_a_cell_set")
        print(problem.lock_a_cell_set)
        print("lock_b_cell_set")
        print(problem.lock_b_cell_set)
        print("block_size_ratio: {}".format(problem.block_size_ratio))
        print("block_a_min_cell_num: {}".format(problem.block_a_min_cell_num_constraint))
        print("block_b_min_cell_num: {}".format(problem.block_b_min_cell_num_constraint))

    print("naive_cutset_size = {}".format(naive_answer[0]))
    print("bucket_cutset_size = {}".format(bucket_answer[0]))
    print("naive_time = {:10.4f}".format(naive_etime - naive_stime))
    print("bucket_time = {:10.4f}".format(bucket_etime - bucket_stime))
