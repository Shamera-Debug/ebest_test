import sys # sys module 가져와라

args = sys.argv[1:] # 1부터 끝까지 슬라이싱 => [] list return
for arg in args:
    print(arg)