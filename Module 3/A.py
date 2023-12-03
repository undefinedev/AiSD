class Fail2Ban:
    def __init__(self, attempts, interval, block_min, block_max, time):
        self.__attempts = attempts
        self.__interval = interval
        self.__block_min = block_min
        self.__block_max = block_max
        self.__timestamp = time
        self.__login_fail = []

    def log_attempt(self, time):
        if time >= self.__timestamp - 2 * self.__block_max:
            self.__login_fail.append(time)

    '''
    Алгоритм проходится по массиву за O(n) и сортирует его за O(n * log(n)).
    Поэтому асимптотическая сложность: O(n * log(n)).
    
    Сложность по памяти будет O(n), потому что в реализации sort в python используется
    Timsort, у которого худшая сложность по памяти O(n).
    '''
    def block_time(self):
        self.__login_fail.sort()
        count = 0
        block_start = 0
        block_interval = self.__block_min
        while count + self.__attempts <= len(self.__login_fail):
            if self.__interval >= self.__login_fail[count + self.__attempts - 1] - self.__login_fail[count]:
                if block_start > 0:
                    block_interval = block_interval * 2 if block_interval * 2 <= self.__block_max else self.__block_max
                block_start = self.__login_fail[count + self.__attempts - 1]
                count += self.__attempts - 1
            count += 1

        if not block_start or block_start + block_interval < self.__timestamp:
            return None
        return block_start + block_interval


if __name__ == "__main__":
    try:
        command = input().split()
        if len(command) != 5:
            raise TypeError
        log_in = Fail2Ban(int(command[0]), int(command[1]), int(command[2]), int(command[3]), int(command[4]))

        while True:
            try:
                command = int(input())
            except EOFError:
                break
            except ValueError:
                continue
            log_in.log_attempt(command)

        unblock = log_in.block_time()
        if unblock:
            print(unblock)
        else:
            print("ok")
    except TypeError:
        pass
