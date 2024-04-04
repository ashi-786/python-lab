x1 = int(input("Enter 1st number: "))
x2 = int(input("Enter 2nd number: "))
op = input("Enter an arithmetic operator (+, -, *, /, //, %, **): ")

# using if-else:
# if op == '+':
#     print(f'{x1} + {x2} = {x1+x2}')
# elif op == '-':
#     print(f'{x1} - {x2} = {x1-x2}')
# elif op == '*':
#     print(f'{x1} * {x2} = {x1*x2}')
# elif op == '/':
#     print("%3d / %2d = %1.2f" % (x1, x2, x1/x2))
# elif op == '//':
#     print(f'{x1} // {x2} = {x1//x2}')
# elif op == '%':
#     print(f'{x1} % {x2} = {x1%x2}')
# elif op == '**':
#     print(f'{x1} ** {x2} = {x1**x2}')
# else:
#     print("Invalid operator!")

# using match-case:
match op:
    case "+":
        print(f'{x1} + {x2} = {x1+x2}')
    case "-":
        print(f'{x1} - {x2} = {x1-x2}')
    case "*":
        print(f'{x1} * {x2} = {x1*x2}')
    case "/":
        print("%3d / %2d = %1.2f" % (x1, x2, x1/x2))
    case "//":
        print(f'{x1} // {x2} = {x1//x2}')
    case "%":
        print(f'{x1} % {x2} = {x1%x2}')
    case "**":
        print(f'{x1} ** {x2} = {x1**x2}')
    case _:
        print("Invalid operator!")