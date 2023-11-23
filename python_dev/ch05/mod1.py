def sum(a,b):
    return a + b

def safe_sum(a,b):
    if type(a) != type(b):
        print('타입 틀리다. 연산할수 없다.')
        return
    else:
        return sum(a,b)

if __name__ == '__main__':
    # function test code
    print(sum(1,1))
    print(safe_sum('a',1))
    print(sum(10,10.4))