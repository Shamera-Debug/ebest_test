import multiprocessing

def calc(a,b,c):
    return a * b + c

input_list = [(1,2,3),(4,5,6),(7,8,9),(10,11,12)]

# process pool : 프로세스를 먼저 생성
pool = multiprocessing.Pool(processes=4)

# 병렬 처리를 위한 map 메소드를 정의
output_list = pool.starmap(calc, input_list)

# 프로세스 풀 종료
pool.close()
pool.join() # 모든 프로세스가 종료될때까지 대기

print(output_list) 