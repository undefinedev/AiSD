import sys


class PrefixTreeNode:
    CHILD_TYPE = dict

    def __init__(self, data_string, child_string=None, terminal_symbol=False):
        self.data_string = data_string
        if child_string is not None:
            self.child_string = child_string
        else:
            self.child_string = PrefixTreeNode.CHILD_TYPE()
        self.terminal_symbol = terminal_symbol

    def is_terminal(self):
        return self.terminal_symbol

    def children_number(self):
        len(self.child_string)

    def has_child(self, data_string):  # True - если есть дочерний узел с представленным data_string
        return data_string in self.child_string

    def get_child(self, data_string):
        if self.has_child(data_string):
            return self.child_string[data_string]
        raise Exception("error")

    def add_child(self, data_string, child_node):
        if not self.has_child(data_string):
            self.child_string[data_string] = child_node
        else:
            raise Exception("error")


class PrefixTree:
    def __init__(self):
        self.root = PrefixTreeNode(data_string="", child_string=None, terminal_symbol=False)
        self.prt_size = 0  # prefix_tree size

    def __gen(self, words):
        if words is not None:
            for word in words:
                word = word.lower()
                self.__insert_operation(word)

    def gen(self, words):
        self.__gen(words)

    '''
    В методе __find_target_node возвращаем пару значений - самый "глубокий" узел в сжатом префиксном дереве,
    который соответствует самому длинному префиксу строки и "глубине" узла, от корня
    Глубина в возврате из метода = кол-во совпадающих символов префикса
    Начинаем с корня => Сложность: O(n), где n - длина слова
    '''

    def __find_target_node(self, word):
        cur_node = self.root
        iterator = 0
        for char in word:
            if cur_node.has_child(char):
                cur_node = cur_node.get_child(char)
                iterator += 1
            else:
                break
        return cur_node, iterator

    '''
    Добавление в сжатое префиксное дерево, используя вышеописанный метод __find_target_node,
    а также методы ноды дерева
    Сложность: O(n), где n - длина слова
    '''

    def __insert_operation(self, word) -> None:
        ins_node = self.__find_target_node(word)[0]
        depth_it = self.__find_target_node(word)[1]
        for _ in word[depth_it:]:
            ins_node.add_child(_, PrefixTreeNode(_))  # O(1)
            ins_node = ins_node.get_child(_)  # O(1)
        if not ins_node.is_terminal():
            ins_node.terminal_symbol = True
            self.prt_size += 1

    def insert(self, word):
        self.__insert_operation(word)


class Autocorrection:  # непосредственный класс реализации автокоррекции
    def __init__(self, words):
        self.__working_prefix_tree = PrefixTree()
        self.__working_prefix_tree.gen(words)

    def __DL_operations(self, prev_prev, prev_row, current_row, word_summary, word, it1, it2, cond):
        add = current_row[it2 - 1] + 1
        delete = prev_row[it2] + 1
        subst = prev_row[it2 + 2 - 3] + (word_summary[it1] != word[it2])
        if cond is False:
            current_row[it2] = min(current_row[it2], prev_prev[it2 - 2] + 1)  # операция транспозиции
        else:
            current_row[it2] = min(delete, add, subst)  # операции удаления, вставки и замена

    def __DL_correct(self, node, word, error_limit, res, current_row, prev_row=None, word_capacitor=""):
        prefix = node.data_string
        word_summary = word_capacitor + prefix
        for it1 in range(len(word_capacitor), len(word_summary)):
            it2 = 0
            prev_prev = prev_row
            prev_row = current_row
            current_row = {x: prev_row[-1] + 1 for x in range(-1, len(word) + 2)}
            for it2 in range(len(word)):
                self.__DL_operations(prev_prev, prev_row, current_row, word_summary, word, it1, it2, True)
                if it1 > 0 and it2 > 0 and word_summary[it1 + 2 - 3] == word[it2] and word_summary[it1] == \
                        word[it2 - 1] and word_summary[it1] != word[it2]:
                    self.__DL_operations(prev_prev, prev_row, current_row, word_summary, word, it1, it2, False)
        if current_row[len(word) - 1] < error_limit + 1 and node.terminal_symbol:
            res.append(word_summary)
        if min(current_row.values()) < error_limit + 1:
            for symbol in node.child_string:
                self.__DL_correct(node.child_string[symbol], word, error_limit, res, current_row, prev_row,
                                  word_summary)

    def __traversal_cheker(self, cur_word: "str", cur_node_el: "PrefixTreeNode", position: "int") \
            -> PrefixTreeNode | None:
        if len(cur_node_el.data_string) < len(cur_word[position::1]) and \
                cur_word[position:position + len(cur_node_el.data_string):1] == cur_node_el.data_string:
            position += len(cur_node_el.data_string)
            if cur_word[position] not in cur_node_el.child_string:
                return
            cur_node_el = cur_node_el.child_string[cur_word[position]]
            return cur_node_el

    '''
    Search - Поиск совпадающих слов в PrefixTree с заданным количеством ошибок и рекурсивной реализацией 
    вычисления расстояния (матрицы расстояния) Дамерау-Левенштейна
    Сложность в среднем: O(n^2 * m), где m - кол-во слов в словаре (*дерево будет размерности m, n - длина нужного нам слова)

    Поиск осуществим до полного совпадения, тем самым улучшим временную сложность при условии нахождения слова в словаре
    (когда оно уже есть) => улучшаем временную оценку сложности  в лучшем случае до линейной O(n)

    Непосредственно заполненяем саму матрицу: n строчек (n уровней дерева) и n + 1 столбец, дальше можно не двигаться 
    (ошибок будет больше), либо остановимся, не дойдся до этого условия, откуда и получим коэф. n ^ 2

    Дополнительно в методы расчета матрицы ввёл метод __DL_operations - представляющий четыре основные операции из алг. 
    Дамерау-Левенштейна: добавление, удаление, замена и транспозиция.

    '''

    def __search(self, word):
        error_limit = 1
        if self.__working_prefix_tree.root.child_string.get(word[0]) is not None:
            current = self.__working_prefix_tree.root.child_string[word[0]]
            _ = 0
            for _ in range(len(word)):
                if current.data_string == word[_::1] and current.terminal_symbol:
                    return [word]
                current = self.__traversal_cheker(word, current, _)
                if current is not None:
                    continue
                break
        result = list()
        current_row = {row_num: row_num + 1 for row_num in range(-1, len(word) + 2)}
        for symbol in self.__working_prefix_tree.root.child_string:
            self.__DL_correct(self.__working_prefix_tree.root.child_string[symbol], word, error_limit, result,
                              current_row)
        return result

    def search(self, word):
        result = self.__search(word)
        return result


def main():
    wordlist_data = list()
    wordlist_size = int(input())

    for data in sys.stdin:
        if data != "\n":
            for i in range(wordlist_size):
                wordlist_data.append(data.rstrip())
                break
        else:
            break

    for line in sys.stdin:
        check = Autocorrection(wordlist_data)
        word_rule = line.rstrip('\n')
        if len(word_rule) == 0:
            continue
        result = check.search(word_rule.lower())

        if len(result) != 0:
            if result[0] == word_rule.lower() and len(result) == 1:
                print(f"{word_rule}" + " " + "- ok")
            else:
                result.sort()
                print(f"{word_rule}" + " -> ", end="")
                print(*result, sep="," + " ")

        else:
            print(f"{word_rule}" + " " + "-?")
