import copy
import numpy as np


class BlockWorldAgent:
    def __init__(self):
        # If you want to do any initial processing, add it here.
        pass

    def solve(self, initial_arrangement, goal_arrangement):
        # Add your code here! Your solve method should receive
        # as input two arrangements of blocks. The arrangements
        # will be given as lists of lists. The first item in each
        # list will be the bottom block on a stack, proceeding
        # upward. For example, this arrangement:
        #
        # [["A", "B", "C"], ["D", "E"]]
        #
        # ...represents two stacks of blocks: one with B on top
        # of A and C on top of B, and one with E on top of D.
        #
        # Your goal is to return a list of moves that will convert
        # the initial arrangement into the goal arrangement.
        # Moves should be represented as 2-tuples where the first
        # item in the 2-tuple is what block to move, and the
        # second item is where to put it: either on top of another
        # block or on the table (represented by the string "Table").
        #
        # For example, these moves would represent moving block B
        # from the first stack to the second stack in the example
        # above:
        #
        # ("C", "Table")
        # ("B", "E")
        # ("C", "A")
        # pass
        block_world_agent = UnstackStack()
        return block_world_agent.solve(initial_arrangement, goal_arrangement)


def find_pos(list_val, s_list):
    pos_r = 0
    pos_c = 0
    #
    # numpy_arr = np.array(([s_list]))
    numpy_arr = np.array([s + [None] * (max(map(len, s_list)) - len(s)) for s in s_list])
    # print("what was the list as an array ", numpy_arr)
    pos_r, pos_c = np.where(numpy_arr == list_val)
    # print("what is pos_r: ", pos_r)
    # print("what is pos_c: ", pos_c)
    return pos_r[0], pos_c[0]
    # return pos_r, pos_c


def find_ssx(list_val, s_list):
    #
    # print("what was the list val: ", list_val)
    # print("what was the list? ", s_list)
    pos_r, pos_c = find_pos(list_val, s_list)
    # pos_r, pos_c = pos_r[0], pos_c[0]
    #
    if s_list[pos_r][pos_c] == list_val:
        if pos_c == 0:
            return 'TABLE'
        else:
            return s_list[pos_r][pos_c - 1]


