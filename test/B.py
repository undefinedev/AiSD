import sys

nums = []
try:
    for line in sys.stdin.read().splitlines():
        num = ''
        for symbol in line:
            if symbol.isdigit() or symbol == '-' and num == '':
                num += symbol
            elif symbol != '-' and num == '-':
                num = ''
            elif num.lstrip('-').isdigit():
                nums.append(int(num))
                num = '-' if symbol == '-' else ''
        if num.lstrip('-').isdigit():
            nums.append(int(num))
except EOFError:
    pass
print(sum(nums))
