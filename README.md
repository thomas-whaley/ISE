# ISE Programming Language

## An Intuitive, Simple and Elegant Programming Language

### Designed for professionals

---

## Design philosophy

The age-old promises of elegance and intuition in a programming language that comes close to the nature and power of human thought have been proposed many times, and one may find that no language they have used comes quite close to the capability of their mind. It is for this reason that the development of ISE began. It is believed that this language may finally deliver upon these goals of such elegance, simplicity and beauty, ensuring that all users may realise the same thing.

## An abstract overview on ISE

ISE is a small-command, large-results language. It only has 14 operators because it only needs 14 operators. It is also a one step at a time language, to a avoid confusing and nested code structure. 

---

## Getting started

Make sure to have the latest version of [Python](https://www.python.org/downloads/) installed.

ISE programs are written in the `.ise` file format. Make sure to save your file in `.ise` to run. 

To run the ISE interpreter, run it like any other Python program. In the directory that `ise.py` is saved, type in the command:
```
python ise.py your_ise_file.ise
```

For those who are running Mac OS or Linux, you can run the file `setup.py` file to make it easier to run files. 

Run the command to turn `ise` into a command.
```
python setup.py
```
This is still in progress so its janky lol

After running `setup.py` you should be able to run either of the commands
```
ise your_ise_file.ise
./ise your_ise_file.ise
```

---

## Functionality

Keeping with the design philosophy, operators and keywords are kept in their most simple form: single characters. There is no need for any more, so why go for more? Whitespace is overrated.

### Program structure

A valid program ends with the keyword `|`. A programme will not run unless it has a `|` at the end. 
Therefore the most simple program in ISE is:

```
|
```

### Variables

A valid variable in ISE is a character in the set

```
!@#$%^&*()
```

To define a variable, one must use the character `~` before the variable name. This sets the variables value to zero. Note that a variable can be defined more than once. 

For example the program below defines a variable named `!`, and ends the program. As the program is running, `!` will have a value of `0`.

```
~!|
```

We can use the define operator more than once in a program, for example

```
~!~@~#~!~@~#|
```


### Numbers

A number in ISE is any `1`-`9` single digit character. A number by itself is considered invalid. It is only valid when inside a conditional or operator.

### Operators

An operator in ISE performs arithmetic. This is comprised of addition, subtraction, multiplication, and division. The keywords for these operators are as follows:

- Addition: `.`
- Subtraction: `,`
- Multiplication: `:`
- Division: `;`

These operators all follow the syntax of `OPERATOR VARIABLE NUMBER|VARIABLE`

For example, adding 3 to variable `!` would be as follows:

```
.!3
```

Note that this operation does not return a value, it only updates a variable. Also note that when dividing, the result will always be an integer.

Some examples of operations include:

```
.!#
:@8
,&9
```

Note that `.2!` is invalid and makes no sense. Think of it as add a value to a variable and write that to the variable, intuitively. 

### Conditional Statements

A conditional statement in ISE is either an if or while statement. The keywords for these are as follows:

- If: `>`
- While: `-`

The syntax for these statements are both of `CONDITIONAL [NOT] NUMBER|VARIABLE NUMBER|VARIABLE LPAREN CODE RPAREN`. This can be thought of as conditional statement runs the code if the first value is the same as the second number, or if the optional not flag is set, if the first value is not the same as the second number.

We have declared a few keywords that we haven't defined yet, so let's do that now.

- Not: `"`
- Left parenthesis: `+`
- Right parenthesis: `<`

An example of a conditional is as follows. This program will subtract `!` by `4` if and only if `!` is `4`.

```
>!4+,!4<
```



Other examples:
```
-"!@+.#<
-11+:!2<
>1#+;#2<
```

### I/O

There are two types of output in ISE, print the value of a variable, and print the ascii value of a variable. The keywords for these are as follows:

- Print value: `'`
- Print ascii character: `` ` ``

There is only one source of input in ISE. This takes user input and expects an integer to write to a variable.

- Input: `\`

An example of these in use is:

```
`#
'7
\%
```

### Misc

- ?: `b`

---

## Example programs

The program to print `Hello World!` with one variable is:
```
~!.!8:!9`!.!9.!9.!9.!2`!.!7`!`!.!3`!~!.!3:!9.!5`!~!.!1:!9:!9.!6`!.!9.!9.!6`!.!3`!,!6`!,!8`!~!.!3:!9.!6`!|
```

The fibonacci sequence can be written as:
```
~!.!1~@-00+~#.#!.#@'#~@.@#~#.#!.#@'#~!.!#<|
```

## Bugs and issues

All bugs and issues are features. This solves this hassle.

yes i did run out of energy writing this.