import math
import re


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class BinaryMinHeap:
    def __init__(self):
        self.__index = {}
        self.data = []

    def add(self, key, value):
        if self.__index.__contains__(key):
            raise IndexError
        self.__index.update({key: len(self.data)})
        self.data.append(Node(key, value))
        self.__heapify(len(self.data) - 1)

    def set(self, key, value):
        if not self.__index.__contains__(key):
            raise IndexError
        self.data[self.__index.get(key)].value = value

    def delete(self, key):
        index = self.__index.get(key)
        if index is None:
            raise IndexError
        self.__index[self.data[-1].key] = index
        self.data[index] = self.data[-1]
        self.__index.pop(key)
        self.data.pop()
        self.__heapify(index)

    def search(self, key):
        if not self.__index.__contains__(key):
            raise KeyError
        return self.data[self.__index.get(key)]

    def __heapify(self, current):
        if current >= len(self.data):
            return
        if self.data[int((current - 1) / 2)].key > self.data[current].key:
            swap = int((current - 1) / 2)
        else:
            node_left = current * 2 + 1
            node_right = current * 2 + 2
            swap = current
            if node_left < len(self.data) and self.data[node_left].key < self.data[swap].key:
                swap = node_left
            if node_right < len(self.data) and self.data[node_right].key < self.data[swap].key:
                swap = node_right
            if swap == current:
                return
        self.__index[self.data[current].key], self.__index[self.data[swap].key] = \
            self.__index[self.data[swap].key], self.__index[self.data[current].key]
        self.data[current], self.data[swap] = self.data[swap], self.data[current]
        return self.__heapify(swap)

    def max(self):
        if len(self.data) == 0:
            raise IndexError
        largest = 0
        for index in range(int(len(self.data)/2), len(self.data)):
            if self.data[index].key > self.data[largest].key:
                largest = index
        return self.data[largest]

    def min(self):
        if len(self.data) == 0:
            raise IndexError
        return self.data[0]

    def extract(self):
        if len(self.data) == 0:
            return IndexError
        root = self.data[0]
        self.delete(root.key)
        return root

    def get_index(self, key):
        return self.__index.get(key)


def print_heap(heap):
    if len(heap.data) == 0:
        return print("_")
    print_value = math.ceil(math.log2(len(heap.data) + 1))
    print(f"[{heap.data[0].key} {heap.data[0].value}]")
    for i in range(1, len(heap.data)):
        if math.log2(i+2) % 1 == 0:
            print(f"[{heap.data[i].key} {heap.data[i].value} {heap.data[int((i - 1) / 2)].key}]")
        else:
            print(f"[{heap.data[i].key} {heap.data[i].value} {heap.data[int((i - 1) / 2)].key}]", end=" ")
    if 2 ** print_value - len(heap.data) - 1 != 0:
        print(*["_"] * (2 ** print_value - len(heap.data) - 1))


if __name__ == "__main__":
    Heap = BinaryMinHeap()
    while True:
        try:
            command = input()
        except EOFError:
            break
        if len(command) == 0:
            continue
        try:
            match command:
                case "min":
                    nod = Heap.min()
                    print(f"{nod.key} 0 {nod.value}")
                case "max":
                    nod = Heap.max()
                    print(f"{nod.key} {Heap.get_index(nod.key)} {nod.value}")
                case "extract":
                    nod = Heap.extract()
                    print(f"{nod.key} {nod.value}")
                case "print":
                    print_heap(Heap)
                case command if re.fullmatch(r"^(add )-?\d+\s[^ ]*$", command):
                    Heap.add(int(command.split()[1]), re.search(r"\s\S*\s(.*)", command).group(1))
                case command if re.fullmatch(r"^(set )-?\d+\s[^ ]*$", command):
                    Heap.set(int(command.split()[1]), re.search(r"\s\S*\s(.*)", command).group(1))
                case command if re.fullmatch(r"^(search )-?\d+$", command):
                    try:
                        nod = Heap.search(int(command.split()[1]))
                        print("1", Heap.get_index(nod.key), nod.value)
                    except KeyError:
                        print("0")
                case command if re.fullmatch(r"^(delete )-?\d+$", command):
                    Heap.delete(int(command.split()[1]))
                case _:
                    print("error")
        except IndexError:
            print("error")
