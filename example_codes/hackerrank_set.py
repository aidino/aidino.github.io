
def average(array):
    # your code goes here
    arr_set = set(arr)
    return round(sum(arr_set)/len(arr_set), 3)

if __name__ == '__main__':
    n = int(input())
    arr = list(map(int, input().split()))
    result = average(arr)
    print(result)