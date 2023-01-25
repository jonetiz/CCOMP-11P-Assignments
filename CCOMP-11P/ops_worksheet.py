# operations worksheet written by Joe Manlove
# Used in Programming and Methodologies 1 in Python
# Last Revised 5/19/2020
# Instructions: You should write code below each comment attempting to carry out the instructions
# you should also include print statements about what you're doing so the output is readable.
# There's an example at the start of the Boolean Section
# I've included some print statements to keep sections straight, no need to change them.
# in cases where errors are generated, feel free to comment out your attempt, but please explain the error
# This section is for numerical operations
print('Numerical Operations Section')
# make two numerical values x and y, initialize them to 4 and 9 respectively
x = 4
y = 9
# Print out the types of x and y.
print(f"Types of x and y: {type(x)}, {type(y)}")
# print x+y
print(f"x + y = {x+y}")
# print x/y
print(f"x/y = {x/y}")
# print the type of x/y
print(f"Type of x/y: {type(x/y)}")
# print x*y
print(f"x*y = {x*y}")
# print the type of x*y
print(f"Type of x*y: {type(x*y)}")
# print x + 0.0
print(f"x + 0.0 = {x + 0.0}")
# print the type of x+0.0
print(f"Type of x + 0.0: {type(x+0.0)}")
# print x//y
print(f"x//y = {x//y}")
# print the type of x//y
print(f"Type of x//y: {type(x//y)}")
# write a comment explaining the difference between // and /.
print("// is the floor division operator - it divides and rounds down to the nearest integer, / is regular division.")
# print x<y
print(f"x < y: {x<y}")
# why is (x<y) == True?
print("Above is true because x (4) is less than y (9).")
# Notice that == and = are different, perform some experimentation or googling to discover the difference
# print out a string explaining the difference
print("== is a comparison operator, while = is an assignment operator.")
# print y%x
print(f"y%x = {y%x}")
# being confused by this one is ok. There'll be a deeper dive on this seperately.
# this is the Boolean Section
# a boolean is a variable that is either True or False
# notice that True and False are case sensative
print('Boolean Operations Section')
# make a variable t and a variable f, set them to True and False respectively
t = True
f = False
# print t and f 
# I did this one for you, you're welcome :)
# notice and is a special word, don't try to use it as a variable name :P
print(f'{t} and {f} is: {t and f}')
# print t or f
print(f'{t} or {f} is: {t or f}')
# print !t
print(f"!t is: {not t}")
# print !f
print(f'!f is: {not f}')
# This is the String Section
print('String Operations Section')
# make two variables, s and ten set them to 'This is a string.' and '10' respectively.
s = 'This is a string.'
ten = '10'
# print s + ten
print(s + ten)
# print s - ten
# print(s - ten) - invalid expression
# print ten + s
print(ten + s)
# print the type of ten
print(type(ten))
# print ten.isnumeric()
print(ten.isnumeric())
# print len(ten) and len(s)
print(f"{len(ten)} and {len(s)}")
# print a string explaining the results
# print s[:4]
print(s[:4])
# print s[:4]
print(s[:4])
# print s[0:4]
print(s[0:4])
# print s[2:]
print(s[2:])
# print s[-4:]
print(s[-4:])
# print s[0]
print(s[0])
# print a string that explains this [] thing...
print("[] when applied to a string accesses the string as an array of characters.")
# This is the Mixed Type Section
print('Mixed Type Section')
# print x*ten
print(x*ten)
# print 2 * s
print(2*s)
# print t*y
print(f'{t}*{y} is {t*y}')
# print f*y
print(f*y)
# print the first 5 letters of s six times
print(s[:5]*6)
# print s + y or explain the issue
print("s + y will not intuitively work because s is a string and y is an integer")
# print ten + y or explain the issue
print("ten + y will not intuitively work because ten is a string")
# force ten + y to work by turning both into strings
print(s + str(y))
# force ten + y to work by turning both into numbers
print(int(ten) + y)