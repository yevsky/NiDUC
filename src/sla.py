class SLA:
    def __init__(self, sla_level_name: str, thresholds: dict[str, float]) -> None:
        """
        Creates an SLA level which meets specified threshold
        :param sla_level_name: (str): gives a name for SLA level
        :param thresholds: (Dict[str, float]): dictionary of thresholds for SLA level e.g.: (availability, max downtime...)
        """
        self.sla_level = sla_level_name
        self.thresholds = thresholds

    def is_sla_compliant(self, average_availability: float, total_breaks: int, max_break_time: float,
                         average_repair_time: float, annual_maintenance_cost: float) -> bool:
        """
        Checks if system met the SLA compliance based on multiple metrics.
        :param average_availability: average availability of the system
        :param total_breaks: total number of breaks in the simulation
        :param max_break_time: the longest single downtime duration
        :param average_repair_time: average time it took to fix a component
        :param annual_maintenance_cost: cost for maintaining system per year
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

        # Check average repair time
        if 'average_repair_time' in self.thresholds and average_repair_time > self.thresholds['average_repair_time']:
            return False

        # Check cost per year
        if 'max_cost_per_year' in self.thresholds and annual_maintenance_cost > self.thresholds['max_cost_per_year']:
            return False

        return True
