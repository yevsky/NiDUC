class SLA:
    def __init__(self, required_availability: float) -> None:
        self.required_availability: float = required_availability

    def check_compliance(self, actual_availability: float) -> bool:
        return actual_availability >= self.required_availability
