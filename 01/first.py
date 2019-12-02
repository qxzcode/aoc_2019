import sys # argv


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        print(sum(int(line)//3 - 2 for line in f.readlines()))
