import random


class Component:
    def __init__(self, name: str, failure_rate: float, repair_time: float) -> None:
        """
        Initializes a Component with a name, failure rate, and repair time
        """
        self.name: str = name
        self.failure_rate: float = failure_rate
        self.repair_time: float = repair_time
        self.is_operational: bool = True
        self.time_until_failure: float = self.generate_time_until_failure()
        self.time_until_repair_complete: Optional[float] = None

    def generate_time_until_failure(self) -> float:
        # Time until failure follows an exponential distribution
        return random.expovariate(self.failure_rate) if self.failure_rate > 0 else float("inf")

    def fail(self) -> None:
        self.is_operational = False
        self.time_until_repair_complete = self.repair_time

    def repair(self) -> None:
        self.is_operational = True
        self.time_until_failure = self.generate_time_until_failure()
        self.time_until_repair_complete = None

    def update(self, delta_time: float) -> None:
        if self.is_operational:
            self.time_until_failure -= delta_time
            if self.time_until_failure <= 0:
                self.fail()
        else:
            if self.time_until_repair_complete is not None:
                self.time_until_repair_complete -= delta_time
                if self.time_until_repair_complete <= 0:
                    self.repair()
