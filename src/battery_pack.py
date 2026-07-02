import logging

import numpy as np

class BatteryPack:
    def __init__(
        self,
        capacity_nom_Ah: float,
        internal_resistance_mOhm: float = 80,
        initial_soc: float = 1.0,
        soc_points=None,
        voltage_points=None,
    ):
        if capacity_nom_Ah <= 0:
            raise ValueError("Battery capacity has to be > 0")

        self.c_nom = capacity_nom_Ah * 3600
        self.R_int = internal_resistance_mOhm / 1000
        self.soc = max(0.0, min(initial_soc, 1.0))

        self.soc_points = soc_points
        self.voltage_points = voltage_points

    def apply_current(self, current: float, duration: float) -> float:
        if duration < 0:
            raise ValueError("Duration must not be negative")

        self.soc = self.soc - ((current * duration) / self.c_nom)
        self.soc = max(0.0, min(self.soc, 1.0))

        return self.soc

    def is_empty(self) -> bool:
        return self.soc <= 0

    def is_full(self) -> bool:
        return self.soc >= 1

    def open_circuit_voltage(self) -> float:
        """
        Berechnet die Leerlaufspannung abhängig vom Ladezustand.
        Wenn Kennlinien vorhanden sind, werden diese verwendet.
        """
        if self.soc_points is not None and self.voltage_points is not None:
            voltage = np.interp(self.soc, self.soc_points, self.voltage_points)
        else:
            voltage = 32.0 + self.soc * (42.0 - 32.0)

        return float(voltage)

    def voltage(self, current: float = 0.0) -> float:
        """
        Berechnet die Spannung unter Last.
        """
        return self.open_circuit_voltage() - (self.R_int * current)

    def __str__(self):
        return f"BatteryPack(SoC={self.soc * 100:.1f}%, V={self.voltage():.2f} V)"