import sys # argv


def get_required_fuel(mass):
    total_fuel = 0
    while True:
        fuel = mass//3 - 2
        if fuel <= 0:
            break
        total_fuel += fuel
        mass = fuel
    return total_fuel

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        print(sum(get_required_fuel(int(line)) for line in f.readlines()))
