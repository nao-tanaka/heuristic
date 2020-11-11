#! /usr/bin/python3

import re

from enum import Enum

from problem import Problem

debug = False

class State(Enum):

    CELL_NUM = 1
    NET_NUM = 2
    CELL_PIN = 3
    CELL_SIZE = 4
    LOCK_CELL_A = 5
    LOCK_CELL_B = 6
    MIN_CELL_NUM = 7


class NetworkReader:

    def __init__(self):
        self.cell_num = re.compile(r"cell_num\s+=\s+(\d+)")
        self.net_num = re.compile(r"net_num\s+=\s+(\d+)")
        self.cell_pin = re.compile(r"\((\d+),\s*(\d+)\)")
        self.cell_size = re.compile(r"\d+:\s*(\d+)")
        self.block_size_ratio = re.compile(r"block_size_ratio\s*=\s*(\d+).(\d+)")
        self.min_cell_num = re.compile(r"min_cell_num(\D)+\s+=\s+(\d+)")
        self.state = State.CELL_NUM


    def read(self, fin):
        self.state = State.CELL_NUM
        
        for line in fin:
            if self.state == State.CELL_NUM:
                result = self.cell_num.match(line)
                if result:
                    cell_num = int(result.group(1))
                    self.state = State.NET_NUM

            elif self.state == State.NET_NUM:
                result = self.net_num.match(line)
                if result:
                    net_num = int(result.group(1))
                    problem = Problem(cell_num, net_num)
                    self.state = State.CELL_PIN

            
            elif self.state == State.CELL_PIN:
                result = self.cell_pin.match(line)
                if result:
                    problem.add_connection(int(result.group(1)),int(result.group(2)))
                    
                elif re.compile(r"cell_size").match(line):
                        self.state = State.CELL_SIZE

            elif self.state == State.CELL_SIZE:
                result = self.cell_size.match(line)
                if result:
                    problem.cell_size_list.append(int(result.group(1)))
                
                elif re.compile(r"lock_a_cell").match(line):
                    self.state = State.LOCK_CELL_A
                    
            elif self.state == State.LOCK_CELL_A:
                if re.compile(r"lock_b_cell").match(line):
                    self.state = State.LOCK_CELL_B
                else:
                    problem.lock_a_cell_set.add(int(line))

            elif self.state == State.LOCK_CELL_B:
                result = self.block_size_ratio.match(line)

                if result:
                    block_size_ratio = float(result.group(1) + "." + result.group(2))
                    problem.block_size_ratio = block_size_ratio

                    self.state = State.MIN_CELL_NUM

                else:
                    problem.lock_b_cell_set.add(int(line))

            elif self.state == State.MIN_CELL_NUM:
                result = self.min_cell_num.match(line)

                if result:
                    if result.group(1) == "A":
                        problem.block_a_min_cell_num_constraint = int(result.group(2))
                    else:
                        problem.block_b_min_cell_num_constraint = int(result.group(2))

        if debug:
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

        return problem
    
                        
                                                                      
                                                        
                                                        
                

                    
            
