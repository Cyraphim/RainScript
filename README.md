# RainScript
A simple BASIC/Python style programming Lanugage

# How to use
## Datatypes
Rainscript is not a strongly typed language. This means that you can store any datatype in any variable. This allows users to rapidly prototype algorithms without having to account for datatypes. There are 3 types of data that can be stored
  - Integer (1, 23, 1000)
  - Floating point values (3.1415, 1.414, 6.25)
  - "Strings" ("Adam", "Pritchard", "Hugh Darrow")
  
## Variables
variables must be assigned using the 'assign' keyword
```
  assign <variable_name> = <variable value>
```
The assign keyword applies to every assignment operation. if a variable has already been assigned, the value can only be changed if the assign keyword is used again

## If Else Statements
There are three kinds of if-else statements
### Only if
This executes a block of code only if the condition given is met
```
  if <condition> then
    #block of code
  end
```
Here the <condition> doesnt have to be in brackets. eg. ` speed <= 500 `

### if-else
This executes a certain block of code if the condition given is met, but if it is not met, then execution moves to a different, defined block of code
```
if <condition> then
  #block of code
else
  #second block of code
end
```
Not that then isnt required in the else statement

###if-else-if
This type of statement is used to execute blocks of code based on multiple conditions
```
if <condition> then
  #block of code
else if <second_condition> then
  #second block of code
else
  #third block of code
end
```
These else if chains can be added indefinitely as long as it is closed with an 'end' keyword
 
 ## For Loops
 ```
 for i = <start_number> to <end_number> then
  #block of code
end
```
A for loop executes a block of code until the value of 'i' reaches from the start value, to the end value.
The value can also be manipulated inside the loop as its scope exists as soon as it is assigned.
Infinite loops are possible, be careful with your logic!

## While Loops
```
  while <condition> then
    #block of code
  end
```
A while loop executes a block of code as many times as the condition given is met. A for loop automatically plans for the loop to end at some point, but in a while loop, the decision to end the loop is entirely on the programmer. Loops can easily be broken out of with the help of control statements.

## Functions
### Single line functions
```
block <function_name>( <...parameters>) -> #line of code
```
A single line function can be used to execute a single line of code in a short way. Its useful for something like executing a loop in only small statement

### Multi line functions
```
block <function_name>(<...parameters>)
  #block of code
end
```
A multi line function allows the programmer to execute multiple lines of code in a small statement. For an example, you can check out the TextAdventureGame.rain in the Rain folder.

## Lists
Data can also be stored in lists. The abstract way of thinking of lists would be to consider it a series of variables with the same name
```
assign <listname> = [1, 3.1415, "Adam"]
```
While usually advised to use the same datatype for all the elements of a list. Rainscript allows programmers to have multiple datatypes in the same list.

To access a value from the list we use the '/' operator
```
<listname>/0
#this will return the first value of the list

<listname>/3
#this will return the 4th value of the list
```
Unfortunately, users cannot assign values to elements of the list by indexing as the subscript operator returns by value and not by reference

## Control Statements
### Break
```
for i = 1 to 10 then
  print(i)
  if i > 5 then
    break
  end
end
```
The output will be
```
1
2
3
4
5
```
Even though the for loop is supposed to print the value of i going from 1 to 9, it stops at 5 because once the if condition is met, the break statements stops the loop from execution

### Continue
```
for i = 1 to 10 then
  if i == 5 then
    continue
  end
  print(i)
end
```
The output will be
```
1
2
3
4
6
7
8
9
```
Here as you can see, if the value of i is 5, continue will stop the current iteration of the loop from running, but the loop itself wont stop executing

### return
```
block add_5(value)
  return value + 5
end

assign val = add_5(10)
assign twenty = add_5(val)

print(val)
print(twenty)
```

The output will be
```
15
20
```
Here, the value that is given after 'return' is the output of the function. in the case of add_5, the value of that is given in the function is increased by 5 and returned as the output of the function

## Built-in functions
There are many built in functions that allow us to expand the feature set of the code
- print(<var>) : Prints <var> to the console screen
- print_ret(<var>) : Prints <var> to the console screen, and also returns the value
- input() : Prompts the user to give an input, which is then the return value of the function
- input_int() : Prompts the user to give an input, and repeatedly asks until the value given is an integer
- clear() / cls() : Flushes the console screen
- is_num(<var>) / is_str(<var>) / is_list(<var>) / is_block(<var>) : returns true if the value given is of the datatype specified
- append(<list>, <var>) : adds the value to the last element of the given list
- pop(<list>) : removes the last value of the list
- extend(<list>, <list>) : similar to append except for lists
- len(<string>) /len(<list>) : returns the number of elements in the list, or the number of characters in the string
- run(<string>) : executes the *.rain file that is given. (happens in the same console) and can be used the same way include is used
- pause() : pauses execution of the program and prompts the user to press Enter/Return
- int(<var>) / float(<var>) / string(<var>) : converts the value given into the datatype specified



## Credits
- Tanuj Shrivastava: Project lead and Compiler Work
- Abhinav Shrivastava: Compiler work
- Shubham Singh: Editor work
- Arundhati Dhar: Editor Work
