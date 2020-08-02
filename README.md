|-> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> ->|
| Conveyor is a queue-centric programming language |
|-> -> -> -> -> -> -> -> -> -> -> -> -> -> -> -> ->|

# This file is under-construction!
## Info may be incorrect/misleading


Usage:
`python -m Conveyor [filename]`


Conveyor is a esoteric programming language which revolves around the
manipulation of queues.  This language is currently implemented via
an interpreter written in Python 3.7

In conveyor there are three types of queues:

1. Nuemric Queues (Hold Integers)
2. The String Queue (Holds Strings)
3. Operator Queues (Hold operator-items)

There are two "levels of computation" available in Conveyor, control operators
which explicity direct program flow by direct queue-manipulations--and item operators
which are operators which exist on the "operator" queue.



===============DISCLAIMER=========================================================
In case it was not already clear, this language is not intended for anything
remotely associated with professional level code.  This language is intended as a
bit of a toy to play around with a model of computation entirely centered
around the Queue data-structure.



===================CONTROL OPERATORS===================================================
	Push-Lists:		[]			-> Adds items to respective queues
	Execute:		$			-> Pops all items off operator queue and evaluates them.
	Pop:			*			-> Pops single value off operator queue and evaluates it.

	Condition:		?[]:[]		-> Checks of two front-most items on the numeric queue are
							   		equal.  If they are, the first push list gets executed.
							   		otherwise the second push list (list coming after the
							   		colon ":") gets executed.

	Queue Index Operator: @queueName -> Switches numeric queue to refer to queue under given name
	Subroutine: {name:code} 		 -> Defines a 'subroutine' (see subroutine section for details). 

====================QUEUE ITEMS==========================================================
Queue items are items which can be pushed onto the function queue.

Strings:		text surrounded by double quotes e.g. "wowza"
Numbers:		whole numbers e.g. -2, 4 or 200230
Operators:		keywords which match a particular builtin functionality.

====================ITEM OPERATORS========================================================
These are queue items which can pushed and popped onto the "operator queue."

This sub-category of data-items can be further sub-divided into three categories
based on their effects on the queues/program execution.

Non-popping Operators:
	These operators either add or modify items on the data queues
	without removing items from these queues.
	
	++	 ->	Increment: increments first item on numeric queue
	--   -> Decrement: decrements first item on numeric queue
	take -> Take:      takes line of string input from user
	ntos -> Number to String: Type-casts a copy of the first item from numeric queue 
			to the string queue.
	ston -> String to Number:  Attempts to type-cast a copy of the first item from the string queue
			to the numeric queue.  If the string contains any non-integer characters this will fail
			and crash the program.
	log    -> Log: prints out first item from string queue.
	strcmp -> String Compare: appends 0 to numeric queue if first two strings on string queue are identical.
							  otherwise appends 1 to numeric queue.

	+	   -> Add:	adds first two items from numeric queue and appends result to the end of the queue.
	popn   -> Pop Number: removes first item from the currently specified numeric queue.
	pops   -> Pop String: removes first item from the string queue.
	cln    -> clear numeric queue: removes all items from currently specified numeric queue.
	cls    -> clear string queue: removes all items from the currently specified string queue.

Control Flow Modifying:
	exit
	(id)	



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
