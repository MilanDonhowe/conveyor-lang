# Parser Function
# Given a string representing the program, returns a list of tokens.
from enum import Enum, auto
from ..items.types import Conv_Item, Conv_Type, BUILTIN_ITEM_OPS
from string import whitespace
import re
from collections import deque

class Token_Type(Enum):
    PUSH_LIST   =   auto() #[]
    POP         =   auto() #*
    IF_CON      =   auto() #?
    ELSE_CON    =   auto() #:
    EXEC_CON    =   auto() #$
    AT_CON      =   auto() #@

QUEUE_OPERATORS = set(['?', '[', ']', '*', '$', '@', '{', '}'])

class Token(object):
    # type is enum
    # contents is a varying thing.  
    # Could be string or could be list of other tokens.
    def __init__(self, token_type, token_contents):
        self.TYPE = token_type
        self.CONTENTS = token_contents


def print_tokens(token_ls):
    for i, tk in enumerate(token_ls):
        if (tk.TYPE == Token_Type.PUSH_LIST):
            print(f"{i}. {tk.TYPE} -> " + ' '.join(map(lambda item: f"({item.TYPE} : {item.VALUE})", tk.CONTENTS)))
        elif (tk.TYPE == Token_Type.AT_CON):
            print(f"{i}. {tk.TYPE} -> {tk.CONTENTS}")
        else:    
            print(f"{i}. {tk.TYPE}")

# Reads text into "tokens" -> push_expression or pop or check_expression
def Tokenizer(program):
    tokens = deque()

    # We use a state-machine to parse in each expression
    currentCharacter = 0

    while (currentCharacter < len(program)):
        # if reading list
        this_token = None
        if (program[currentCharacter] == '['):

            this_token, currentCharacter = parse_push_list(program, currentCharacter)

        elif (program[currentCharacter] == '*'):
            this_token = Token(Token_Type.POP, None)
        
        elif (program[currentCharacter] == '?'):
            tokens.append(Token(Token_Type.IF_CON, None))
            currentCharacter += 1

            # Make sure first push-list exists.
            currentCharacter = check_next('[', currentCharacter, program)
            
            # Parse push-list
            first_token_list, currentCharacter = parse_push_list(program, currentCharacter)
            
            tokens.append(first_token_list)

            # Check for ELSE condition
            currentCharacter = check_next(':', currentCharacter, program)

            tokens.append(Token(Token_Type.ELSE_CON, None))

            this_token, currentCharacter = parse_push_list(program, currentCharacter)

        elif (program[currentCharacter] == '$'):
            this_token = Token(Token_Type.EXEC_CON, None)

        elif (program[currentCharacter] == "@"):
            queue_name = ""

            while (not program[currentCharacter+1] in QUEUE_OPERATORS):
                if (currentCharacter+1 >= len(program)):
                    print("Error: @ queue name reached end of input")
                    exit(2)
                currentCharacter += 1
                queue_name += program[currentCharacter]
            
            this_token = Token(Token_Type.AT_CON, queue_name.strip())

        if (this_token != None):
            tokens.append(this_token)
        
        currentCharacter += 1
    return tokens


def check_next(requestedChar, index, txt):
    while (txt[index] != requestedChar):
        index += 1
        if (index >= len(txt)):
            print(f"Error: Expected {requestedChar}, reached end of input instead.")
            exit(2)
        if (not txt[index] in whitespace) and (txt[index] != requestedChar):
            print(f"Error: unexpected symbol.  Got \"{txt[index]}\", expected \"{requestedChar}\".")
            exit(2)
    return index





def parse_push_list(txt, index):
    push_list_token = Token(Token_Type.PUSH_LIST, [])
    list_range = [index+1, -1]
    while (txt[index] != ']'):
        index += 1
        if (index >= len(txt)):
            # TODO: Make error reporting function
            print(f"Error: Unclosed Push List [ @ {list_range[0]}")
            exit(3)
    list_range[1] = index

    # We have starting and ending index of text contents
    item_text = txt[list_range[0]:list_range[1]]
    return (parse_push_items(push_list_token, item_text), index)

def parse_push_items(token, txt):
  
    # Use Regular Expressions to parse out identifiable items
    item_reg = re.compile(r'\(.+?\)|".+?"|[a-z]+|-?\d+|\+\+|--|\+')
  
    items = []

    while (len(txt) > 0):
        next_match = item_reg.search(txt)
        if (next_match == None):
            print(f"Error: Unidentifiable push-list contents, '{txt}''")
            exit(2)

        items.append(next_match.group())
        txt = txt[next_match.span()[1]:]


    # Finally, we parse these items into Conv_items
    items = parse_conv_items(items)    

    token.CONTENTS = items
    

    return token
    
# Converts list of push items as text e.g. "4", "+", "HELLO" into their object type.
def parse_conv_items(text_items):
    
    for index, text in enumerate(text_items):
        # if number
        if text.isdecimal() or (text[1:].isdecimal and text[0] == '-'):
            int_val = int(text)
            text_items[index] = Conv_Item(Conv_Type.INTEGER, int_val)
        # if operator
        elif text in BUILTIN_ITEM_OPS:
            text_items[index] = Conv_Item(Conv_Type.OPERATOR, text)
        # if string
        elif text.startswith("\"") and text.endswith("\""):
            text_items[index] = Conv_Item(Conv_Type.STRING, text)
        elif text.startswith("(") and text.endswith(")"):
            text_items[index] = Conv_Item(Conv_Type.OPERATOR, text)
        else:
            # Unidentifiable Push Item
            print(f"Error: Unidentifiable Push Item: {text}")
            exit(3)
    
    return text_items



def read_program(contents):
    # TODO: REMOVE COMMENTS FROM PROGRAM CONTENTS
    
    # FIND ALL FUNCTIONS & remove them from main program text
    func_regex = re.compile(r"\{(.+?);(.+?)\}", re.DOTALL)
    functions = {}
    
    func = func_regex.search(contents)

    while (func != None):
        
        # Parse token contents into function table
        functions[func.groups()[0].strip()] = Tokenizer(func.groups()[1])
        # Remove function from text
        contents = contents[:func.span()[0]] + contents[func.span()[1]:]
        # Get next function
        func = func_regex.search(contents)


    main_token_list = Tokenizer(contents)
    return (main_token_list, functions)