class UnstackStack:
    def __init__(self):
        self.all_blocks = []
        self.all_paths = []
        self.clear_dict = {}
        self.examined_dict = {}
        #
        self.init_case = []
        self.goal_case = []
        self.delta_case = []
        #
        self.in_position = {}
        self.block_in_position_count_dict = {}
        #
        self.block_stack_count_dict = {}
        self.block_unstack_count_dict = {}
        ###
        # # first pos is concierge, second pos is S_i_x or S_g_x....or the whole sequence up until the block.....
        # self.goal_sgx_dict = {}
        # self.init_six_dict = {}
        # self.delta_ssx_dict = {}

    def solve(self, init_arr, goal_arr):
        self.init_case = copy.deepcopy(init_arr)
        self.goal_case = copy.deepcopy(goal_arr)
        self.delta_case = copy.deepcopy(init_arr)
        #
        temp_all_blocks = []
        for i in init_arr:
            temp_all_blocks += i
            # print("temp_all_blocks: ", temp_all_blocks)
        #
        self.all_blocks = copy.deepcopy(temp_all_blocks)
        #####
        # the init part
        #####
        # first add all blocks to clear and to examined
        for b in self.all_blocks:
            self.clear_dict[b] = True
            self.examined_dict[b] = False
            self.block_in_position_count_dict[b] = 0
            self.block_unstack_count_dict[b] = 0
            self.block_stack_count_dict[b] = 0
        # print("#1: clear dict is \n", self.clear_dict, "\n and examined dict is \n", self.examined_dict)
        ##
        # second, do the inpos(b) f(x) & if S_i_b != 'Table', set clear(S_i_b) to false
        for b in self.all_blocks:
            # if self.block_in_position_count_dict[b] < 2:
            self.position_block(b)
            # self.block_in_position_count_dict[b] += 1
            s_i_b = find_ssx(b, self.init_case)
            if s_i_b != 'TABLE':
                self.clear_dict[s_i_b] = False
        # print("#2: clear dict is \n", self.clear_dict)
        #####
        # the unstack part
        #####
        for b in self.all_blocks:
            if self.clear_dict[b]:
                # print("unstacking time")
                self.unstack_block(b)
        #
        # print("completed unstacking")
        #####
        # the stack part
        #####
        for b in self.all_blocks:
            if self.clear_dict[b]:
                # print("stacking time")
                self.stack_block(b)
        ##
        # if list(filter(None, self.delta_case)) == self.goal_case:
        return self.all_paths

    def stack_block(self, b):
        #
        if self.block_stack_count_dict[b] < 2:
            self.block_stack_count_dict[b] += 1
            if not self.in_position[b]:
                s_g_b = find_ssx(b, self.goal_case)
                if s_g_b != 'TABLE':
                    self.stack_block(s_g_b)
                self.move_block(b, s_g_b)
        #return None

    def unstack_block(self, b):
        if self.block_unstack_count_dict[b] < 2:
            self.block_unstack_count_dict[b] += 1
            s_i_b = find_ssx(b, self.init_case)
            if (not self.in_position[b]) and (s_i_b != 'TABLE'):
                c = s_i_b
                self.move_block(b, 'TABLE')
                self.unstack_block(c)
        #return None

    def move_block(self, a, b):
        # print(" in move_block")
        # print("a is ", a, "\n and b is ", b)
        s_i_a = find_ssx(a, self.init_case)
        s_g_a = find_ssx(a, self.goal_case)
        if s_i_a != 'TABLE':
            self.clear_dict[s_i_a] = True
        if b != 'TABLE':
            self.clear_dict[b] = False
            if (s_g_a == b) and self.in_position[b]:
                self.in_position[a] = True
            else:
                self.in_position[a] = False
        else:
            if s_g_a == 'TABLE':
                self.in_position[a] = True
            else:
                self.in_position[a] = False
        #
        self.actually_move(a, b)
        #return None

    def actually_move(self, a, b):
        # print(" in actually_move")
        # print("a is ", a, "\n and b is ", b)
        # print(" the init list: ")
        # print(self.init_case)
        # print("  the goal list: ")
        # print(self.goal_case)
        # print("    the delta list: ")
        # print(self.delta_case)
        if a != 'TABLE':
            pos_a_r, pos_a_c = find_pos(a, self.delta_case)
            ## self.delta_case[pos_a_r].pop(a)
            self.delta_case[pos_a_r].pop(pos_a_c)
            #
            if b != 'TABLE':
                pos_b_r, pos_b_c = find_pos(b, self.delta_case)
                self.delta_case[pos_b_r].append(a)
            else:
                new_tower = [a]
                self.delta_case.append(new_tower)
            #
            # print("NOW    the delta list: ")
            # print(self.delta_case)
            self.all_paths.append(tuple((a, b)))
            # print("NOW    the all_paths list: ")
            # print(self.all_paths)
        #return None

    def position_block(self, b):
        if b == 'TABLE':
            return True
        # if b != 'TABLE':
        if self.block_in_position_count_dict[b] < 2:
            self.block_in_position_count_dict[b] += 1
            if not self.examined_dict[b]:
                self.examined_dict[b] = True
                s_i_b = find_ssx(b, self.init_case)
                # print("for block ", b, ", its s_i_b is ", s_i_b)
                s_g_b = find_ssx(b, self.goal_case)
                # print("for block ", b, ", its s_g_b is ", s_g_b)
                if s_i_b != s_g_b:
                    self.in_position[b] = False
                else:
                    self.in_position[b] = self.position_block(s_i_b)
            #
        return self.in_position[b]
