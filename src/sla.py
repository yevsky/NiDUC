class SLA:
    def __init__(self, sla_level_name: str, thresholds: dict[str, float]) -> None:
        """
        Creates an SLA level which meets specified threshold
        :param sla_level_name: (str): gives a name for SLA level
        :param thresholds: (Dict[str, float]): dictionary of thresholds for SLA level e.g.: (availability, max downtime...)
        """
        self.sla_level = sla_level_name
        self.thresholds = thresholds

    def is_sla_compliant(self, average_availability: float, total_breaks: int, max_break_time: float) -> bool:
        """
        Checks if system met the SLA compliance based on multiple metrics.
        :param average_availability: average availability of the system
        :param total_breaks: total number of breaks in the simulation
        :param max_break_time: the longest single downtime duration
        :return: bool indicating SLA compliance
        """
        # Check availability
        if 'availability' in self.thresholds and average_availability < self.thresholds['availability']:
            return False

        # Check maximum allowed breaks
        if 'max_breaks' in self.thresholds and total_breaks > self.thresholds['max_breaks']:
            return False

        # Check maximum break time
        if 'max_break_time' in self.thresholds and max_break_time > self.thresholds['max_break_time']:
            return False

        return True
