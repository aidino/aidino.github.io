n = int(input())
s = set(map(int, input().split()))
N = int(input())
for _ in range(N):
    cmd = input().strip().split()
    match cmd:
        case ["pop"]:
            s.pop() 
        case ["remove", num]:
            s.remove(int(num))
        case ["discard", num]:
            s.discard(int(num))
        case _:
            print("Invalid command")

print(sum(s))