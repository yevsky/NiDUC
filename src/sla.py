class SLA:
    def __init__(self, sla_level_name: str, thresholds: dict[str, float]) -> None:
        """
        Creates an SLA level which meets specified threshold
        :param sla_level_name: (str): gives a name for SLA level
        :param thresholds: (Dict[str, float]): dictionary of thresholds for SLA level e.g.: (availability, max downtime...)
        """
        self.sla_level = sla_level_name
        self.thresholds = thresholds

    def is_sla_compliant(self, average_availability: float) -> bool:
        """
        Checks if system met the SLA compliance
        :param average_availability: average availability of a system
        :return: (bool): return true if system has met SLA
        """
        return average_availability >= self.thresholds['availability']
