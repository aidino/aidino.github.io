from collections import Counter

n, m = tuple(map(int, input().split()))
arr_counter = Counter(map(int, input().split()))
like_set = set(map(int, input().split()))
dislike_set = set(map(int, input().split()))

happiness=0
for num, ctn in arr_counter.items():
    if num in like_set:
        happiness += ctn
    if num in dislike_set:
        happiness -= ctn

print(happiness)
