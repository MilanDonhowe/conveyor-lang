```
=========================================================================================  
| ______     ______     __   __     __   __   ______     __  __     ______     ______    |
|/\  ___\   /\  __ \   /\ "-.\ \   /\ \ / /  /\  ___\   /\ \_\ \   /\  __ \   /\  == \   |
|\ \ \____  \ \ \/\ \  \ \ \-.  \  \ \ \'/   \ \  __\   \ \____ \  \ \ \/\ \  \ \  __<   |
| \ \_____\  \ \_____\  \ \_\\"\_\  \ \__|    \ \_____\  \/\_____\  \ \_____\  \ \_\ \_\ |
|  \/_____/   \/_____/   \/_/ \/_/   \/_/      \/_____/   \/_____/   \/_____/   \/_/ /_/ |
|=========================================================================================  
|                      A Queue-Centric Programming Language                              |
==========================================================================================  
                                                              
```



Interpreter Usage:
`python -m Conveyor [filename]`


Conveyor is a esoteric programming language which revolves around the manipulation of queues.  This language is currently implemented via
an interpreter written in Python 3.7.

In conveyor you push integers, strings and operators onto queues
and pop operators from the operator queue to perform computations.

## Pushing Items

In conveyor there are three types of queues:

1. Nuemric Queues (Hold Integers)
2. The String Queue (Holds Strings)
3. Operator Queues (Hold operator-items)

You can push items onto these queues via "push-lists" which are square brackets surrounding
items delimited by spaces.

For instance the push list ```[1 2 3]``` would push the integers 1, 2 and 3 onto the
numeric queue.  Whereas ```["Hello" "World"]``` would push the strings "Hello" and "World"
onto the string queue.

You can put any arrangement of items in a particular push-list.  For instance,
```["Hello" 123]``` would be a valid push-list that pushes "Hello" onto the string queue
and the integer 123 onto the numeric queue.

