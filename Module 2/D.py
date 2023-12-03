class RadixNode:
    def __init__(self, text, is_word=False, children=None):
        if children is None:
            children = {}
        self.text = text
        self.isWord = is_word
        self.children = children


class RadixTree:
    def __init__(self):
        self.root = RadixNode(text=None)

    '''
    Добавление слова в сжатое префиксное дерево
    Сложность: О(n), где n - длина слова
    '''

    def add(self, word):
        if word[0] not in self.root.children:
            self.root.children[word[0]] = RadixNode(word, is_word=True)
            return

        current = self.root.children[word[0]]
        i = 0
        while i < len(word):
            if word[i:].startswith(current.text):
                i += len(current.text)
                if i == len(word):
                    current.isWord = True
                    break
                if i < len(word) and word[i] not in current.children:
                    current.children[word[i]] = RadixNode(word[i:], is_word=True)
                    break
                current = current.children[word[i]]
            elif word[i:] in current.text:
                temp = current.text[len(word[i:]):]
                current.text = word[i:]
                current.children = {temp[0]: RadixNode(temp, is_word=current.isWord, children=current.children)}
                current.isWord = True
                return
            else:
                equal_index = 0
                for j in range(len(current.text)):
                    if current.text[j] != word[i + j]:
                        equal_index = j
                        break
                temp = current.text[equal_index:]
                current.text = current.text[:equal_index]
                current.children = {temp[0]: RadixNode(temp, is_word=current.isWord, children=current.children),
                                    word[i + equal_index]: RadixNode(word[i + equal_index:], is_word=True)}
                current.isWord = False
                return


class Correction:
    def __init__(self, words):
        self.__radix = RadixTree()
        for word in words:
            word = word.lower()
            self.__radix.add(word)

    '''
    Поиск похожих слов в сжатом префиксном дереве с задаваемым количеством ошибок
    и рекурсивной функцией для вычисления матрицы расстояния Дамерау-Левенштейна
    Сложность в среднем: O(n^2 * m), где n - длина искомого слова, m - число слов в словаре

    При заполнении матрицы мы доходим до состояния с n + 1 столбцами и n строками, 
    дальше нет смысла - больше ошибок, либо останавливаемся ещё раньше
    => n ^ 2
    
    UPD: обновил поиск: сначала выполняется обычный поиск полного совпадения, 
    что улучшает время работы для случаев, когда слово уже есть в словаре. В этом
    случае поиск занимает линейное время (сложность в лучшем случае О(n)).
    '''

    def search(self, word, error_limit=1):
        word = word.lower()
        if self.__radix.root.children.get(word[0]) is not None:
            current = self.__radix.root.children[word[0]]
            i = 0
            while i < len(word):
                if current.text == word[i:] and current.isWord:
                    return [word]
                if len(current.text) < len(word[i:]) and word[i:i + len(current.text)] == current.text:
                    i += len(current.text)
                    if word[i] not in current.children:
                        break
                    current = current.children[word[i]]
                    continue
                break
        res = []
        cur_row = {x: x + 1 for x in range(-1, len(word) + 1)}
        for symbol in self.__radix.root.children:
            self.__correction(self.__radix.root.children[symbol], word, error_limit, res, cur_row)
        return res

    def __correction(self, node, word, error_limit, res, cur_row, prev_row=None, word_capacitor=""):
        prefix = node.text
        word_sum = word_capacitor + prefix
        for x in range(len(word_capacitor), len(word_sum)):
            prev_prev_row = prev_row
            prev_row = cur_row
            cur_row = {x: prev_row[-1] + 1 for x in range(-1, len(word) + 1)}
            for y in range(len(word)):
                cur_row[y] = min(prev_row[y] + 1,  # delete
                                 cur_row[y - 1] + 1,  # add
                                 prev_row[y - 1] + (word_sum[x] != word[y]))  # substitution
                if x > 0 and y > 0 and word_sum[x - 1] == word[y] and word_sum[x] == word[y - 1] and word_sum[x] != \
                        word[y]:
                    cur_row[y] = min(cur_row[y], prev_prev_row[y - 2] + 1)  # transposition

        if cur_row[len(word) - 1] <= error_limit and node.isWord:
            res.append(word_sum)
        if min(cur_row.values()) <= error_limit:
            for symbol in node.children:
                self.__correction(node.children[symbol], word, error_limit, res, cur_row, prev_row, word_sum)


if __name__ == "__main__":
    wordlist = [str(input()) for i in range(int(input()))]
    checker = Correction(wordlist)

    while True:
        try:
            command = input()
        except EOFError:
            break
        if len(command) == 0:
            continue

        result = checker.search(command)
        if result:
            if result[0] == command.lower() and len(result) == 1:
                print(f"{command} - ok")
            else:
                result.sort()
                print(f"{command} -> ", end="")
                print(*result, sep=", ")
        else:
            print(f"{command} -?")

