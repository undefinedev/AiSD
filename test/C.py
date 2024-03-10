import sys

if len(sys.argv) == 3:
    input_f = sys.argv[1]
    output_f = sys.argv[2]
else:
    sys.exit()

numbers = []
with open(input_f) as file:
    for line in file.readlines():
        if line.lstrip('-').rstrip('\n').isdigit():
            numbers.append(int(line))

with open(output_f, 'w') as file:
    file.write((sum(numbers) % 256).__str__())

