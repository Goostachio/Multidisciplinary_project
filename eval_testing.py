print("Test eval")
equation = 'x1+2*x2+x3'
def modify_value(x1,x2,x3):
    result = eval(equation)
    print(result)
    return result
a=5
modify_value(a,2,3)