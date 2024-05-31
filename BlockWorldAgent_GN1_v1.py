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
            return "Table"
        else:
            return s_list[pos_r][pos_c - 1]

def find_ppx(list_val, s_list):
    #
    pos_r, pos_c = find_pos(list_val, s_list)
    # print("what was the list val: ", list_val)
    # print("what was the list? ", s_list)
    len_tower = len(s_list[pos_r])
    # print("what was the list length? ", len_tower)
    if s_list[pos_r][pos_c] == list_val:
        if pos_c >= (len_tower - 1):
            return "Air"
        else:
            return s_list[pos_r][pos_c + 1]


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
        self.block_status_count_dict = {}
        #
        self.init_six_dict = {}
        self.goal_sgx_dict = {}

        self.init_pix_dict = {}
        self.goal_pgx_dict = {}
        self.goal_pg_six_dict = {}
        #
        self.status_b = {}
        #
        self.ready_blocks = []
        self.stuck_blocks = []

    def solve(self, init_arr, goal_arr):
        #####
        # the init part
        #####
        self.bw_init(init_arr, goal_arr)
        # #####
        # # make lists of can move and can't move
        # #####
        # self.ready_blocks = [k for k, v in self.status_b.items() if v == "Ready"]
        # # print("what is ready_blocks? ", ready_blocks)
        # self.stuck_blocks = [k for k, v in self.status_b.items() if v == "Stuck"]
        # # print("what is stuck_blocks? ", stuck_blocks)
        #####
        # while ready_blocks and stuck_blocks:
        while self.ready_blocks or self.stuck_blocks:
            # print("what is ready_blocks? ", self.ready_blocks)
            # print("what is stuck_blocks? ", self.stuck_blocks)
            if self.ready_blocks:
                b = self.ready_blocks[0]
                s_g_b = self.goal_sgx_dict[b]
                self.move_block(b, s_g_b)
                # self.ready_blocks.pop(0)
            else:
                b = self.stuck_blocks[0]
                self.move_block(b, "Table")
                # self.stuck_blocks.pop(0)
            self.ready_blocks = [k for k, v in self.status_b.items() if v == "Ready"]
            self.stuck_blocks = [k for k, v in self.status_b.items() if v == "Stuck"]
        return self.all_paths

    def bw_init(self, init_arr, goal_arr):
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
            self.block_status_count_dict[b] = 0
            #
            self.init_six_dict[b] = find_ssx(b, self.init_case)
            self.goal_sgx_dict[b] = find_ssx(b, self.goal_case)
            self.init_pix_dict[b] = find_ppx(b, self.init_case)
            # self.init_pix_dict[b] = "Air"
            self.goal_pgx_dict[b] = find_ppx(b, self.goal_case)
            # self.goal_pgx_dict[b] = "Air"
            #self.goal_pg_six_dict = {}
            #
            self.status_b[b] = "Other"
        # print("#1: clear dict is \n", self.clear_dict, "\n and examined dict is \n", self.examined_dict)
        # print("#1: six_dict is \n", self.init_six_dict, "\n and sgx_dict is \n", self.goal_sgx_dict)
        # print("#1: init_pix_dict is \n", self.init_pix_dict, "\n and goal_pgx_dict is \n", self.goal_pgx_dict)
        ##
        # second, do the inpos(b) f(x) & if S_i_b != "Table", set clear(S_i_b) to false
        for b in self.all_blocks:
            self.position_block(b)
            s_i_b = self.init_six_dict[b]
            s_g_b = self.goal_sgx_dict[b]
            if s_i_b != "Table":
                self.clear_dict[s_i_b] = False
                self.init_pix_dict[s_i_b] = b
            if s_g_b != "Table":
                self.goal_pgx_dict[s_g_b] = b
        # third do the status
        for b in self.all_blocks:
            #do the status of the block
            self.status_block(b)
        # print("#3: status_block dict is \n", self.status_b)

    def status_block(self, b):
        # print("what was b? ", b)
        if b != "Air" and b != "Table":
            if self.block_status_count_dict[b] < 2:
                self.block_status_count_dict[b] += 1
                s_g_b = self.goal_sgx_dict[b]
                # print("for block ", b, ", the s_g_b is ", s_g_b)
                s_i_b = self.init_six_dict[b]
                # print("for block ", b, ", the s_i_b is ", s_i_b)
                #
                # print(" is block in position: ", self.in_position[b])
                # if s_g_b == "Table":
                #     print(" is s_g_b in position: ", True)
                # else:
                #     print(" is s_g_b in position: ", self.in_position[s_g_b])
                if (not self.in_position[b]) and self.clear_dict[b]:
                    if s_g_b == "Table":
                        self.status_b[b] = "Ready"
                        # print("STAT")
                    elif (self.in_position[s_g_b]) and self.clear_dict[s_g_b]:
                        self.status_b[b] = "Ready"
                        # print("STAT")
                    elif s_i_b == "Table":
                        self.status_b[b] = "Other"
                    else:
                        self.status_b[b] = "Stuck"
                else:
                    self.status_b[b] = "Other"
        #
        # self.ready_blocks = [k for k, v in self.status_b.items() if v == "Ready"]
        # self.stuck_blocks = [k for k, v in self.status_b.items() if v == "Stuck"]

    def move_block(self, a, b):
        # print("a is : ", a)
        # print("b is : ", b)
        s_i_a = self.init_six_dict[a]
        c_1 = s_i_a
        p_g_a = self.goal_pgx_dict[a]
        c_2 = p_g_a
        s_g_a = self.goal_sgx_dict[a]
        if s_i_a != "Table":
            p_g_sia = self.goal_pgx_dict[s_i_a]
            c_3 = p_g_sia
            self.clear_dict[s_i_a] = True
            self.init_pix_dict[s_i_a] = "Air"
            # print("p_g_sia is ", p_g_sia)
        else:
            c_3 = "Table"
        if b != "Table":
            self.clear_dict[b] = False
            self.init_pix_dict[b] = a
            if (s_g_a == b) and self.in_position[b]:
                self.in_position[a] = True
            else:
                self.in_position[a] = False
        else:
            if s_g_a == "Table":
                self.in_position[a] = True
            else:
                self.in_position[a] = False
                # print("self.in_position[a] ", self.in_position[a])
        #
        self.init_six_dict[a] = b
        #
        self.status_block(a)
        #
        # if c_1 != "Table" and c_1 != "Air":
        if c_1 != "Table":
            # print("c 1 is not table")
            self.status_block(c_1)
        # if c_2 != "Air" and c_2 != "Table":
        if c_2 != "Air":
            # print("c 2 is not Sky")
            self.status_block(c_2)
        # if c_3 != "Table" and c_3 != "Air":
        if c_3 != "Table":
            # print("c 3 is not table")
            self.status_block(c_3)
        self.actually_move(a, b)

    def actually_move(self, a, b):
        # print(" in actually_move")
        # print("a is ", a, "\n and b is ", b)
        # print(" the init list: ")
        # print(self.init_case)
        # print("  the goal list: ")
        # print(self.goal_case)
        # print("    the delta list: ")
        # print(self.delta_case)
        if a != "Table":
            pos_a_r, pos_a_c = find_pos(a, self.delta_case)
            self.delta_case[pos_a_r].pop(pos_a_c)
            #
            if b != "Table":
                pos_b_r, pos_b_c = find_pos(b, self.delta_case)
                self.delta_case[pos_b_r].append(a)
            else:
                new_tower = [a]
                self.delta_case.append(new_tower)
            #
            self.all_paths.append(tuple((a, b)))
            # print("NOW    the all_paths list: ")
            # print(self.all_paths)
        #return None

    def position_block(self, b):
        if b == "Table":
            return True
        # if b != "Table":
        if self.block_in_position_count_dict[b] < 2:
            self.block_in_position_count_dict[b] += 1
            if not self.examined_dict[b]:
                self.examined_dict[b] = True
                #
                s_i_b = self.init_six_dict[b]
                s_g_b = self.goal_sgx_dict[b]
                if s_i_b != s_g_b:
                    self.in_position[b] = False
                else:
                    self.in_position[b] = self.position_block(s_i_b)
            #
        return self.in_position[b]
