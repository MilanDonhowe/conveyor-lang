
from Conveyor.parser.parser import Tokenizer, print_tokens, Token_Type, read_program
from Conveyor.items.types import Conv_Type, Conv_Item
from Conveyor.queues.Numeric_Queues import Numeric_Queues
from copy import deepcopy
from collections import deque

# Class responsible for running programs
class Program_Queue(object):



    def __init__(self, main_queue, function_table):
        self.token_queue = main_queue

        # When calling a function we push the current token_queue environment 
        # onto this stack.  When a function ends we then pop this.
        self.token_queue_stack = list()

        self.func_table = function_table

        # Operator Queue Stack
        self.operator_queue_stack = list()

        # Data Queues
        self.operator_queue = deque()        
        self.numeric_queue = Numeric_Queues("main")
        self.string_queue = deque()



    def take_next_token(self):
        return self.token_queue.popleft()
    

    def push_data(self, items):
        for c_item in items.CONTENTS:
            self.get_queue_type(c_item).append(c_item)
    
    def get_queue_type(self, item):
        if item.TYPE == Conv_Type.OPERATOR:
            return self.operator_queue
        elif item.TYPE == Conv_Type.INTEGER:
            return self.numeric_queue
        else:
            return self.string_queue

    def evaluate_tokens(self):
        while (len(self.token_queue) > 0):
            this_token = self.take_next_token()

            # If we are pushing values onto the queue
            if (this_token.TYPE == Token_Type.PUSH_LIST):
                self.push_data(this_token)
            
            # If we are popping values off the queue
            elif (this_token.TYPE == Token_Type.POP):
                # Popped operation
                self.size_test(self.operator_queue, 1, "*")
                self.pop_operator()

            elif (this_token.TYPE == Token_Type.EXEC_CON):
                while (len(self.operator_queue) > 0):
                    self.pop_operator()

            # Conditional Operation
            elif (this_token.TYPE == Token_Type.IF_CON):

                first_push_list = self.take_next_token()
                else_clause = self.take_next_token()
                second_push_list = self.take_next_token()
                            
                self.size_test(self.numeric_queue, 2, "?")

                if (self.numeric_queue[0].VALUE == self.numeric_queue[1].VALUE):
                    self.push_data(first_push_list)
                else:
                    self.push_data(second_push_list)

            # @ operator --> specifies which numeric queue to push integers
            elif (this_token.TYPE == Token_Type.AT_CON):
                self.numeric_queue.at(this_token.CONTENTS)



    def size_test(self, queue, min_size, op):
        if (len(queue) < min_size):
            print(f"Error: insufficient items on queue for \"{op}\"")
            exit(2)

    def pop_operator(self):
        operator = self.operator_queue.popleft().VALUE

        if (operator.startswith('(') and operator.endswith(')')):
            # Function call => Change token Queue
            
            function_id = operator[1:len(operator)-1]

            if not (function_id in self.func_table.keys()):
                print(f"Error: no function named '{function_id}' specified.")
                exit(2)

            # Push current token queue onto stack
            self.token_queue_stack.append(self.token_queue)
            
            # Now place function table onto queue
            self.token_queue = deepcopy(self.func_table[function_id])
            
            # Also push operator queue onto the stack
            self.operator_queue_stack.append(self.operator_queue)
            self.operator_queue = deque()

            # call execute token function
            self.evaluate_tokens()

            self.operator_queue = self.operator_queue_stack.pop()
            self.token_queue = self.token_queue_stack.pop()

        elif (operator == "++"):
            self.size_test(self.numeric_queue, 1, operator)
            self.numeric_queue[0].VALUE += 1
  
        elif (operator == "--"):
            self.size_test(self.numeric_queue, 1, operator)
            self.numeric_queue[0].VALUE -= 1
        
        elif (operator == "+"):
            self.size_test(self.numeric_queue, 2, operator)
            first = self.numeric_queue[0].VALUE
            second = self.numeric_queue[1].VALUE
            self.numeric_queue.append(Conv_Item(Conv_Type.INTEGER, first+second))
        
        elif (operator == "log"):
            self.size_test(self.string_queue, 1, operator)
            msg = self.string_queue[0].VALUE
            print(msg)

        elif (operator == "strcmp"):
            self.size_test(self.string_queue, 2, operator)
            first_str = self.string_queue[0].VALUE
            second_str = self.string_queue[1].VALUE

            if (first_str == second_str):
                self.numeric_queue.append(Conv_Item(Conv_Type.INTEGER, 0))
            else:
                self.numeric_queue.append(Conv_Item(Conv_Type.INTEGER, 1))
        
        elif (operator == "take"):
            self.string_queue.append(Conv_Item(Conv_Type.STRING, input()))
        
        elif (operator == "popn"):
            self.size_test(self.numeric_queue, 1, operator)
            self.numeric_queue.popleft()
        
        elif (operator == "pops"):
            self.size_test(self.string_queue, 1, operator)
            self.string_queue.popleft()
        
        elif (operator == "cls"):
            self.string_queue.clear()

        elif (operator == "cln"):
            self.numeric_queue.clear()

        elif (operator == "ntos"):
            self.size_test(self.numeric_queue, 1, operator)
            self.string_queue.append(Conv_Item(Conv_Type.STRING, str(self.numeric_queue[0].VALUE)))

        elif (operator == "ston"):
            self.size_test(self.string_queue, 1, operator)
            if (self.string_queue[0].VALUE.isdecimal() or (self.string_queue[0].VALUE[1:].isdecimal() and self.string_queue[0].VALUE[0] == '-')):
                self.numeric_queue.append(Conv_Item(Conv_Type.INTEGER, int(self.string_queue[0].VALUE)))
            else:
                print("Error: attempt to parse non-integer from string via ston")
                exit(2)

        elif (operator == "exit"):
            exit(0)
        
        else:
            print(f"Unknown operator: {operator}")
            exit(2)
            



