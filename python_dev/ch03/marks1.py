# marks1.py

marks = [90,25,67,45,80] # list 생성
number = 0

for mark in marks:
    number += 1
    if mark >= 60:
        print(f'{number}번 학생은 합격')
    else:
        print(f'{number}번 학생은 불합격')