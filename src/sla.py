class SLA:
    def __init__(self, sla_level_name: str, thresholds: dict[str, float]) -> None:
        """
        Creates an SLA level which meets specified threshold
        :param sla_level_name: (str): gives a name for SLA level
        :param thresholds: (Dict[str, float]): dictionary of thresholds for SLA level e.g.: (availability, max downtime...)
        """
        self.sla_level = sla_level_name
        self.thresholds = thresholds
        self.availability = 0
        self.downtime = 0

    def calculate_availability(self, uptime: float, total_time: float) -> float:
        """
        Calculates availability based on uptime of the system
        :param uptime: (float): time that system was working for
        :param total_time: (float): time that system worked in total
        """
        self.availability = uptime / total_time
        return self.availability

    def is_sla_compliant(self) -> bool:
        """
        Checks if system met the SLA compliance
        :return: (bool): return true if system has met SLA
        """
        return self.availability >= self.thresholds['availability']
