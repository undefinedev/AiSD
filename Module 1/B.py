class deque:
    def __init__(self, size):
        self.__data = [None] * size
        self.__size = size
        self.__head = -1
        self.__tail = 0

    def pushf(self, num):
        if self.__head != self.__tail and self.__size > 0:
            if self.__head == -1:
                self.__head = 0
                self.__tail = 1
                self.__data[0] = num
            else:
                self.__head = (self.__head - 1) % self.__size
                self.__data[self.__head] = num
        else:
            print("overflow")

    def pushb(self, num):
        if self.__head != self.__tail and self.__size > 0:
            if self.__head == -1:
                self.__head = 0
                self.__tail = 1
                self.__data[0] = num
            else:
                self.__data[self.__tail] = num
                self.__tail = (self.__tail + 1) % self.__size
        else:
            print("overflow")

    def popf(self):
        if self.__head != -1:
            print(self.__data[self.__head])
            self.__head = (self.__head + 1) % self.__size
            if self.__head == self.__tail:
                self.__head = -1
                self.__tail = 0
        else:
            print("underflow")

    def popb(self):
        if self.__head != -1:
            self.__tail = (self.__tail - 1) % self.__size
            print(self.__data[self.__tail])
            if self.__head == self.__tail:
                self.__head = -1
                self.__tail = 0
        else:
            print("underflow")

    def print(self):
        if self.__head != -1:
            if self.__head < self.__tail:
                print(*self.__data[self.__head:self.__tail])
            else:
                print(*self.__data[self.__head:self.__size], end="")
                print("", *self.__data[0:self.__tail])
        else:
            print("empty")


if __name__ == "__main__":
    while True:
        try:
            size_in = input()
        except EOFError:
            exit()
        if len(size_in) == 0:
            continue
        if (size_in.__contains__("set_size ") and (size_in[9:].isdigit() or size_in[9:] == "-0")
                and " " not in size_in[9:]):
            deq = deque(int(size_in[9:]))
            break
        else:
            print("error")

    while True:
        try:
            command = input()
        except EOFError:
            break
        if len(command) == 0:
            continue
        match command:
            case "print" if len(command) == 5:
                deq.print()
            case "popf" if len(command) == 4:
                deq.popf()
            case "popb" if len(command) == 4:
                deq.popb()
            case command if command.__contains__("pushf ") and " " not in command[6:]:
                deq.pushf(command[6:])
            case command if command.__contains__("pushb ") and " " not in command[6:]:
                deq.pushb(command[6:])
            case _:
                print("error")
