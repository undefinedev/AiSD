class Item:
    def __init__(self, weight, cost):
        self.weight = weight
        self.cost = cost


class Knapsack:
    def __init__(self, capacity, approx):
        self.capacity = capacity
        self.approx = approx
        self.weight = 0
        self.cost = 0

    def optimize(self, items):
        coefficient = self.approx * max(items, key=lambda item: item.cost).cost / len(items)
        valuable = {0: ([], 0, 0)}
        for index in range(len(items)):
            for valuable_cost in list(valuable.values()):
                weight, cost = (items[index].weight + valuable_cost[1],
                                int(items[index].cost / coefficient) + valuable_cost[2])
                if weight <= self.capacity and (cost not in valuable.keys() or weight < valuable[cost][1]):
                    valuable[cost] = (valuable_cost[0] + [index], weight, cost)

        most_valuable = valuable[max(valuable.keys())]
        self.weight = most_valuable[1]
        self.cost = sum(items[i].cost for i in most_valuable[0])
        return most_valuable[0]


if __name__ == "__main__":
    try:
        approximation = float(input())
        capacity_max = int(input())
    except ValueError:
        exit()

    items_all = []

    while True:
        try:
            command = input().split()
        except EOFError:
            break
        if len(command) == 0:
            continue

        try:
            items_all.append(Item(int(command[0]), int(command[1])))
        except ValueError:
            exit()

    rykzack = Knapsack(capacity_max, approximation)
    indexes = rykzack.optimize(items_all)
    print(rykzack.weight, rykzack.cost)
    for item_ind in indexes:
        print(item_ind + 1)
