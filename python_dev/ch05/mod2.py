PI = 3.141592

# class
class Math:
    def solv(self, r):
        return PI * (r**2)

# function
def sum(a,b):
    return a + b

if __name__ == '__main__': # True라는 것은 직접 실행
    print(PI)
    a = Math() # object create
    print(a.solv(2))
    print(sum(PI,4.4))