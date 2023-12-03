import re


class Node:
    def __init__(self, key, value, parent=None, left=None, right=None):
        self.key = key
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent


class SplayTree:
    def __init__(self):
        self.root = None

    def add(self, key, value):
        if not self.root:
            self.root = Node(key, value)
            return
        node, node_next = self.__find(key)
        if node_next:
            self.__splay(node)
            raise IndexError
        if key < node.key:
            node.left = Node(key, value, node)
            self.__splay(node.left)
        else:
            node.right = Node(key, value, node)
            self.__splay(node.right)

    def set(self, key, value):
        if not self.root:
            raise IndexError
        node, node_next = self.__find(key)
        self.__splay(node)
        if not node_next:
            raise IndexError
        self.root.value = value

    def delete(self, key):
        if not self.root:
            raise IndexError
        node, node_next = self.__find(key)
        self.__splay(node)
        if not node_next:
            raise IndexError
        node_l = self.root.left
        node_r = self.root.right
        del self.root
        if node_l:
            node_l.parent = None
        if node_r:
            node_r.parent = None
        if not node_l:
            self.root = node_r
        elif not node_r:
            self.root = node_l
        else:
            self.root = node_l
            node = node_l
            while node.right:
                node = node.right
            self.__splay(node)
            node_r.parent = self.root
            self.root.right = node_r

    def search(self, key):
        if not self.root:
            raise KeyError
        node, node_next = self.__find(key)
        self.__splay(node)
        if not node_next:
            raise KeyError
        return self.root

    def __find(self, key):
        node = self.root
        node_next = self.root
        while node_next:
            node = node_next
            if key < node.key:
                node_next = node_next.left
            elif key > node.key:
                node_next = node_next.right
            else:
                break
        return node, node_next

    def min(self):
        if self.root is None:
            raise IndexError
        node = self.root
        while node.left:
            node = node.left
        self.__splay(node)
        return node

    def max(self):
        if self.root is None:
            raise IndexError
        node = self.root
        while node.right:
            node = node.right
        self.__splay(node)
        return node

    def __splay(self, node):
        while node.parent:
            parent = node.parent
            if not parent.parent:
                self.__zig(node)
            elif (parent.left == node and parent.parent.left == parent or
                  parent.right == node and parent.parent.right == parent):
                self.__zig(parent)
                self.__zig(node)
            else:
                self.__zig(node)
                self.__zig(node)
        self.root = node

    def __zig(self, node):
        parent = node.parent
        if parent.parent:
            if parent.parent.left == parent:
                parent.parent.left = node
            else:
                parent.parent.right = node

        node.parent = parent.parent
        parent.parent = node
        if parent.left == node:
            parent.left = node.right
            if node.right:
                node.right.parent = parent
            node.right = parent
        else:
            parent.right = node.left
            if node.left:
                node.left.parent = parent
            node.left = parent


def printsplaytree(tree):            # переписал, чтобы ускорить время работы программы
    if not tree.root:
        print("_")
        return

    print(f"[{tree.root.key} {tree.root.value}]")
    level = {}
    level_next = {}
    if tree.root.left:
        level[0] = tree.root.left
    if tree.root.right:
        level[1] = tree.root.right

    iteration = 0
    while level:
        expected_num = 0
        for num in level:
            node = level[num]
            if num != expected_num:
                print("_ " * (num - expected_num), end="")
            if num != (2 << iteration) - 1:
                print(f"[{node.key} {node.value} {node.parent.key}]", end=" ")
            else:
                print(f"[{node.key} {node.value} {node.parent.key}]")

            expected_num = num + 1
            if node.left:
                level_next[num * 2] = node.left
            if node.right:
                level_next[num * 2 + 1] = node.right

        if expected_num < 2 << iteration:
            print("_ " * ((2 << iteration) - expected_num - 1), end="_\n")
        level = level_next
        level_next = {}
        iteration += 1


if __name__ == "__main__":
    Tree = SplayTree()
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
                    nod = Tree.min()
                    print(nod.key, nod.value)
                case "max":
                    nod = Tree.max()
                    print(nod.key, nod.value)
                case "print":
                    printsplaytree(Tree)
                case command if re.fullmatch(r"^(add )-?\d+\s[^ ]*$", command):
                    Tree.add(int(command.split()[1]), re.search(r"\s\S*\s(.*)", command).group(1))
                case command if re.fullmatch(r"^(set )-?\d+\s[^ ]*$", command):
                    Tree.set(int(command.split()[1]), re.search(r"\s\S*\s(.*)", command).group(1))
                case command if re.fullmatch(r"^(search )-?\d+$", command):
                    try:
                        nod = Tree.search(int(command.split()[1]))
                        print("1", nod.value)
                    except KeyError:
                        print("0")
                case command if re.fullmatch(r"^(delete )-?\d+$", command):
                    Tree.delete(int(command.split()[1]))
                case _:
                    print("error")
        except IndexError:
            print("error")
