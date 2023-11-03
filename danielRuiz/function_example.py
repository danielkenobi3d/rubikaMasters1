
def add_two_values(value_a, value_b):
    result = value_a + value_b
    return result
rslt = add_two_values(20, 67)

print(rslt)

def add_multiple_values(*args):
    result = 0
    print(type(args))
    print(args)
    for each in args:
        result = result + each
    return result

print(add_multiple_values(2,43,45, 7))

adding_numbers = list(range(20))
print(add_multiple_values(*adding_numbers))
