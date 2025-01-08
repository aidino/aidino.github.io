from collections import Counter
#URL: https://www.hackerrank.com/challenges/collections-counter/problem?isFullScreen=true

if __name__=="__main__":
    X = int(input()) # Number of shoes
    shoe_storage = list(map(int, input().split()))
    shoe_counter = Counter(shoe_storage)
    N = int(input()) # Number of customers
    money=0
    for _ in range(N):
        size, price = tuple(map(int, input().split()))
        if shoe_counter[size] > 0:
            money += price
            shoe_counter[size] -= 1
    print(money)
        