There are also operator items which we can push onto the operator stack.  You can see a list of
these operators under the section [operator-items](##operator-items)

Push-lists work sequentially from left-to-right, so the push-list ```[log pops]``` would first append the operator-item "log" and then the operator-item "pops"
to the operator queue.

## Popping Items

In order to actually compute things we "pop" items off the operator queue.  When an operator-item is popped off the operator
queue it executes some associated built-in functionality.

In order to pop off the first item you can use an asteriks (```*```) or if you want to pop and execute every item
on the operator queue you can use a dollar-sign (```$```).

So in order to write a "hello world" program we would first push the string ```"Hello World"``` onto the string queue and the
```log``` operator onto the operator-queue before popping it off.

Example Hello World Program: ```[log "Hello World"]*```

## Conditionals

Conditionals in Conveyor are conceptualized as a choice between two competing push-lists.

The syntax for a conditional looks similar to a ternary operator in most procedural programming languages:
```?[first push list]:[second push list]```.  

When the conveyor interpreter encounters the ```?``` operator it checks the first two items on the
current numeric queue.  If the first two items on the current numeric queue are equal than it executes
the first push-list.  Otherwise it will execute the second push-list.

As such we can make fun conditionals like so:

Example Conditional Program: ```[0 10 log]?["first two items on numeric queue are equal!"]:["first two items on numeric queue are NOT equal"]*```
Should output: ```first two items on numeric queue are NOT equal```

## Subroutines

Conveyor has support for subroutines which work like functions--without any of the neat lexical scoping, return values, safety, etc.

To define a subroutine you use the following syntax:
```
{subroutine_name;
	#Magic Conveyor Language Code Here
}
```
In order to call a subroutine you use the call operator ```(subroutine_name)```.  

So in order to call a subroutine named "print" we would do the following:
```
{print;
	[log pops]$
}
["I used a subroutine!" (print)]*
```

Two notes about subroutines:
They access the same numeric & string queues.  **However, they have their own operator queue.**  In order words if you were to push three operators onto the operator
queue ```[op1 (my_sub) op2 op3]$``` and the subroutine ```my sub``` had a push-list of ```[op4 op5]$``` then the order in which operators would be popped & executed
would be as follows: ```op1 -> op4 -> op5 -> op2 -> op3``` (Note if you didn't pop the operators in the my_sub subroutine they wouldn't be executed).

Subroutines are relatively powerful and can be used for some recursive loops:
```
# Example Loop Program
# prints "I am in a loop" 4 times using a recursive subroutine

# Subroutine
{loop;
    ?[log "Out of loop!" pops]
    :[++ log "Inside of loop" pops (loop)]
    $
}

[0 4 (loop)]$
```



## Selecting Numeric Queues

In Conveyor while there is only one string-queue there are infinite possible numeric-queues.  By default Conveyor uses a numeric queue called "main"
however, if you at any point in a program want to switch to a different numeric queue you can use the "at" (```@numeric_queue_name```) operator to switch queues.

So if we wanted to push the numbers 1 2 3 onto the "main" queue but the number 4 5 6 onto a custom queue called "alt" we would do the following:
```
[1 2 3]
@alt
[4 5 6]
```
Whenever you specify a new numeric queue Conveyor dynamically allocates the a new numeric queue with the given name.

Using push-lists, recursive sub-routines, conditionals and multiple numeric-queues allows for the creation of some neat programs.

An example recursive fibbonacci program is given as an example below:

```
# Fibbonaci Calculator in Conveyor!

{print;
    [log pops]$
}

{input;
    ["Which term do you want in the Fibbonaci sequence? (counting from zero): " (print)]$ 
    [take ston pops]$
    
    ?[log "0" exit]
    :[++]
    $
    ?[log "1" exit]
    :[++ (fibb)]
    $
}

{print_result;
    @fibb
    [popn ntos (print)]$
    [exit]$
}

{fibb;
    @main
    ?
        [(print_result)]
    :
        [++]$
    @fibb
    [+ popn (fibb)]$
}

# Execution starts here
@fibb
[1 1]
@main
[0 (input)]$
```


## Operator Items

|Operator Identifier| Name | Description|
|-------------------|------|------------|
| ```log```			|Log| prints first element on string queue into console.|
| ```+```			|Add| Calculates the sum of the first two elements on the numeric queue and appends it the end of the numeric queue|
|```take```			|Take User Input| Takes string of user input and appends it to the string queue|
|```++```			|Increment| Increments first item on current numeric queue|
|```--```			|Decrement| Decrements first item on current numeric queue|
|```strcmp```		|String Compare| Compares first two items on string queue.  If they are identical then a 0 is appended to the current numeric queue, otherwise a 1 is appended to the current numeric queue|
|```ntos```			|Number to string| Appends first item on numeric queue to the string queue as a string.|
|```ston```			|String to Number| Appends first item on string queue to numeric queue as a integer.|
|```popn```			|Pop Number| Pops first item on current numeric queue.|
|```pops```			|Pop String| Pops first item on string queue.|
|```cls```			|Clear String Queue| Empties out string queue.|
|```cln```			|Clear Numeric Queue| Empties out numeric queue.|
|```(subroutine_name)```|Subroutine call| Calls subroutine with given name.|
---------------------- 


There are two "levels of computation" available in Conveyor, control operators
which explicity direct program flow by direct queue-manipulations--and item operators
which are operators which exist on the "operator" queue.

```
===============DISCLAIMER=========================================================
In case it was not already clear, this language is not intended for anything
remotely associated with professional level code.  This language is intended as a
bit of a toy to play around with a model of computation entirely centered
around the Queue data-structure.
===================================================================================


	Grammer of the Language:

operator:	log|+|take|exit|++|--|rewind|\(.+?\)
integer:	-?\d+
string: 	".+"
item:		<integer> | <operator> | <string>
push-list:  [item1 item2 ...]
pop:		\*
exec:		\$
condition:	\? <push-list> : <push-list>
function:	{ (.+?) ; (<condition>|<push-list>|<pop>|<exec>)+}
```
