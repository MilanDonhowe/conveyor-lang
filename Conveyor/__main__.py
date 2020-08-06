# Conveyor Language Interpreter 
# Version 0.0.1.2
# By Milan Donhowe
#
# This code is incredibly messy and scuffed due to a lot of trial-and-error
# protoyping to try and make this language somewhat usable.

from sys import argv

def help_msg():
    print("\{Conveyor Interpreter Usage\}")
    print("python -m Conveyor filename.con")
    print("\{Additional Falgs\}")
    print("-tokens       --> prints out parsed token list for main subroutine")
    print("-table        --> prints out list of parsed subroutines")
    print("-table-tokens --> prints out list of parsed tokens for each subroutine")
    print("-help         --> shows this message")
    exit(1)


def handle_flags(argv, main, subroutine_table):
    if (len(argv) > 2):
        if "-help" in argv:
            help_msg()
        if "-tokens" in argv:
            print_tokens(main)
        if "-table" in argv:
            print(subroutine_table.keys())
        if "-table-tokens" in argv:
            for x in subroutine_table.keys():
                print(f"{x}'s Token List")
                print_tokens(subroutine_table[x])

if __name__ == "__main__":

    
    if (len(argv) < 2):
        print("No program supplied")
        exit(0)
    
    # Remove Comments from file and join lines into string.
    program_text = ""
    with open(argv[1], "r") as f:
        program_text = f.readlines()
        program_text = ''.join(filter(lambda ln: ln.startswith("#") == False, program_text))
    program_text = ''.join(program_text.split("\n"))

    # Parse source-code into token lists
    main, subroutine_table = read_program(program_text)

    # Handle Compiler Flags
    handle_flags(argv, main, subroutine_table)
   

    PQ = Program_Queue(main, subroutine_table)
    PQ.evaluate_tokens()
