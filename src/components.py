import random


class Component:
    def __init__(self, name: str, failure_rate: float, time_to_repair: float, repair_cost: float) -> None:
        """
        Initializes a Component with a name, failure rate, and repair time
        :param name (str): Name of component
        :param failure_rate: (float): (failures/time unit) higher value means that component is more likely to fail quickly
        :param time_to_repair (float): Average time it takes to repair component can be expressed in days, hours or minutes
        """
        self.name: str = name
        self.failure_rate: float = failure_rate
        self.repair_time: float = time_to_repair
        self.repair_cost = repair_cost

    def generate_failure_time(self) -> float:
        """
        Returns a time at which component will fail using exponential distribution
        :return: float: point in exponential distribution
        """
        return random.expovariate(self.failure_rate)

    def generate_repair_time(self):
        """
        Returns a time it will take to repair component based on exponential distribution
        :return: float: point in exponential distribution
        """
        return random.expovariate(1 / self.repair_time)


if __name__ == "__main__":
    component = Component(name="test_server", failure_rate=0.01, time_to_repair=10)
    failure_time = component.generate_failure_time()
    repair_time = component.generate_repair_time()

    print(f"failure time: {failure_time} \nrepair_time: {repair_time}")
