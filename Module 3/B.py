import math
import re


class BitArray:
    def __init__(self, size=0):
        self.size = size
        self.array = 0

    def set(self, i):
        if i < 0 or i >= self.size:
            raise MemoryError
        self.array |= (1 << i)

    def reset(self, i):
        if i < 0 or i >= self.size:
            raise MemoryError
        self.array &= ~(1 << i)

    def get(self, i):
        if i < 0 or i >= self.size:
            raise MemoryError
        return self.array & (1 << i) != 0


class BloomFilter:
    def __init__(self, n, p):
        if n <= 0 or p <= 0 or p >= 1:
            raise ValueError
        self.__size = n
        self.__p = p
        bit_array_size = round(-n * math.log2(p) / math.log(2))
        self.hash_num = round(-math.log2(p))
        if bit_array_size == 0 or self.hash_num == 0:
            raise ValueError
        self.bitarray = BitArray(bit_array_size)
        self.__mersenne = 2 ** 31 - 1
        temp = 6 if self.hash_num < 6 else self.hash_num  # из-за высокой плотности простых чисел в самом начале
        self.__primes = list(
            self.__eratosthenes(round(temp * math.log(temp) + temp * (math.log(math.log(temp)) - 0.25))))
        '''
        Функция аппроксимации была взята почти готовой и доработана собственным коэффициентом, который даёт очень малую
        погрешность в оценке сверху на малом количестве простых чисел. Статистика приведена далее:
        hash_num    len(__primes)   error
        10          10              0%
        25          27              8%
        50          54              8%
        75          80              6,7%
        100         107             7%
        500         539             7,8%
        1000        1069            6,9%

        Можно было бы даже сделать переменный коэффициент в зависимости от кол-ва хеш-функций. 
        Многократным тестированием установил, что от 100 уже можно использовать коэффициент 0.7, что уменьшает процент
        на больших числах. На очень больших числах (от 10000 простых чисел) этот коэффициент стремится к 0.94-0.95.

        Скорость работы увеличивается в разы. Проверял на повторяющемся цикле, вычисляющем от 2 до 1000 простых чисел
        для функции с перебором по уже известным простым числам и решета эратосфена. Разница такова:
        Time in seconds: 0.4885437488555908    решето
        Time in seconds: 1.9636526107788086    перебор

        Аппроксимационная функция взята с Wiki: 
        https://en.wikipedia.org/wiki/Prime_number_theorem#Approximations_for_the_nth_prime_number
        Улучшенное решето Эратосфена:
        https://rosettacode.org/wiki/Sieve_of_Eratosthenes#Using_set_lookup
        '''

    def add(self, key):
        if key < 0:
            raise ValueError
        for i in range(self.hash_num):
            ind = self.__hash(key, i)
            self.bitarray.set(ind)

    def __eratosthenes(self, n):
        multiples = set()
        for i in range(2, n + 1):
            if i not in multiples:
                yield i
                multiples.update(range(i * i, n + 1, i))

    def __hash(self, key, i):
        return ((i + 1) * key + self.__primes[i]) % self.__mersenne % self.bitarray.size

    def search(self, key):
        if key < 0:
            raise ValueError
        for i in range(self.hash_num):
            ind = self.__hash(key, i)
            if not self.bitarray.get(ind):
                return False

        return True


def print_bit_array_bloom(bloom):
    print(bin(bloom.bitarray.array)[:1:-1].ljust(bloom.bitarray.size, '0'))


if __name__ == "__main__":
    while True:
        try:
            command = input()
        except EOFError:
            break
        if len(command) == 0:
            continue
        try:
            if re.fullmatch(r'^(set )\d+\s(0.)\d+$', command):
                Bloom = BloomFilter(int(command.split()[1]), float(command.split()[2]))
                print(Bloom.bitarray.size, Bloom.hash_num)
                break
            else:
                print("error")
        except ValueError:
            print("error")

    while True:
        try:
            command = input()
        except EOFError:
            break
        if len(command) == 0:
            continue
        try:
            match command:
                case "print":
                    print_bit_array_bloom(Bloom)
                case command if re.fullmatch(r'^(add )\d+$', command):
                    Bloom.add(int(command.split()[1]))
                case command if re.fullmatch(r'^(search )\d+$', command):
                    print("1" if Bloom.search(int(command.split()[1])) else "0")
                case _:
                    print("error")
        except ValueError or MemoryError:
            print("error")
