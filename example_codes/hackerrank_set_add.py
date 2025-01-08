if __name__=="__main__":
    n = int(input())
    stamps = {input() for _ in range(n)}
    print(len(stamps))
    