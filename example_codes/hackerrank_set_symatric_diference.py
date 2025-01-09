# Enter your code here. Read input from STDIN. Print output to STDOUT

if __name__=="__main__":
    m = int(input())
    set_m = set(map(int, input().split()))
    n = int(input())
    set_n = set(map(int, input().split()))
    m_diff_n = set_m.difference(set_n)
    n_diff_m = set_n.difference(set_m)
    result_set = m_diff_n.union(n_diff_m)
    result_arr = sorted(result_set)
    print(*result_arr, sep="\n")