import os

path = os.path.join(os.path.dirname('input.txt'))


def get_monkey_decisions(path_to_file):
    with open(path_to_file) as file:
        monkeys = [monkey.split("\n")
                   for monkey in file.read().strip().split("\n\n")]
    decisions = []
    for monkey in monkeys:
        decisions.append([])
        decisions[-1].append([int(x)
                             for x in monkey[1].strip("Starting items:").split(", ")])
        decisions[-1].append(eval("lambda old: o" +
                             monkey[2].strip("Operation: w =")))
        decisions[-1].append(int(monkey[3].strip("Test: divisable by")))
        decisions[-1].append(int(monkey[4].strip("If true: throw to monkey")))
        decisions[-1].append(int(monkey[5].strip("If false: throw to monkey")))
    return decisions


def one_round(monkeys, part):
    modulo = 1
    for monkey in monkeys:
        modulo *= monkey[2]
    counters = []
    for monkey in monkeys:
        counters.append(len(monkey[0]))
        while len(monkey[0]):
            inspected_item = monkey[0].pop()
            inspected_item = (monkey[1](inspected_item) %
                              modulo) // (5-2*part)  # // 3 for part == 1
            if inspected_item % monkey[2] == 0:
                monkeys[monkey[3]][0].append(inspected_item)
            else:
                monkeys[monkey[4]][0].append(inspected_item)
    return counters


def monkey_business(monkeys, n, part):
    overall_activity = []
    for i in range(len(monkeys)):
        overall_activity.append(0)
    for i in range(n):
        activity = one_round(monkeys, part)
        for i in range(len(overall_activity)):
            overall_activity[i] += activity[i]
    return max(overall_activity) * max([x for x in overall_activity if x != max(overall_activity)])


if __name__ == "__main__":
    monkeys = get_monkey_decisions(
        '/home/hagay/Development/advent-of-code/advent-of-code-2022/day-11/input.txt')
    print(monkey_business(monkeys, 20, 1))  # Part One
    monkeys = get_monkey_decisions(
        '/home/hagay/Development/advent-of-code/advent-of-code-2022/day-11/input.txt')
    print(monkey_business(monkeys, 10000, 2))  # Part Two
