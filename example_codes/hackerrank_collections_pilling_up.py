# Enter your code here. Read input from STDIN. Print output to STDOUT
from collections import deque

for _ in range(int(input())):
    n = int(input())
    cubes = deque(map(int, input().split()))
    last_cube = -1
    left = 0
    right = -1
    for _ in range(n):
        if last_cube == -1:
            if cubes[left] > cubes[right]:
                last_cube = cubes.popleft()
            else:
                last_cube = cubes.pop()
        else:
            if cubes[left] <= last_cube and cubes[right] <= last_cube:
                if cubes[left]<=cubes[right]:
                    last_cube=cubes.pop()
                else:
                    last_cube=cubes.popleft()
            else:
                break
    print("Yes" if len(cubes)==0 else "No")
                
                
    
            