import unittest
import logging
import sys

# Настройка логирования
logging.basicConfig(
    level=logging.WARNING,
    filename='runner_tests.log',
    filemode='w',
    encoding='UTF-8',
    format='%(asctime)s,%(msecs)03d | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class Runner:
    def __init__(self, name, speed=5):
        if isinstance(name, str):
            self.name = name
        else:
            raise TypeError(f'Имя может быть только числом, передано {type(name).__name__}')
        self.distance = 0
        if speed > 0:
            self.speed = speed
        else:
            raise ValueError(f'Скорость не может быть отрицательной, сейчас {speed}')

    def run(self):
        self.distance += self.speed * 2

    def walk(self):
        self.distance += self.speed

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        elif isinstance(other, Runner):
            return self.name == other.name


class Tournament:
    def __init__(self, distance, *participants):
        self.full_distance = distance
        self.participants = list(participants)

    def start(self):
        finishers = {}
        place = 1
        while self.participants:
            for participant in self.participants:
                participant.run()
                if participant.distance >= self.full_distance:
                    finishers[place] = participant
                    place += 1
                    self.participants.remove(participant)

        return finishers

class RunnerTest(unittest.TestCase):

# Обработка исключения ValueError с логированием на уровне WARNING, включающее тип исключения и его сообщение
    def test_walk(self):
        try:
            runner = Runner('Вася', -5)
            runner.walk()
            self.fail("Ожидалось исключение ValueError") # вызов, если исключение не возникло
        except ValueError as e:
            logging.warning(f"Неверная скорость для Runner\n{type(e).__name__}: {e}")

# обработка исключения TypeError с логированием на уровне WARNING, включающее тип исключения и его сообщение
    def test_run(self):
        try:
            runner = Runner(2)
            runner.run()
            self.fail("Ожидалось исключение TypeError") # вызов, если исключение не возникло
        except TypeError as e:
            logging.warning(f"Неверный тип данных для объекта Runner\n{type(e).__name__}: {e}")

# Дополнительный тест, для проверки корректного создания объекта.
    def test_valid_runner(self):
        runner = Runner("Вaся", 10)
        self.assertEqual(runner.name, "Вaся")
        self.assertEqual(runner.speed, 10)

if __name__ == '__main__':
    unittest.main()

# Вывод логов в консоль
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.WARNING)
logging.getLogger().addHandler(console_handler)

first = Runner('Вaся', 10)
second = Runner('Илья', 5)
third = Runner('Арсен', 10)

t = Tournament(101, first, second, third)
print(t.start())