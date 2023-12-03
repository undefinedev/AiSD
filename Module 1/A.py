import sys

nums = 0
try:
    for line in sys.stdin.read().splitlines():
        num = ''
        for symbol in line:
            if symbol.isdigit() or symbol == '-' and num == '':
                num += symbol
            elif symbol != '-' and num == '-':
                num = ''
            elif num != "" and num != "-":
                nums += int(num)
                num = '-' if symbol == '-' else ''
        if num != "" and num != "-":
            nums += int(num)
except EOFError:
    pass
print(nums)
