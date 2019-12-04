import sys # argv


def is_valid(num):
    digits = [int(d) for d in str(num)]
    adjacent_digits = list(zip(digits[:-1], digits[1:]))
    
    # digits must never decrease
    if not all(d1 <= d2 for d1, d2 in adjacent_digits):
        return False
    
    # there must be a double digit
    if not any(d1 == d2 for d1, d2 in adjacent_digits):
        return False
    
    return True

min_num, max_num = [int(n) for n in sys.argv[1].split('-')]
valid_count = 0
for num in range(min_num, max_num+1):
    if is_valid(num):
        valid_count += 1
print(valid_count)
