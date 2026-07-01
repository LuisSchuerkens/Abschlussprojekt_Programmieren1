import battery_pack


class BatterySimulator:
    """
    Simuliert einen Akku über ein Leistungsprofil.
    """

    def __init__(self, battery: battery_pack.BatteryPack) -> None:
        self.battery = battery
        self.soc_profile = []
        self.voltage_profile = []
        self.current_profile = []

    def simulate(self, current_profile: list[float], duration_profile: list[float]) -> None:
        """
        Simuliert den Akku mit einem direkt vorgegebenen Stromprofil.
        """
        if len(current_profile) != len(duration_profile):
            raise ValueError("Current profile and duration profile must have the same length.")

        self.soc_profile = []
        self.voltage_profile = []
        self.current_profile = []

        for current, duration in zip(current_profile, duration_profile):
            self.battery.apply_current(current, duration)

            self.current_profile.append(current)
            self.soc_profile.append(self.battery.soc)
            self.voltage_profile.append(self.battery.voltage(current))

    def simulate_power(self, power_profile: list[float], duration_profile: list[float]) -> None:
        """
        Simuliert den Akku mit einem Leistungsprofil.

        Der Akku-Strom wird aus Leistung und aktueller Akkuspannung berechnet:
        current = power / voltage
        """
        if len(power_profile) != len(duration_profile):
            raise ValueError("Power profile and duration profile must have the same length.")

        self.soc_profile = []
        self.voltage_profile = []
        self.current_profile = []

        for power, duration in zip(power_profile, duration_profile):
            voltage = self.battery.open_circuit_voltage()

            if voltage > 0:
                current = power / voltage
            else:
                current = 0.0

            self.battery.apply_current(current, duration)

            self.current_profile.append(current)
            self.soc_profile.append(self.battery.soc)
            self.voltage_profile.append(self.battery.voltage(current))